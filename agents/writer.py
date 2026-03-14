# from executor import Executor


# class Writer:

#     def __init__(self):
#         self.executor = Executor()

#     def build_references(self, researched_info):
#         references = []

#         papers = researched_info.get("literature_sources", [])

#         for paper in papers:

#             title = paper.get("title", "Unknown Title")
#             authors = paper.get("authors", [])
#             year = paper.get("year", "Unknown Year")

#             if isinstance(authors, list):
#                 authors = ", ".join(authors)

#             ref = f"{authors} ({year}). {title}."
#             references.append(ref)

#         if not references:
#             return ["No explicit references were available from the analyzed research sources."]

#         return references
    
#     def write_section(self, topic, plan, researched_info, section_title):

#         system_prompt = """
# You are a senior Computer Science research writer specializing in literature reviews and technical survey papers.

# Your task is to write a detailed section of an academic review paper.

# The paper should resemble publications from:

# • IEEE review papers
# • ACM Computing Surveys
# • graduate-level literature reviews
# • technical whitepapers

# Your writing must:

# • synthesize research insights rather than list facts
# • explain technical concepts clearly
# • analyze methodologies and approaches
# • discuss advantages, limitations, and trade-offs
# • maintain academic tone and structure
# • provide technical depth suitable for a research audience

# Do NOT hallucinate papers, systems, or evidence.

# Use only the research information provided.
# """

#         user_prompt = f"""
# RESEARCH TOPIC
# {topic}

# RESEARCH PLAN
# {plan}

# SYNTHESIZED RESEARCH DATA
# {researched_info}

# SECTION TO WRITE
# {section_title}

# TASK

# Write ONLY this section of the review paper.

# Guidelines:

# • Write 800-1200 words
# • Use multiple paragraphs
# • Maintain an academic research tone
# • Explain technical ideas clearly
# • Integrate insights from the research data
# • Discuss engineering trade-offs when relevant
# • Provide deep explanations rather than short summaries

# Do NOT write other sections.

# Return plain text only.
# """

#         return self.executor.executePrompt(
#             system_prompt,
#             user_prompt,
#             temperature=0.6,
#             isJson=False
#         )

#     def write_abstract(self, topic, researched_info):

#         system_prompt = """
# You are a computer science research writer.

# Write a high-quality academic abstract for a literature review paper.
# """

#         user_prompt = f"""
# TOPIC
# {topic}

# RESEARCH DATA
# {researched_info}

# Write a 200-250 word academic abstract.

# The abstract should:

# • summarize the research domain
# • describe the scope of the review
# • highlight major research themes
# • briefly mention challenges and future directions

# Return plain text only.
# """

#         return self.executor.executePrompt(
#             system_prompt,
#             user_prompt,
#             temperature=0.5,
#             isJson=False
#         )

#     def write_paper(self, topic, plan, researched_info):

#         sections = [
#             "1 Introduction",
#             "2 Technical Background",
#             "3 Literature Review",
#             "4 Comparative Analysis of Approaches",
#             "5 Implementation and Practical Applications",
#             "6 Performance and Engineering Considerations",
#             "7 Research Gaps and Future Directions",
#             "8 Conclusion"
#         ]

#         paper_parts = []

#         # Title
#         paper_parts.append(f"Title: A Comprehensive Review of {topic}\n")

#         # Abstract
#         abstract = self.write_abstract(topic, researched_info)
#         paper_parts.append(f"Abstract:\n{abstract}\n")

#         # Sections
#         for section in sections:
#             print(f"Writing section: {section}")
#             content = self.write_section(topic, plan, researched_info, section)

#             #paper_parts.append(f"{section}\n")
#             paper_parts.append(content)
#             paper_parts.append("\n")

#         references = self.build_references(researched_info)
#         paper_parts.append("References\n")
#         for ref in references:
#             paper_parts.append(ref + "\n")

#         return "\n".join(paper_parts)


from executor import Executor


