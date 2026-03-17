from agents.planner import Planner
from agents.researcher import Researcher
from agents.writer import Writer
from agents.reviewer import Reviewer

from memory import Memory

import json
from pathlib import Path

class Agent:
    def __init__(self):
        self.memory = Memory()
        self.planner = Planner()
        self.researcher = Researcher()
        self.writer = Writer()
        self.reflection = Reviewer()

        self.log_dir = Path("logs")
        for item in self.log_dir.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                import shutil
                shutil.rmtree(item)
    
    def log(self, what, info):
        with open(f"{self.log_dir}/{what}_log.json", "w") as f:
            #f.write(info)
            json.dump(info, f, indent=2, ensure_ascii=False, default=str)

    def run(self, topic, s_from=0, depth=0, max_depth=5):
        if depth >= max_depth:
            print("Stopped: too many retries")
            return self.memory.get(draft, "No draft available")

        if depth == 0:
            self.memory.add("topic", topic)

        plan = None
        researched_info = None
        draft = None

        if (s_from <= 0):
            plan = self.planner.create_plan(topic)
            self.log("plan", plan)
            self.memory.add("plan", plan)

        if (s_from <= 1):
            if plan is None:
                plan = self.memory.get("plan")
                self.log("plan", plan)
                if plan is None:
                    raise ValueError("Planner failed to produce plan")
            researched_info = self.researcher.gather_research(topic, plan)
            self.log("researched_info", researched_info)
            self.memory.add("researched_info", researched_info)

        if (s_from <= 2):
            if plan is None:
                plan = self.memory.get("plan")
                self.log("plan", plan)
                if plan is None:
                    raise ValueError("Planner failed to produce plan")
            if researched_info is None:
                researched_info = self.memory.get("researched_info")
                self.log("researched_info", researched_info)
                if researched_info is None:
                    raise ValueError("Planner failed to produce researched_info")
            feedback = self.memory.get("review_feedback")
            self.log("review_feedback", feedback)
            draft = self.writer.write_paper(topic, plan, researched_info, feedback)
            self.log("draft", draft)

            self.memory.add("draft", draft)

        if (s_from <= 3):
            review = self.reflection.review_paper(topic, plan, researched_info, draft)
            self.log("review", review)
            self.memory.add("review", review)

            if not review or "overall_assessment" not in review:
                return "Reviewer failed to produce valid output"

            assessment = review["overall_assessment"]
            self.log("assessment", assessment)
            if (assessment == "approved"):
                return draft
            elif (assessment == "revision_needed"):
                print(f"Retry depth: {depth} | revising draft")
                feedback = review.get("specific_feedback", "")
                self.log("review_feedback", feedback)
                self.memory.add("review_feedback", feedback)
                return self.run(topic, s_from=2, depth=depth+1, max_depth=max_depth)
            elif (assessment == "research_insufficient"):
                print(f"Retry depth: {depth} | expanding research")
                feedback = review.get("specific_feedback", "")
                self.log("review_feedback", feedback)
                if researched_info is None:
                    researched_info = self.memory.get("researched_info")
                expanded_research = self.researcher.expand_research(topic, plan, researched_info, feedback)
                self.log("expanded_research", expanded_research)

                self.memory.add("researched_info", expanded_research)
                self.memory.add("review_feedback", None)
                return self.run(topic, s_from=2, depth=depth+1, max_depth=max_depth)