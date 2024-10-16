# Specter
Specter is an AI powered web platform designed to help lawyers and legal professionals prepare for case negotiations by simulating potential outcomes. Users upload a case that they want to practice with in PDF format, which we can then cross reference against prior cases. All relevant information for the case is used to simulate multiple trajectories between an agent representing party A and an agent representing party B. Each of these trajectories forms a catalog of strategies that worked and didn't when negotiating and are used to initialize a persona for opposing counsel, one that is now much stronger and competent. This persona is then integrated with the GPT4 voice mode, which a lawyer at your firm can practice negotiating against, until a deal is verbally confirmed.

![image](https://github.com/user-attachments/assets/2784feb1-fb97-465d-b319-c912f2d20474)

## High Level Overview

At a high level, it involves three steps: 
1) Integrating with information from past cases and the current case to retrieve relevant information about the case using past precedent. 
2) Simulating 100 potential trajectories for negotiations between agent 1 (representing company 1) and agent 2 (representing company 2). These trajectories then are used to create an intelligent AI persona that can think of more complex use cases. 
3) The persona is fed into the Chat GPT voice endpoint to initialize it. Then the voice agent takes the stance of opposing counsel and negotiates against you.



## RAG Engine
   - Our RAG Engine uses a **contextual summary** approach pioneered by Anthropic, which allows for more efficient and accurate extraction of legal precedents, outcomes, strategies, and tactics relevant to the current negotiation. 
   - All information is stored in a pinecone vector database. The allows easy retrieval of facts about the case. This approach ensures that the AI persona is well-informed and capable of simulating realistic negotiation scenarios.

 ![image](https://github.com/user-attachments/assets/24abc685-d8b9-4bf7-b5a9-0c9336a0720a)


## Simulation Infrastructure
   - **Agent 1 vs. Agent 2 Dynamics:** Two agents, one representing each party (company 1 and company 2), simulate a wide range of potential negotiation pathways (trajectories). Each agent leverages the retrieved case information and applies different negotiation strategies to explore possible outcomes.
   - **Parallel Simulations:** The system generates and runs 100 potential negotiation trajectories in parallel, covering various tactics, strategies, and outcomes. This large-scale simulation allows the tool to map out a diverse set of negotiation outcomes, enabling lawyers to visualize different ways the negotiation could unfold.
   - **Trajectory Evaluation:** Each trajectory is analyzed for potential success, risks, and opportunities, helping the lawyer prepare for a wide array of negotiation moves, counter-moves, and final outcomes.

![image](https://github.com/user-attachments/assets/8f8cfef4-300f-49de-93e9-53d9337d07f3)

## Intelligent AI Persona Creation
   - **Persona Synthesis:** After running the 100 trajectories, the system synthesizes the knowledge gained from the simulations into an intelligent AI persona. This persona embodies the thought process, strategies, and negotiation stances of an experienced opponent, enabling more nuanced and sophisticated interactions during practice negotiations.
   - **Adaptive Responses:** The AI persona is designed to adapt to different negotiation styles and react dynamically to the user’s inputs, helping the lawyer refine their tactics in real-time.

## Voice Bot Integration (Chat GPT Voice Endpoint)
   - **Natural Language Interaction:** Once the intelligent persona is generated, it is integrated into a voice bot powered by the Chat GPT voice endpoint. This allows the user to interact with the agent in a natural, conversational manner, simulating a real negotiation scenario with opposing counsel.
   - **Realistic Back-and-Forth Negotiations:** The voice bot, representing opposing counsel, negotiates against the user. It simulates pressure tactics, alternative offers, counterarguments, and other elements that a lawyer would face in real-world negotiations, offering a highly immersive preparation experience.

## Get Started: 
1) Clone: Clone the repo
2) Requirements: `pip install -r requirements.txt`
3) API Keys: Add OpenAI and Pinecone Keys in .env
4) Host backend: `python server.py` from root folder
5) Host frontend: Navigate to UI/specter, and run `npm run dev`

## Credits
- Frontend based on Harvey.ai 
- Voice API based on OpenAI's ChatGPT Voice Endpoint
- Voice API hosted on outspeed. 
- A LOT of help from Cursor :) 


