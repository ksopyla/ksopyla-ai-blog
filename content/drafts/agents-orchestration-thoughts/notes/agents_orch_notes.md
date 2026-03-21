



Currenttly we are creating the agents manually, one by one, and then we are connecting them with each 
other to create a pipeline.


However I see this differently, what companies should or how they need to start thinking about their 
systems
- we have a problem that we need to solve - this is defined by the CEO, mangager, team leader, etc. - this 
is our main objective
  - problem needs to be defined clearly and concisely - however this is oftene the most difficult part, 
  and in normal life we even don't know exaclyw what we want to have, 
  - the framework should allo for refining the problem iteratively, 
- the company have a set of agents, each agent could be treated as expert, with expierience and knowledge 
in a specific domain, with a set of tools at their disposal, and thinking patterns
  - each agent is a separate entity not thight to a particular problem or task, but just an expert which 
  figour out how to contirbute to the problem solution
- having a problem we could define a Team (team of agents) that will be responsible for solving the problem
  - team is a dynamic group of agents that are working together to solve the problem
  - team id devoted to solving the problem
  - team has it own budget (time and money) - when this budget is spent the team finished their work - 
  inrespectively if the problem is solved or not
  - each team is evbaluated and got the feedback from
- there should exists some meta layer that will be responsible for learning and feedback loop for the teams
  - this layer will be responsible for learning from the teams feedback and improving the agents and the 
  teams
  - all the failures and successes should be recorded in company knowledge base
  - 
- there should exists persistent knowledge base accessible by all the agents (Read only)



how we should change our way of thinking about the AI systems?

- what I have observed is that now we are sticke to software 2.0 REST api, microservices based 
decomposition
- engineers are not thinking in term of agents and teams, but what is the input that help me prepare the 
expected output, this is in contradiction to the way we should think about the agentic systems
- we should more realiy on agents communication and collaboration: use the A2A communication, MCP or other 
communication protocols 
- discoverability of the agents is key, each agent should be able to be discovered by other agents that 
would help them to solve the problem
- the agentic systems are difficult from engineering perspective: asynchronous communication, concurrent 
execution, checkpointing, re-execution, resilience, scalability and observability are key challenges
- the one clue aspect is the agents authentication and authorization - how we should desing this part for 
the whole company, this is the challenge that we need to solve
- UI  becomes obsolete now voice first or your current chat application is the new UI where you can 
attache new agent.