import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
import shutil
import os
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed

app = FastAPI()

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
    conversations[task_id] = []

    def simulate_trajectory(task_id, n):
        # Simulate the conversation n times
        for _ in range(n):
            # Placeholder for actual simulation logic
            conversations[task_id].append(f"Simulated conversation {_+1}")
        tasks[task_id] = "complete"

    with ThreadPoolExecutor() as executor:
        future = executor.submit(simulate_trajectory, task_id, payload.n)
        as_completed([future])

    return {"task_id": task_id}

@app.get("/status")
async def get_status(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": tasks[task_id]}

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