class Writer:

    def __init__(self):
        self.executor = Executor()


    def build_references(self, researched_info):
        references = []

        papers = researched_info.get("literature_sources", [])

        for i, paper in enumerate(papers, start=1):

            title = paper.get("title", "Unknown Title")
            authors = paper.get("authors", [])
            year = paper.get("year", "Unknown Year")

            if isinstance(authors, list):
                authors = ", ".join(authors)

            ref = f"[{i}] {authors} ({year}). {title}."
            references.append(ref)

        if not references:
            references.append("[1] No explicit references were available from the analyzed research sources.")

        return references


    def write_section(self, topic, plan, researched_info, section_title, references, feedback=None):

        reference_list = "\n".join(references)

        feedback_text = feedback if feedback else "No reviewer feedback provided."

        system_prompt = """
You are a senior Computer Science research writer specializing in literature reviews and technical survey papers.

Your task is to write a detailed section of an academic review paper.

The paper should resemble publications from:

• IEEE review papers
• ACM Computing Surveys
• graduate-level literature reviews
• technical whitepapers

Your writing must:

• synthesize research insights rather than list facts
• explain technical concepts clearly
• analyze methodologies and approaches
• discuss advantages, limitations, and trade-offs
• maintain academic tone and structure
• provide technical depth suitable for a research audience

Use citation numbers like [1], [2], [3] when referring to sources.

Do NOT hallucinate papers or citations.

Use only the provided research information and reference list.
"""

        user_prompt = f"""
RESEARCH TOPIC
{topic}

RESEARCH PLAN
{plan}

AVAILABLE REFERENCES
{reference_list}

SYNTHESIZED RESEARCH DATA
{researched_info}

REVIEWER FEEDBACK (if any)
{feedback_text}

If reviewer feedback is provided, revise the section accordingly.
Address the issues mentioned while preserving correct analysis.

SECTION TO WRITE
{section_title}

TASK

Write ONLY this section of the review paper.

Guidelines:

• Write 800-1200 words
• Use multiple paragraphs
• Maintain academic research tone
• Explain technical ideas clearly
• Integrate insights from the research data
• Cite sources using numbers like [1], [2], etc when relevant
• Discuss engineering trade-offs when relevant
• Provide deep explanations rather than short summaries

Do NOT write other sections.

Return plain text only.
"""

        return self.executor.executePrompt(
            system_prompt,
            user_prompt,
            temperature=0.6,
            isJson=False
        )


    def write_abstract(self, topic, researched_info):

        system_prompt = """
You are a computer science research writer.

Write a high-quality academic abstract for a literature review paper.
"""

        user_prompt = f"""
TOPIC
{topic}

RESEARCH DATA
{researched_info}

Write a 200-250 word academic abstract.

The abstract should:

• summarize the research domain
• describe the scope of the review
• highlight major research themes
• briefly mention challenges and future directions

Return plain text only.
"""

        return self.executor.executePrompt(
            system_prompt,
            user_prompt,
            temperature=0.5,
            isJson=False
        )


    def write_paper(self, topic, plan, researched_info, feedback=None):

        sections = [
            "1 Introduction",
            "2 Technical Background",
            "3 Literature Review",
            "4 Comparative Analysis of Approaches",
            "5 Implementation and Practical Applications",
            "6 Performance and Engineering Considerations",
            "7 Research Gaps and Future Directions",
            "8 Conclusion"
        ]

        paper_parts = []

        # Title
        paper_parts.append(f"Title: A Comprehensive Review of {topic}\n")

        # Abstract
        abstract = self.write_abstract(topic, researched_info)
        paper_parts.append(f"Abstract:\n{abstract}\n")

        # Build references
        references = self.build_references(researched_info)

        # Sections
        for section in sections:
            print(f"Writing section: {section}")

            content = self.write_section(
                topic,
                plan,
                researched_info,
                section,
                references,
                feedback
            )

            paper_parts.append(content)
            paper_parts.append("\n")

        # References
        paper_parts.append("References\n")
        for ref in references:
            paper_parts.append(ref + "\n")

        return "\n".join(paper_parts)