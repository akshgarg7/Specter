import autogen 
import os
import json
from autogen import AssistantAgent, UserProxyAgent, ConversableAgent
from autogen.coding import DockerCommandLineCodeExecutor
import dotenv 
from openai import OpenAI

dotenv.load_dotenv()

# Set up the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")

question_prompt = f"""Analyze their interview transcript to determine how they did. 
                    In the end, you want to end with a list of 5 reasons why this person is a strong candidate and 5 reasons why they are not. Also agree on a score from 1 to 10 for the interview.
                    I want you to focus on both their technical abilities and proficiency of communiation. 

                    End with a list of 5 reasons why this person is a strong candidate and 5 reasons why they are not. Also decide on a score of 1 to 10 for the interview.
                """
client = OpenAI(api_key=api_key)



injections = {
    "Brendan": "You are generally optimistic and focus more on the soft skills that a person has.",
    "Adarsh": "You are an extremely technical person and critical of each person that you evaluate. Be harsh in your interview.",
    "Surya": "You are very operational and want to see good practicality in the candidates. You are neutral in your evaluation."
}


for person, injection in injections.items():
    response = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "system", "content": f"You are evaluating a person's interview and seeing whether they did well or not. {injection}"},
                    {
                        "role": "user", "content": question_prompt
                }
                ],
                max_tokens=500,
                temperature=0.5,
            )


# Create an AssistantAgent instance named "assistant" with the LLM configuration
config_list = [{"model": "gpt-3.5-turbo", "api_key": api_key, "temperature": 0.8}]
assistant = AssistantAgent(name="assistant", llm_config={"config_list": config_list})

shared_prompt = """
                You are evaluating a person's interview and seeing whether they did well or not. Before responding to other people, first shared your own analysis on the candidate.. 
                You will have to negotiate with Adarsh and Surya to come to a conclusion; however, push back to support your own arguments as much as possible. 
                While you should defend your stance, you need to realize when other points make sense.
                In the end, your goal is to reach a shared consensus. Cite an explicit sentence from the interview transcript to support your argument. 

                In the end, you want to end with a list of 5 reasons why this person is a strong candidate and 5 reasons why they are not. 
                Also agree on a score from 1 to 10 for the interview.
                """
brendan_agent = ConversableAgent(
    "Brendan", 
    llm_config={"config_list": config_list},
    system_message=f"You are a very optimistic person. {shared_prompt}",
    human_input_mode="NEVER"
)

adarsh_agent = ConversableAgent(
    "Adarsh", 
    llm_config={"config_list": config_list},
    system_message=f"You are a very negative person and critical of the candidates. {shared_prompt}",
    human_input_mode="NEVER"
)

surya_agent = ConversableAgent(
    "Surya", 
    llm_config={"config_list": config_list},
    system_message=f"You are a neutral person, who can hedge the commentary between Brendan and Adarsh. {shared_prompt}",
    human_input_mode="NEVER"
)

from load_interview import load_interview
transcript, questions, answers = load_interview("interviews/1.json")

groupchat = autogen.GroupChat(agents=[brendan_agent, adarsh_agent, surya_agent, assistant], messages = [f"here's the transcript from the interview, use this to base your responses: {transcript}"], max_round=20) 
manager = autogen.GroupChatManager(groupchat = groupchat, llm_config={"config_list": config_list})

brendan_agent.initiate_chat(manager, message=f"Hi, I'm Brendan. This is the latest transcript from the interview. Curious what everyone thinks about it. {transcript}")
# manager.initiate_chat(brendan_agent, f"Attached is a transcript of the interview. Let's start by reading it. Then proceed to evaluate these candidates by discussing with your colleagues. {transcript}")