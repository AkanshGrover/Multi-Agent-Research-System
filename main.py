from agent_start import Agent

agent = Agent()

while True:
    topic = input("Enter topic: ")
    
    if (topic == "exit"):
        break

    ans = agent.run(topic)

    print(ans)