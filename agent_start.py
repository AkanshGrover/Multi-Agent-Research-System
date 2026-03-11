from agents.planner import Planner
from agents.researcher import Researcher
from agents.writer import Writer
from agents.reviewer import Reviewer

from memory import Memory #rn this is used for logging purposes

class Agent:
    def __init__(self):
        self.memory = Memory()
        self.planner = Planner()
        self.researcher = Researcher()
        self.writer = Writer()
        self.reflection = Reviewer()

    def run(self, topic):
        self.memory.add(f"Research topic: {topic}")

        plan = self.planner.create_plan(topic)

        self.memory.add(f"Plan created by the agent: \n{plan}")

        researched_info = self.researcher.gather_research(plan)

        self.memory.add(f"Information gathered: \n{researched_info}")

        draft = self.writer.write_paper(researched_info)

        self.memory.add(f"Draft paper: \n{draft}")

        review = self.reflection.review_paper(draft)

        self.memory.add(f"Review of the paper: \n{review}")

        if (review > 0):
            return draft
        else:
            pass #do something to restart the agents and improve the paper

