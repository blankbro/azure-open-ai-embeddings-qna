import re

from langchain.schema import Document


def document_to_markdown_link(doc: Document):
    match = re.search("\((.*)\)", doc.metadata["source"])
    if match:
        docurl = match.group(1).replace(" ", "%20")
    else:
        docurl = ""
    return "[" + doc.metadata["filename"] + "](" + docurl + ")"
