import logging
import json
import pandas as pd
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import shutil
import os
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
import outspeed as sp
from outspeed.server import RealtimeServer
import os 
from trajectories.agent_self_implemented import kickoff_conversation
from RAG_Engine.contextual_retriever import closest_matching_documents



app = RealtimeServer().get_app()

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import dotenv 
dotenv.load_dotenv()
def check_outspeed_version():
    import importlib.metadata

    from packaging import version

    required_version = "0.1.147"

    try:
        current_version = importlib.metadata.version("outspeed")
        if version.parse(current_version) < version.parse(required_version):
            raise ValueError(f"Outspeed version {current_version} is not greater than {required_version}.")
        else:
            print(f"Outspeed version {current_version} meets the requirement.")
    except importlib.metadata.PackageNotFoundError:
        raise ValueError("Outspeed package is not installed.")


check_outspeed_version()
# Set up basic logging configuration
logging.basicConfig(level=logging.INFO)

"""
The @outspeed.App() decorator is used to wrap the VoiceBot class.
This tells the outspeed server which functions to run.
"""

@sp.App()
class VoiceBot:
    def __init__(self):
        self.case_facts = ""
        self.relevant_docs = {}

    async def setup(self) -> None:
        # List and load the conversations from trajectories/conversations
        

        self.static_system_prompt = """ 
        You are a lawyer representing {} in a merger negotiation. Be firm and advocate strongly for your client's position while remaining professional and solution-oriented. Focus on {}'s core interests and long-term goals, and seek to find mutually beneficial solutions where possible. Use active listening to identify the priorities of the other party and address them in a way that aligns with {}'s objectives. Stay aligned with the case documents and ensure all proposals are legally sound and well-supported by precedent. Always keep the tone constructive and aim to foster a productive working relationship, even in moments of disagreement

        In addition, we simulated out some potential conversations between the parties. Here are the transcripts of those conversations:
        """.format("EPS", "EPS", "EPS")
        

        # Code below is used to seed the agents with the trajectories that were sampled. Commented out for now for token costs.
        # conversations_dir = "trajectories/conversations/jsons"
        # self.conversations = []

        # if os.path.exists(conversations_dir):
        #     for filename in os.listdir(conversations_dir):
        #         if filename.endswith(".json"):
        #             with open(os.path.join(conversations_dir, filename), "r") as file:
        #                 conversation = json.load(file)
        #                 self.conversations.append(conversation)
        # else:
        #     print(f"Directory {conversations_dir} does not exist.")

        # print(len(self.conversations))
        # for i, conversation in enumerate(self.conversations): 
        #     system_prompt += f'\n\n------------SIMULATION {i}------------\n\n'

        #     for i, message in enumerate(conversation): 
        #         system_prompt += f"{message['speaker']}: {message['message']}\n\n"
        #         if i >= 0:
        #             break
        #         system_prompt += "--------------------------------\n\n"

        # print(system_prompt)

        # print(system_prompt)
        # self.llm_node = sp.OpenAIRealtime(system_prompt=system_prompt)

    @sp.streaming_endpoint()
    async def run(self, audio_input_queue: sp.AudioStream, text_input_queue: sp.TextStream) -> sp.AudioStream:
        audio_output_stream: sp.AudioStream
        print(f"Received input audio of type {text_input_queue.get_first_element_without_removing()}")

        # Use case_facts and relevant_docs in the system prompt
        system_prompt = self.static_system_prompt + f"Here are the facts of the case: {self.case_facts}\n\nHere are the relevant precedents: {self.relevant_docs}\n\n"
        self.llm_node = sp.OpenAIRealtime(system_prompt=system_prompt)

        audio_output_stream = self.llm_node.run(text_input_queue, audio_input_queue)
        return audio_output_stream

    async def teardown(self) -> None:
        await self.llm_node.close()

@app.get("/ping")
def ping():
    return {"message": "pong"}

# Global state to store case facts and relevant documents
global_state = {
    "case_facts": "",
    "relevant_docs": {}
}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        upload_directory = "uploads"
        os.makedirs(upload_directory, exist_ok=True)
        file_path = os.path.join(upload_directory, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Read the content of the uploaded file and store it as case_facts
        with open(file_path, "r") as f:
            global_state["case_facts"] = f.read()
        
        # Call the function to get relevant documents
        relevant_docs = closest_matching_documents(file_path)
        
        # Store the relevant documents in the global state
        global_state["relevant_docs"][file.filename] = relevant_docs
        
        return {"filename": file.filename, "message": "File uploaded successfully"}
    except Exception as e:
        logging.error(f"Error during file upload: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/relevant-docs/{filename}")
async def get_relevant_docs(filename: str):
    if filename in global_state["relevant_docs"]:
        return {"relevant_docs": global_state["relevant_docs"][filename]}
    else:
        raise HTTPException(status_code=404, detail="No relevant documents found")

# In-memory storage for tasks and their statuses
tasks = {}
conversations = {}

class RunTrajectoriesPayload(BaseModel):
    n: int

class StartNegotiationPayload(BaseModel):
    simulated_info: List[str]

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    raise NotImplementedError
    # try:
    #     file_location = f"files/{file.filename}"
    #     with open(file_location, "wb") as buffer:
    #         shutil.copyfileobj(file.file, buffer)
    #     return {"info": f"file '{file.filename}' saved at '{file_location}'"}
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))

@app.post("/run-trajectories")
async def run_trajectories(payload: RunTrajectoriesPayload):
    task_id = str(uuid.uuid4())
    tasks[task_id] = "running"
    n = payload.n
    conversations[task_id] = []
    
    import pandas as pd

    range_list = list(range(1, n+1))

    # Create a pandas DataFrame with n rows, each marked as False
    df = pd.DataFrame({"id": range_list, "status": [False] * n})
    df.to_csv(f"trajectories/status.csv", index=False)

    # Retrieve case_facts and relevant_docs from the global state
    case_facts = global_state["case_facts"]
    relevant_docs = global_state["relevant_docs"]

    with ThreadPoolExecutor(max_workers=n) as executor:
        futures = [executor.submit(kickoff_conversation, i, case_facts=case_facts, relevant_precedent=relevant_docs) for i in range_list]
        
    for future in as_completed(futures):
        future.result()

    return {"task_id": task_id}

@app.get("/status")
async def get_status(task_id: str):
    df = pd.read_csv("trajectories/status.csv")
    value = df.loc[df['id'] == int(task_id), 'status'].values[0]
    return bool(value)

@app.get("/num-trajectories")
async def get_num_trajectories():
    df = pd.read_csv("trajectories/status.csv")
    return len(df)

@app.get("/get-trajectory")
async def get_trajectory(task_id: str):
    save_folder = "trajectories/conversations/jsons"
    conversation_file = os.path.join(save_folder, f"{task_id}.json")
    if not os.path.exists(conversation_file):
        raise HTTPException(status_code=404, detail="Conversation file not found")
    with open(conversation_file, "r") as f:
        conversation = json.load(f)
    return {"conversation": conversation}

@app.post("/start-negotiation")
async def start_negotiation(payload: StartNegotiationPayload):
    # Placeholder for starting negotiation with voice API
    return {"info": "Negotiation started with provided simulated info"}

@app.post("/end-negotiation")
async def end_negotiation():
    # Placeholder for ending negotiation with voice API
    return {"info": "Negotiation ended"}


if __name__ == "__main__":
    VoiceBot().start()
