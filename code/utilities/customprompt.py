# flake8: noqa
from langchain.prompts import PromptTemplate

# CONDENSE_QUESTION_PROMPT 拷贝自 .venv/lib/python3.10/site-packages/langchain/chains/chat_vector_db/prompts.py
condense_question_prompt_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(condense_question_prompt_template)

# COMPLETION_PROMPT
completion_prompt_template = """{summaries}
Please reply to the question using only the information present in the text above. 
Include references to the sources you used to create the answer if those are relevant ("SOURCES"). 
If you can't find it, reply politely that the information is not in the knowledge base.
Reply in 中文
Question: {question}
Answer:"""

COMPLETION_PROMPT = PromptTemplate(template=completion_prompt_template, input_variables=["summaries", "question"])


# 未知用途
EXAMPLE_PROMPT = PromptTemplate(
    template="Content: {page_content}\nSource: {source}",
    input_variables=["page_content", "source"],
)


