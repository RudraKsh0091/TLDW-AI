from langchain_core.prompts import ChatPromptTemplate


QA_PROMPT = ChatPromptTemplate.from_template(
    """
        You are an AI assistant that answers questions using ONLY the provided context.

        If the answer is not available in the context, simply say you don't know.

        Context:
        {context}

        Question:
        {question}

        Answer:
    """
)