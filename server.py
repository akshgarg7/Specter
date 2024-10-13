import logging
import json
import pandas as pd
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import List
import shutil
import os
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
import outspeed as sp
from outspeed.server import RealtimeServer
from fastapi import HTTPException
import os 
from trajectories.agent_self_implemented import kickoff_conversation



app = RealtimeServer().get_app()

# print(os.getenv("OPENAI_API_KEY"))
# if "OPENAI_API_KEY" in os.environ: 
#     del os.environ["OPENAI_API_KEY"]

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
# logging.basicConfig(level=logging.DEBUG)

"""
The @outspeed.App() decorator is used to wrap the VoiceBot class.
This tells the outspeed server which functions to run.
"""


@sp.App()
class VoiceBot:
    async def setup(self) -> None:
        # List and load the conversations from trajectories/conversations
        conversations_dir = "trajectories/conversations/jsons"
        self.conversations = []

        if os.path.exists(conversations_dir):
            for filename in os.listdir(conversations_dir):
                if filename.endswith(".json"):
                    with open(os.path.join(conversations_dir, filename), "r") as file:
                        conversation = json.load(file)
                        self.conversations.append(conversation)
        else:
            print(f"Directory {conversations_dir} does not exist.")


        case_facts = open("negotiations/negotiation_case.txt", "r").read()
        system_prompt = """ 
    You are a lawyer representing {} in a merger negotiation. Be firm and advocate strongly for your client's position while remaining professional and solution-oriented. Focus on {}'s core interests and long-term goals, and seek to find mutually beneficial solutions where possible. Use active listening to identify the priorities of the other party and address them in a way that aligns with {}'s objectives. Stay aligned with the case documents and ensure all proposals are legally sound and well-supported by precedent. Always keep the tone constructive and aim to foster a productive working relationship, even in moments of disagreement. Here are the facts of the case: {}.

    In addition, we simulated out some potential conversations between the parties. Here are the transcripts of those conversations:
    """.format("EPS", "EPS", "EPS", case_facts)
        
        print(len(self.conversations))
        for i, conversation in enumerate(self.conversations): 
            system_prompt += f'------------SIMULATION {i}------------'
            # keep length of system prompt within 92767
            for i, message in enumerate(conversation): 
                system_prompt += f"{message['speaker']}: {message['message']} "
                if i >= 2: 
                    break
                system_prompt += "-------------------------------- "
            

        print(f"Sys prompt length: {len(system_prompt)}")

        system_prompt += ". Only output audio. "

        # print(system_prompt)
        self.llm_node = sp.OpenAIRealtime(system_prompt=system_prompt)

    @sp.streaming_endpoint()
    async def run(self, audio_input_queue: sp.AudioStream, text_input_queue: sp.TextStream) -> sp.AudioStream:
        audio_output_stream: sp.AudioStream
        print(f"Received input audio of type {text_input_queue.get_first_element_without_removing()}")
        audio_output_stream = self.llm_node.run(text_input_queue, audio_input_queue)

        return audio_output_stream

    async def teardown(self) -> None:
        await self.llm_node.close()

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.post("/upload")
def upload(pdf_file: UploadFile):
    """ function to upload a PDF file to storage """
    """ https://fastapi.tiangolo.com/tutorial/request-files/#multiple-file-uploads to have a form upload"""
    print(f"Received file of size {pdf_file.size}b")
    with open(f"pdf/{pdf_file.filename}", "wb") as local_copy:
        local_copy.write(pdf_file.file.read())
        print(f"Successfully wrote to pdf/{pdf_file.filename}")
    return {"filename": pdf_file.filename}

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

    # print('hi')
    # logging.info(f"Kicking off conversations")
    import pandas as pd

    # Create a pandas DataFrame with n rows, each marked as False
    df = pd.DataFrame({"id": range(n), "status": [False] * n})
    df.to_csv(f"trajectories/status.csv", index=False)


    with ThreadPoolExecutor(max_workers=n) as executor:
        futures = [executor.submit(kickoff_conversation, i) for i in range(n)]
        
    for future in as_completed(futures):
        future.result()

    return {"task_id": task_id}

@app.get("/status")
async def get_status(task_id: str):
    df = pd.read_csv("trajectories/status.csv")
    return {"status": df.loc[df["id"] == int(task_id), "status"].values[0]}

@app.get("/get-trajectory")
async def get_trajectory(task_id: str):
    save_folder = "trajectories/conversations"
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