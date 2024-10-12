import os 
from autogen import ConversableAgent
import autogen

def multi_agent_conversation(agent1_name, agent1_system_message, agent2_name, agent2_system_message, case_facts, config_list):
    # Create ConversableAgent instances for both agents
    agent1 = ConversableAgent(
        agent1_name, 
        llm_config={"config_list": config_list},
        system_message=agent1_system_message,
        human_input_mode="NEVER"
    )
    
    agent2 = ConversableAgent(
        agent2_name, 
        llm_config={"config_list": config_list},
        system_message=agent2_system_message,
        human_input_mode="NEVER"
    )
    
    # Initialize the group chat with the two agents
    groupchat = autogen.GroupChat(
        agents=[agent1, agent2],
        messages=[f"Welcome to the negotiation. Here are the facts of the case: {case_facts}"],
        max_round=20
    )
    
    # Create a GroupChatManager to manage the conversation
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})
    
    # Initiate the conversation
    agent1.initiate_chat(manager, message=f"Hi, my name is {agent1_name}. It's nice to meet you, {agent2_name}.")

# Example usage
if os.getenv("OPENAI_API_KEY"):
    del os.environ["OPENAI_API_KEY"]

import dotenv
dotenv.load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

config_list = [{"model": "gpt-4o-mini", "api_key": api_key, "temperature": 0.8}]
case_facts = open("negotiation_case.txt", "r").read()
multi_agent_conversation(
    agent1_name="Brendan",
    agent1_system_message="You are negotiating a deal. " + case_facts,
    agent2_name="Adarsh",
    agent2_system_message="You are negotiating a deal. " + case_facts,
    case_facts=case_facts,
    config_list=config_list
)