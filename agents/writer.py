from executor import Executor

class Writer:
    def __init__(self):
        self.executor = Executor()

    def write_paper(self, topic, plan, researched_info):
        system_prompt = """
You are a senior Computer Science and Information Technology technical writer.

Your role is to transform structured research data into a comprehensive, technically rigorous research report suitable for software engineers, researchers, and technical decision-makers.

You are part of a multi-agent research system. Your responsibility is to synthesize research findings into a coherent and authoritative report.

Your writing must prioritize:
• technical accuracy
• logical organization
• evidence-based explanations
• practical relevance
• clarity for technically literate readers

WRITING OBJECTIVES

1. Transform fragmented research findings into a clear technical narrative.
2. Organize information into logically structured sections.
3. Explain complex technical ideas clearly without oversimplifying them.
4. Highlight practical implementations, real systems, and engineering trade-offs.
5. Present multiple approaches when they exist and explain their differences.
6. Identify performance, scalability, and security implications.

TECHNICAL CONTENT EXPECTATIONS

The report should integrate information from:
• academic research papers
• open-source implementations
• engineering blog posts
• technical documentation
• conference papers
• real-world deployments and case studies

You must emphasize:
• system architectures
• algorithms and methods
• implementation techniques
• benchmarks and performance
• real-world engineering trade-offs
• production usage and tooling

WRITING STYLE

• precise and technically authoritative
• analytical rather than promotional
• objective and evidence-based
• clear section hierarchy
• professional tone suitable for engineers and researchers

IMPORTANT RULES

• Do NOT invent citations, papers, or repositories.
• If research evidence is limited, explain the limitation rather than hallucinating.
• Do NOT repeat the research plan verbatim.
• Focus on synthesizing insights rather than listing facts.
• Maintain strong logical flow between sections.

Before writing the report, internally determine the section structure based on the research plan and findings.

Your final output must be a well-structured technical report written in clear academic-style prose.
"""

        user_prompt = f"""
RESEARCH TOPIC
{topic}


RESEARCH PLAN
This plan defines the core research questions and investigation areas.

{plan}


SYNTHESIZED RESEARCH DATA
This data contains the gathered findings from multiple sources.

{researched_info}


TASK

Using the research plan and synthesized research data, write a comprehensive technical report about the topic.


REPORT REQUIREMENTS

Total length: 2500-3500 words.


REPORT STRUCTURE

Executive Summary (300-400 words)
Summarize the most important technical insights, major findings, and practical implications.

Technical Background (400-500 words)
Explain the technical context, foundational concepts, and historical evolution of the topic.

Main Technical Findings (1500-2000 words)
Organize this section into multiple subsections based on the research plan's main questions and subtopics.

Each subsection should include:
• explanation of the concept
• relevant research findings
• engineering approaches
• examples of real-world systems when available

Implementation and Practical Applications (400-600 words)
Explain how the technology or methods are implemented in real systems.
Discuss tools, frameworks, architectures, and deployment considerations.

Performance and Engineering Considerations (300-400 words)
Discuss performance characteristics, scalability challenges, optimization techniques, and security considerations.

Future Directions and Research Gaps (300-400 words)
Identify limitations of current approaches and highlight emerging research directions.


WRITING GUIDELINES

• Use clear technical headings and subheadings.
• Ensure smooth logical flow between sections.
• Provide concrete technical examples where possible.
• Explain trade-offs between different approaches.
• Discuss engineering constraints and practical limitations.
• Emphasize modern research and current implementations.
• Avoid unnecessary repetition.


TECHNICAL DEPTH EXPECTATION

The report should reflect the level of detail expected in:

• technical whitepapers
• engineering research reports
• advanced technical blog posts
• graduate-level CS literature reviews


OUTPUT FORMAT

Return the report as plain structured text with headings and subheadings.

Do NOT include markdown code blocks around the entire response.
Do NOT include explanations about the writing process.

Write the complete technical report now.
"""
        
        draft = self.executor.executePrompt(system_prompt, user_prompt, 0.7, False)
        return draft