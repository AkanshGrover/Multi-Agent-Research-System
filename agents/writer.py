from executor import Executor


class Writer:

    def __init__(self):
        self.executor = Executor()

    def write_paper(self, topic, plan, researched_info):

        system_prompt = """
You are a senior Computer Science research writer specializing in literature reviews and technical survey papers.

Your task is to convert structured research findings into a high-quality REVIEW PAPER.

The paper must resemble a formal academic survey or literature review used in:

• IEEE review papers
• ACM Computing Surveys
• graduate-level literature reviews
• technical whitepapers

Your goal is to synthesize research insights rather than simply describing them.

You must:

• organize prior research into logical categories
• compare different approaches
• highlight major research contributions
• identify gaps and limitations in the literature
• provide structured technical explanations

Do NOT hallucinate papers or references.

If the research data lacks specific citations, refer to the work conceptually.

Write clearly, formally, and technically.
"""

        system_prompt_alt = """
You are a senior Computer Science research writer specializing in literature reviews and technical survey papers.

Your task is to convert structured research findings into a high-quality REVIEW PAPER.

The paper must resemble a formal academic survey or literature review used in:

• IEEE review papers
• ACM Computing Surveys
• graduate-level literature reviews
• technical whitepapers

Your goal is to synthesize research insights rather than simply describing them.

You must:

• organize prior research into logical categories
• compare different approaches
• highlight major research contributions
• identify gaps and limitations in the literature
• provide structured technical explanations

When multiple approaches exist, compare them in terms of:

• methodology
• performance
• scalability
• limitations

When available in the research findings, discuss:

• system architectures
• real-world implementations
• benchmarks and performance
• engineering trade-offs
• deployment considerations

Base explanations strictly on the provided research evidence.

Do NOT hallucinate papers, citations, or systems.

If the research data lacks specific citations, refer to the work conceptually.

If research evidence is limited, explicitly acknowledge the limitation rather than inventing details.

Focus on synthesizing insights rather than listing facts.

Before writing the paper, internally determine a logical section structure based on the research findings.

Write clearly, formally, and technically in an academic survey style.
"""

        user_prompt = f"""
RESEARCH TOPIC
{topic}


RESEARCH PLAN
{plan}


SYNTHESIZED RESEARCH DATA
{researched_info}


TASK

Write a structured REVIEW PAPER.

The output must be formatted so that it can be easily converted into a Word document.


DOCUMENT STRUCTURE

Title

Abstract (200-300 words)

1 Introduction
Explain the importance of the topic and why it is being researched.

2 Technical Background
Explain the foundational concepts and historical development.

3 Literature Review
Organize prior work into logical categories based on research approaches.

Example:

3.1 Transformer Architectures  
3.2 Mixture-of-Experts Models  
3.3 Efficient Inference Methods  

Each subsection should:

• summarize important research contributions
• explain methodologies used
• discuss advantages and limitations

4 Comparative Analysis of Approaches

Compare major approaches.

Discuss:

• trade-offs
• scalability
• performance
• practical usability

5 Implementation and Practical Applications

Explain how the research is implemented in real systems.

Discuss frameworks, tools, and architectures.

6 Performance and Engineering Considerations

Discuss:

• computational cost
• scalability
• optimization techniques
• deployment constraints
• security considerations

7 Research Gaps and Future Directions

Identify open problems and emerging research opportunities.

8 Conclusion

Summarize the key insights of the review.

References

List major works mentioned in the review.


WRITING RULES

• Use numbered section headings
• Use subsections where appropriate
• Maintain academic tone
• Avoid bullet lists unless necessary
• Write continuous paragraphs
• Ensure logical transitions between sections


OUTPUT FORMAT

Return plain structured text.

Example:

Title: ...

Abstract: ...

1 Introduction

(text)

2 Technical Background

(text)

3 Literature Review

3.1 ...

(text)

3.2 ...

(text)

8 Conclusion

(text)

References

(text)


Do not include markdown code blocks.

Write the full paper now.
"""

        user_prompt_alt = """
RESEARCH TOPIC
{topic}

RESEARCH PLAN
{plan}

SYNTHESIZED RESEARCH DATA
{researched_info}

TASK

Write a structured REVIEW PAPER.

Target length: approximately 2500-3500 words.

Base the paper strictly on the synthesized research data.
Do not introduce external claims, papers, systems, or unsupported statements.

If the research data is incomplete, explicitly acknowledge the limitation rather than inventing information.

Synthesize and integrate the findings rather than listing sources sequentially.

The output must be formatted so that it can be easily converted into a Word document.

DOCUMENT STRUCTURE

Title

Abstract (200-300 words)

1 Introduction
Explain the importance of the topic and why it is being researched.

2 Technical Background
Explain foundational concepts and historical development.

3 Literature Review
Organize prior work into logical categories based on the research plan or major methodological approaches.

Example:

3.1 Transformer Architectures
3.2 Mixture-of-Experts Models
3.3 Efficient Inference Methods

Each subsection should:

• summarize important research contributions
• explain methodologies used
• discuss engineering approaches when relevant
• discuss advantages and limitations
• provide concrete technical examples when available

4 Comparative Analysis of Approaches

Compare major approaches.

Discuss:

• trade-offs
• scalability
• performance
• practical usability

5 Implementation and Practical Applications

Explain how the research is implemented in real systems.

Discuss frameworks, tools, architectures, and deployment considerations.

6 Performance and Engineering Considerations

Discuss:

• computational cost
• scalability
• optimization techniques
• deployment constraints
• security considerations

7 Research Gaps and Future Directions

Identify limitations of current research and highlight emerging opportunities.

8 Conclusion

Summarize the key insights of the review.

References

List major works mentioned in the review.

WRITING RULES

• Use numbered section headings
• Use subsections where appropriate
• Maintain an academic and technical tone
• Avoid bullet lists unless necessary
• Write continuous paragraphs
• Ensure logical transitions between sections
• Provide concrete technical examples when possible
• Explain engineering trade-offs between approaches
• Avoid unnecessary repetition
• Prioritize influential and recent research when synthesizing literature

OUTPUT FORMAT

Return plain structured text.

Example:

Title: ...

Abstract: ...

1 Introduction

(text)

2 Technical Background

(text)

3 Literature Review

3.1 ...

(text)

3.2 ...

(text)

4 Comparative Analysis of Approaches

(text)

5 Implementation and Practical Applications

(text)

6 Performance and Engineering Considerations

(text)

7 Research Gaps and Future Directions

(text)

8 Conclusion

(text)

References

(text)

Do not include markdown code blocks.

Do not use Markdown heading symbols (#).

Write the full paper now.
"""

        draft = self.executor.executePrompt(
            system_prompt,
            user_prompt,
            temperature=0.6,
            isJson=False
        )

        return draft#alt never worked coz limit got imposed, gonna check it first and then remove, for now it is just present there