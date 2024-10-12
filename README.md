# NegotiationSim
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
