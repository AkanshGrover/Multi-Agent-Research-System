from executor import Executor
from tools.fetch_info import InfoFetcher
from tools.fetch_rt_info import InfoFetcherRT
import json
from datetime import datetime, timedelta


class Researcher:

    def __init__(self):
        self.executor = Executor()
        self.fetcher = InfoFetcher()
        self.rt_fetcher = InfoFetcherRT()

        self.github_page = 1
        self.so_page = 1
        self.research_attempts = 0

    def gather_research(self, topic, plan):
        self.research_attempts += 1

        if not self.fetcher.is_cs_topic(topic):
            return self.create_domain_warning(topic)
        
        structured_data = self.collect_sources(topic)
        summarized_data = self.prepare_data_summary(structured_data)

        try:
            synthesized = self.synthesize_research(topic, plan, summarized_data)

            synthesized["metadata"] = {
                "research_attempt": self.research_attempts,
                "github_page": self.github_page,
                "stackoverflow_page": self.so_page,
                "timestamp": datetime.now().isoformat()
            }

            return synthesized
        
        except Exception as e:
            print("Research synthesis failed:", e)
            return self.create_fallback_data(topic)


    def collect_sources(self, topic):
        static_sources = self.fetcher.fetch_all(topic)
        realtime_sources = self.rt_fetcher.fetch_all(topic, github_page=self.github_page, so_page=self.so_page)

        self.github_page += 1
        self.so_page += 1

        return {
            "static_sources": static_sources,
            "realtime_sources": realtime_sources
        }
    
    def prepare_data_summary(self, data):
        summary = {
            "arxiv_papers": [],
            "tech_news": [],
            "github_projects": [],
            "stackoverflow_questions": [],
            "insights": data["static_sources"]["insights"]
        }

        # limit arxiv
        for paper in data["static_sources"]["sources"]["arxiv"][:5]:

            summary["arxiv_papers"].append({
                "title": paper["title"],
                "abstract": paper["abstract"][:300],
                "authors": paper["authors"][:3],
                "published": str(paper["published"]),
                "relevance_score": paper["relevance_score"]
            })

        # hackernews
        for post in data["static_sources"]["sources"]["hackernews"][:5]:

            summary["tech_news"].append({
                "title": post["title"],
                "points": post["points"],
                "comments": post["comments"],
                "url": post["url"]
            })

        # github
        for repo in data["realtime_sources"]["sources"]["github"][:5]:

            summary["github_projects"].append({
                "name": repo["name"],
                "description": repo["description"],
                "stars": repo["stars"],
                "language": repo["language"]
            })

        # stackoverflow
        for q in data["realtime_sources"]["sources"]["stackoverflow"][:5]:

            summary["stackoverflow_questions"].append({
                "title": q["title"],
                "views": q["views"],
                "answers": q["answers"],
                "tags": q["tags"]
            })

        return summary

    def synthesize_research(self, topic, plan, data):
        system_prompt = """
You are an expert computer science research analyst.

Your task is to analyze large amounts of raw technical research data and extract meaningful structured insights.

You are part of a multi-agent research system.

Your responsibility is to transform raw technical data from multiple sources into structured research findings that will later be used to write a technical research report.

You must carefully analyze the data and identify:

• key technical concepts
• major research directions
• important architectures or algorithms
• real-world implementations
• engineering trade-offs
• emerging trends
• performance considerations

You must NOT invent information that does not exist in the data.

Focus on extracting insights supported by the research sources.
"""

        user_prompt = f"""
RESEARCH TOPIC
{topic}


RESEARCH PLAN
{json.dumps(plan, indent=2)}


RAW RESEARCH DATA
{json.dumps(data, indent=2)}


TASK

Analyze the research data and organize findings according to the research plan.


OUTPUT FORMAT

Return a structured JSON object:

{{
 "topic_overview": "summary of the technical domain",

 "key_concepts": [],

 "literature_sources": [
   {{
     "title": "",
     "authors": [],
     "year": "",
     "main_contribution": "",
     "methodology": "",
     "limitations": ""
   }}
 ],

 "methodologies": [],

 "research_findings": [
   {{
     "question": "",
     "insights": [],
     "supporting_sources": []
   }}
 ],

 "comparative_insights": [],

 "important_systems_or_projects": [],

 "implementation_patterns": [],

 "performance_considerations": [],

 "security_considerations": [],

 "research_gaps": [],

 "emerging_trends": [],

 "data_quality_score": 0.0
}}


IMPORTANT RULES

• Only use evidence from the provided research data
• Do NOT hallucinate research papers or projects
• Organize findings clearly for a technical writer
• Focus on insights rather than raw information
"""

        research = self.executor.executePrompt(
            system_prompt,
            user_prompt,
            temperature=0.4,
            isJson=True
        )

        return research
    
    def create_domain_warning(self, topic):
        return {
            "topic_overview": f"The topic '{topic}' does not appear to be strongly related to Computer Science or Information Technology.",

            "key_concepts": [],

            "research_findings": [],

            "important_systems_or_projects": [],

            "implementation_patterns": [],

            "performance_considerations": [],

            "security_considerations": [],

            "emerging_trends": [],

            "data_quality_score": 0.1
        }
    
    def expand_research(self, topic, plan, previous_research, feedback):

        system_prompt = """
You are an expert CS researcher improving an existing research analysis.

You must expand the research based on reviewer feedback.

Focus on filling missing gaps while keeping the same structure.
"""

        user_prompt = f"""
TOPIC
{topic}

RESEARCH PLAN
{json.dumps(plan, indent=2)}

PREVIOUS RESEARCH
{json.dumps(previous_research, indent=2)}

REVIEWER FEEDBACK
{feedback}

Expand the research findings.

Return updated JSON with deeper insights.
"""

        return self.executor.executePrompt(
            system_prompt,
            user_prompt,
            temperature=0.4,
            isJson=True
        )
    
    def create_fallback_data(self, topic):#this gonna be improved in future, dont know whether needed or not

        return {
            "topic_overview": f"General overview of {topic}.",

            "key_concepts": [
                topic,
                "modern computing architectures",
                "scalable systems"
            ],

            "research_findings": [],

            "important_systems_or_projects": [],

            "implementation_patterns": [],

            "performance_considerations": [],

            "security_considerations": [],

            "emerging_trends": [],

            "data_quality_score": 0.3
        }