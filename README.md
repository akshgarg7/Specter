# NegotiationSim

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
