import re

from langchain.schema import Document
import urllib


def document_to_markdown_link(doc: Document):
    match = re.search("\((.*)\)", doc.metadata["source"])
    if match:
        docurl = match.group(1).replace(" ", "%20")
    else:
        docurl = ""
    return "[" + urllib.parse.unquote(doc.metadata["filename"]) + "](" + docurl + ")"
