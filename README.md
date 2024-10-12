# Spector
We are am building a tool to help prepare lawyers for negotiations by creating a voice agent that negotiates back and forth with you.

It involves three steps: 
1) Integrating with information from past cases and the current case to retrieve relevant information about the case using past precedent
2) sim out 100 potential trajectories for negotiations between agent 1 (representing company 1) and agent 2 (representing company 2). These trajectories then are used to create an intelligent AI persona that can think of more complex use cases. 
3) The persona is fed into the Chat GPT voice endpoint to initialize it. Then the voice agent takes the stance of opposing counsel and negotiates against you. 

![image](https://github.com/user-attachments/assets/2afa4829-beb0-46e9-b554-fef842573004)

# Rest API
POST Request at /upload 
- Payload (Pass in PDF Contents)
- Loads and saves the PDF

POST Request at /run-trajectories
- Payload (n = number of trajectories to simulate)
- Launches the parallel units for simming out trajectories concurrently

GET request at /status
- query (task id)
- Returns whether the conversation for task i is complete

GET Request at /get-trajectory
- query (task id)
- Returns the conversation between representative A and B for task id

SOME Request to the voice API  /start-negotiation
- payload (simulated info from the different trajectories)
- Starts the converation between the agent and us

SOME request to the voice API /end-negotiation
- Ends the conversation

# Todos
- Multiple trajectories, multi-agent collaboration (Aksh)
- Upload, Voice API Stuff (Mike)

# More Deets
The goal is to develop a tool that helps lawyers prepare for negotiations by simulating back-and-forth negotiations with an AI-powered voice agent. The agent represents opposing counsel and utilizes past case precedents and a simulation of possible negotiation trajectories to enhance realism and strategy formulation. 

### Key Steps and Features

1. **Case Information Integration (Past and Current Cases):**
   - **Data Retrieval:** The system integrates with a database of past cases and the current case at hand to extract relevant information. The retrieval is powered by a retrieval-augmented generation (RAG) model that efficiently pulls legal precedents, outcomes, strategies, and tactics that are relevant to the current negotiation.
   - **Precedent Matching:** By analyzing similarities in case details, the tool identifies key precedents that might shape the negotiation strategy, highlighting historical patterns and their potential implications for the current case.

2. **Simulation of Negotiation Trajectories:**
   - **Agent 1 vs. Agent 2 Dynamics:** Two agents, one representing each party (company 1 and company 2), simulate a wide range of potential negotiation pathways (trajectories). Each agent leverages the retrieved case information and applies different negotiation strategies to explore possible outcomes.
   - **Parallel Simulations:** The system generates and runs 100 potential negotiation trajectories in parallel, covering various tactics, strategies, and outcomes. This large-scale simulation allows the tool to map out a diverse set of negotiation outcomes, enabling lawyers to visualize different ways the negotiation could unfold.
   - **Trajectory Evaluation:** Each trajectory is analyzed for potential success, risks, and opportunities, helping the lawyer prepare for a wide array of negotiation moves, counter-moves, and final outcomes.

3. **Intelligent AI Persona Creation:**
   - **Persona Synthesis:** After running the 100 trajectories, the system synthesizes the knowledge gained from the simulations into an intelligent AI persona. This persona embodies the thought process, strategies, and negotiation stances of an experienced opponent, enabling more nuanced and sophisticated interactions during practice negotiations.
   - **Adaptive Responses:** The AI persona is designed to adapt to different negotiation styles and react dynamically to the user’s inputs, helping the lawyer refine their tactics in real-time.

4. **Voice Bot Integration (Chat GPT Voice Endpoint):**
   - **Natural Language Interaction:** Once the intelligent persona is generated, it is integrated into a voice bot powered by the Chat GPT voice endpoint. This allows the user to interact with the agent in a natural, conversational manner, simulating a real negotiation scenario with opposing counsel.
   - **Realistic Back-and-Forth Negotiations:** The voice bot, representing opposing counsel, negotiates against the user. It simulates pressure tactics, alternative offers, counterarguments, and other elements that a lawyer would face in real-world negotiations, offering a highly immersive preparation experience.

### Value Proposition:
The primary value proposition is to **“Enable anyone to prepare against expert negotiator chatbots trained on past case precedent.”** This tool empowers lawyers to practice and refine their negotiation strategies by interacting with an AI-powered opponent that has been trained on relevant case law and hypothetical trajectories. It provides a safe and controlled environment for legal professionals to prepare for high-stakes negotiations with confidence.
