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

    # def run(self, topic, s_from="0"):
    #     self.memory.add(f"Research topic: {topic}")

    #     plan = self.planner.create_plan(topic)

    #     self.memory.add(f"Plan created by the agent: \n{plan}")

    #     researched_info = self.researcher.gather_research(topic, plan)

    #     self.memory.add(f"Information gathered: \n{researched_info}")

    #     draft = self.writer.write_paper(topic, plan, researched_info)

    #     self.memory.add(f"Draft paper: \n{draft}")

    #     review = self.reflection.review_paper(topic, plan, researched_info, draft)

    #     self.memory.add(f"Review of the paper: \n{review}")

    #     if (review == "approved"):
    #         return draft
    #     elif (review == "revision_needed"):
    #         pass
    #     elif (review == "research_insufficient"):
    #         pass

    def run(self, topic, s_from=0, depth=0, max_depth=5):
        if depth >= max_depth:
            return "Stopped: too many retries"

        if depth == 0:
            self.memory.add("topic", topic)

        plan = None
        researched_info = None
        draft = None

        if (s_from <= 0):
            plan = self.planner.create_plan(topic)
            self.memory.add("plan", plan)

        if (s_from <= 1):
            if plan is None:
                plan = self.memory.get("plan")
                if plan is None:
                    raise ValueError("Planner failed to produce plan")
            researched_info = self.researcher.gather_research(topic, plan)
            self.memory.add("researched_info", researched_info)

        if (s_from <= 2):
            if plan is None:
                plan = self.memory.get("plan")
                if plan is None:
                    raise ValueError("Planner failed to produce plan")
            if researched_info is None:
                researched_info = self.memory.get("researched_info")
                if researched_info is None:
                    raise ValueError("Planner failed to produce researched_info")
            draft = self.writer.write_paper(topic, plan, researched_info)
            self.memory.add("draft", draft)

        if (s_from <= 3):
            review = self.reflection.review_paper(topic, plan, researched_info, draft)
            self.memory.add("review", review)

            if not review or "overall_assessment" not in review:
                return "Reviewer failed to produce valid output"

            assessment = review["overall_assessment"]
            if (assessment == "approved"):
                return draft
            elif (assessment == "revision_needed"):
                print(f"Retry depth: {depth} | restarting from stage {s_from}")
                return self.run(topic, s_from=2, depth=depth+1, max_depth=max_depth)
            elif (assessment == "research_insufficient"):
                print(f"Retry depth: {depth} | expanding research")
                feedback = review.get("feedback", "")
                if researched_info is None:
                    researched_info = self.memory.get("researched_info")
                expanded_research = self.researcher.expand_research(topic, plan, researched_info, feedback)

                self.memory.add("researched_info", expanded_research)
                return self.run(topic, s_from=2, depth=depth+1, max_depth=max_depth)