import pandas as pd
import json 
from openai import OpenAI
import os
import threading

print(os.getenv("OPENAI_API_KEY"))
# if os.getenv("OPENAI_API_KEY"):
#     del os.environ["OPENAI_API_KEY"]


import dotenv
dotenv.load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
case_facts = open("cases/negotiation_case.txt", "r").read()

# Set up your OpenAI API key
class TextAgent:
    def __init__(self, name, system_message):
        self.name = name
        self.system_message = system_message
        self.conversation_history = [{"role": "system", "content": self.system_message}]  # Initialize with system message

    def get_response(self, prompt):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=prompt, 
            temperature=0.8
        )
        return response.choices[0].message.content.strip()

    def add_message(self, role, content):
        self.conversation_history.append({"role": role, "content": content})

    def respond(self):
        # print(self.conversation_history)
        return self.get_response(self.conversation_history)


def consensus_reached(conversation_history):
    prompt = [
        {"role": "system", "content": "You are an expert in analyzing negotiation conversations to determine if a consensus has been reached. Only say that a consensus has been reached if the two parties have agreed on all terms. If there are any disagreements, return false. "},
        {"role": "user", "content": f"Here is the conversation history: {conversation_history}. Has a consensus been reached? Respond with 'true' or 'false'. Output a json formatted as {{'consensus': true/false}}."}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=prompt,
        response_format={"type": "json_object"},
        temperature=0.0
    )

    consensus = response.choices[0].message.content.strip()
    consensus_json = json.loads(consensus)
    return consensus_json["consensus"]

def simulate_conversation(agent1, agent2, initial_message, num_turns=5):
    conversation_history = []
    agents = []

    # Start the conversation
    agent1.add_message("user", initial_message)
    agent2.add_message("assistant", initial_message)
    conversation_history.append(initial_message)
    agents.append(agent1.name)

    print(f"Conversation Start: {initial_message}")

    for turn in range(num_turns):
        # Agent 2 responds
        agent2_response = agent2.respond()
        agent2.add_message("assistant", agent2_response)
        agent1.add_message("user", agent2_response)
        conversation_history.append(agent2_response)
        agents.append(agent2.name)

        # Agent 1 responds
        agent1_response = agent1.respond()
        agent1.add_message("assistant", agent1_response)
        agent2.add_message("user", agent1_response)
        conversation_history.append(agent1_response)
        agents.append(agent1.name)

        if consensus_reached(conversation_history):
            print("Consensus reached!")
            break

    return conversation_history, agents

def store_conversation_history(conversation_history, agents, save_path):
    with open(save_path, "w") as f:
        for line, agent in zip(conversation_history, agents):
            f.write(f"{agent}: {line}\n")

def store_conversation_history_json(conversation_history, agents, save_path):
    conversation_data = []
    for line, agent in zip(conversation_history, agents):
        conversation_data.append({"speaker": agent, "message": line})

    with open(save_path, "w") as f:
        json.dump(conversation_data, f, indent=4)

conversation_starters = {
    1: "Hi", 
    2: "i hate you",
    3: "let's discuss the equity split and leadership structure for the merger.", 
    4: "We need more money",
    5: "I want to be CEO",
    6: "I want to be in charge of the new office",
    7: "I want 4 board seats", 
    8: "We can't merge",
    9: "We have larger teams than you",
    10: "Raise your standards",
}

def update_status_csv(run_id):
    status_file_path = "trajectories/status.csv"
    lock = threading.Lock()
    with lock:
        df = pd.read_csv(status_file_path)
        if run_id in df["id"].values:
            df.loc[df["id"] == run_id, "status"] = True
        else:
            df = pd.concat([df, pd.DataFrame([{"id": run_id, "status": True}])], ignore_index=True)
        df.to_csv(status_file_path, index=False)

def kickoff_conversation(run_id, max_turns=2):
    print(f"Kicking off conversation {run_id}")
    # Create two agents with system messages
    system_message_template = """ 
    You are a lawyer representing {} in a merger negotiation. Be firm and advocate strongly for your client's position while remaining professional and solution-oriented. Focus on {}'s core interests and long-term goals, and seek to find mutually beneficial solutions where possible. Use active listening to identify the priorities of the other party and address them in a way that aligns with {}'s objectives. Stay aligned with the case documents and ensure all proposals are legally sound and well-supported by precedent. Always keep the tone constructive and aim to foster a productive working relationship, even in moments of disagreement. Keep your comments to less than 50 words. Here are the facts of the case: {}
    """

    agent1_system_message = system_message_template.format("GTI", "GTI", "GTI", case_facts)
    agent2_system_message = system_message_template.format("EPS", "EPS", "EPS", case_facts)

    agent1 = TextAgent("Harvey (GTI)", agent1_system_message)
    agent2 = TextAgent("Mike (EPS)", agent2_system_message)

    # Simulate the conversation
    # initial_message = conversation_starters.get(run_id, "Hello")
    initial_message = "Hello"
    conversation_history, agents = simulate_conversation(agent1, agent2, initial_message=initial_message, num_turns=max_turns)
    store_conversation_history(conversation_history, agents, f"trajectories/conversations/txts/{run_id}.txt")
    store_conversation_history_json(conversation_history, agents, f"trajectories/conversations/jsons/{run_id}.json")
    print(f"ID {run_id}: {conversation_history[-1]}")

if __name__ == "__main__":
    kickoff_conversation(1)