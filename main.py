from agent_start import Agent
from tools.convert_to_word import convert_word

agent = Agent()

while True:
    topic = input("Enter topic: ")
    
    if (topic == "exit"):
        break

    ans = agent.run(topic)

    print(ans)#just in case word file is not generated, this is gonna be removed in future

    print("Paper generated")
    convert_word(ans, topic)
    print(f"Paper generated is saved as {topic}_review_paper.docx")