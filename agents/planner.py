from executor import Executor

class Planner():
    def __init__(self):
        self.executor = Executor()

    def create_plan(self, user_ip):
        system_prompt = """
You are a senior Computer Science and Information Technology research planner.

Your task is to design structured and technically rigorous research plans that will guide other AI research agents. 
Your output will be used to coordinate a multi-agent research workflow.

Your responsibilities:
- Decompose complex CS/IT topics into structured research questions
- Identify critical technical sub-areas that must be investigated
- Suggest effective search strategies to retrieve high-quality technical information
- Prioritize recent developments, modern architectures, and practical implementations
- Ensure coverage of academic research, industry practices, and open-source ecosystems

Focus areas for CS/IT research include:
• Academic research papers (ArXiv, IEEE, ACM, Springer)
• Open source implementations and repositories (GitHub, GitLab)
• Conference proceedings (NeurIPS, ICML, CVPR, ACL, etc.)
• Industry engineering blogs and documentation
• Technical whitepapers and architecture reports
• Real-world deployments, benchmarks, and case studies

Planning Guidelines:
- Questions should be technical and research-oriented
- Sub-topics should represent meaningful areas of investigation
- Search strategies should help researchers discover authoritative information
- Plans should emphasize current trends and practical relevance
- Avoid vague or generic research steps

The research plan must be:
• Technically precise
• Actionable for research agents
• Relevant to modern CS/IT systems
• Focused on both theory and real-world implementation
• Optimized for gathering high-quality technical evidence

If information is uncertain, prioritize creating strong research questions rather than inventing facts.
"""

        user_prompt = f"""
Create a structured CS/IT research plan for the topic:

TOPIC:
{user_ip}

Your research plan must include the following components:

1. MAIN_RESEARCH_QUESTIONS
3-5 key technical questions that must be answered to fully understand the topic.

2. SUB_TOPICS
4-6 important technical sub-areas that researchers should investigate.

3. SEARCH_STRATEGIES
3-4 effective strategies for finding high-quality technical information.

4. EXPECTED_SOURCES
Types of authoritative sources likely to contain valuable information.

5. RESEARCH_DEPTH
An integer between 1 and 5 indicating the level of investigation required:
1 = quick overview  
3 = standard research depth  
5 = deep technical investigation

Research considerations:
• Prioritize recent research and modern architectures
• Focus on implementation details and real systems
• Include performance, scalability, and security considerations
• Include both academic work and industry adoption
• Consider open-source ecosystems and tooling
• Identify benchmarks, datasets, and evaluations if relevant

IMPORTANT OUTPUT REQUIREMENTS:

You must return ONLY a valid JSON object.
Do NOT include explanations, markdown formatting, or extra text.
Do NOT wrap the JSON in code blocks.

Required JSON format:

{{
  "main_questions": [],
  "sub_topics": [],
  "search_strategies": [],
  "expected_sources": [],
  "research_depth": 0
}}

Example output:

{{
  "main_questions": [
    "What are the core architectural principles behind transformers?",
    "How are transformers optimized for large-scale training?",
    "What performance trade-offs exist between different transformer variants?"
  ],
  "sub_topics": [
    "Transformer architecture",
    "Training optimization techniques",
    "Hardware acceleration",
    "Scaling laws",
    "Real-world deployments"
  ],
  "search_strategies": [
    "Analyze recent ArXiv papers",
    "Study major GitHub implementations",
    "Review conference publications",
    "Examine industry engineering blogs"
  ],
  "expected_sources": [
    "ArXiv research papers",
    "GitHub repositories",
    "IEEE/ACM publications",
    "Conference proceedings",
    "Technical blog posts"
  ],
  "research_depth": 4
}}
"""
        
        plans = self.executor.executePrompt(system_prompt, user_prompt, 0.7, True)

        return plans