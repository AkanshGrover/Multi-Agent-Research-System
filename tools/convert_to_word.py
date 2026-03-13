from docx import Document

def convert_word(text, topic):
    doc = Document()

    lines = text.split("\n")

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.startswith("Title:"):
            doc.add_heading(line.replace("Title:", "").strip(), level=0)

        elif line.startswith("Abstract"):
            doc.add_heading("Abstract", level=1)

        elif line[0].isdigit() and " " in line:
            doc.add_heading(line, level=1)

        elif line[:3].count(".") == 1:
            doc.add_heading(line, level=2)

        elif line.lower().startswith("references"):
            doc.add_heading("References", level=1)

        else:
            doc.add_paragraph(line)

        doc.save(f"{topic}_review_paper.docx")