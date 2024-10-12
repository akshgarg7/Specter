import os
import autogen
from autogen import ConversableAgent
from openai import OpenAI

# Or start logging to a file
logging_session_id = autogen.runtime_logging.start(logger_type="file", config={"filename": "runtime.log"})


if os.getenv("OPENAI_API_KEY"):
    del os.environ["OPENAI_API_KEY"]

import dotenv
dotenv.load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

case_facts = open("negotiation_case.txt", "r").read()
lawyer1_agent = ConversableAgent(
    name="Lawyer1_Agent",
    system_message="You are a lawyer representing GTI in a merger negotiation. Adhere to the suggestions outlined in the case documents. Here are the facts of the case: {case_facts}",
    llm_config={"config_list": [{"model": "gpt-4o-mini", "api_key": api_key}]},
)
lawyer2_agent = ConversableAgent(
    name="Lawyer2_Agent",
    system_message="You are a lawyer representing EPS in a merger negotiation. Adhere to the suggestions outlined in the case documents. Here are the facts of the case: {case_facts}",
    llm_config={"config_list": [{"model": "gpt-4o-mini", "api_key": api_key}]},
)

chat_result = lawyer1_agent.initiate_chat(
    lawyer2_agent,
    message="Let's discuss the equity split and leadership structure for the merger.",
    summary_method="reflection_with_llm",
    max_turns=3,
)

print(chat_result.cost)
print(chat_result.messages)