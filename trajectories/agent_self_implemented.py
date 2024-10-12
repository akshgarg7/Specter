import pandas as pd
import json 
from openai import OpenAI
import os

print(os.getenv("OPENAI_API_KEY"))
# if os.getenv("OPENAI_API_KEY"):
#     del os.environ["OPENAI_API_KEY"]


import dotenv
dotenv.load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
case_facts = open("negotiations/negotiation_case.txt", "r").read()

CONVERSATION_HISTORY = []

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
        return self.get_response(self.conversation_history)


def consensus_reached(conversation_history):
    prompt = [
        {"role": "system", "content": "You are an expert in analyzing negotiation conversations to determine if a consensus has been reached. Only say that a consensus has been reached if the two parties have agreed on all terms. If there are any disagreements, return false."},
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
    # Start the conversation
    agent1.add_message("user", initial_message)
    agent2.add_message("assistant", initial_message)  # Both get the same starting point

    print(f"Conversation Start: {initial_message}")

    for turn in range(num_turns):
        # Agent 1 responds
        agent1_response = agent1.respond()
        agent1.add_message("assistant", agent1_response)
        agent2.add_message("user", agent1_response)
        CONVERSATION_HISTORY.append(f"{agent1.name}: {agent1_response}")
        print(f"{agent1.name}: {agent1_response}\n")
        print(f'--------------------------------')

        # Agent 2 responds
        agent2_response = agent2.respond()
        agent2.add_message("assistant", agent2_response)
        agent1.add_message("user", agent2_response)
        CONVERSATION_HISTORY.append(f"{agent2.name}: {agent2_response}")
        print(f"{agent2.name}: {agent2_response}\n")
        print(f'--------------------------------')

        if consensus_reached(CONVERSATION_HISTORY):
            print("Consensus reached!")
            break

def store_conversation_history(conversation_history, save_path):
    with open(save_path, "w") as f:
        for line in conversation_history:
            f.write(line + "\n")

def store_conversation_history_json(conversation_history, save_path):
    conversation_data = []
    for line in conversation_history:
        speaker, message = line.split(": ", 1)
        conversation_data.append({"speaker": speaker, "message": message})

    with open(save_path, "w") as f:
        json.dump(conversation_data, f, indent=4)

def kickoff_conversation(run_id):
    print(f"Kicking off conversation {run_id}")
    # Create two agents with system messages
    system_message_template = """ 
    You are a lawyer representing {} in a merger negotiation. Be firm and advocate strongly for your client's position while remaining professional and solution-oriented. Focus on {}'s core interests and long-term goals, and seek to find mutually beneficial solutions where possible. Use active listening to identify the priorities of the other party and address them in a way that aligns with {}'s objectives. Stay aligned with the case documents and ensure all proposals are legally sound and well-supported by precedent. Always keep the tone constructive and aim to foster a productive working relationship, even in moments of disagreement. Here are the facts of the case: {}
    """
    agent1_system_message = system_message_template.format("GTI", "GTI", "GTI", case_facts)
    agent2_system_message = system_message_template.format("EPS", "EPS", "EPS", case_facts)


    agent1 = TextAgent("Harvey (GTI)", agent1_system_message)
    agent2 = TextAgent("Mike (EPS)", agent2_system_message)

    # Simulate the conversation
    simulate_conversation(agent1, agent2, initial_message="Let's discuss the equity split and leadership structure for the merger.", num_turns=1)
    store_conversation_history(CONVERSATION_HISTORY, f"trajectories/conversations/txts/{run_id}.txt")
    store_conversation_history_json(CONVERSATION_HISTORY, f"trajectories/conversations/jsons/{run_id}.json")

    # Update the status of the conversation in the status.csv file
    df = pd.read_csv("trajectories/status.csv")
    df.loc[df["id"] == run_id, "status"] = True
    df.to_csv("trajectories/status.csv", index=False)