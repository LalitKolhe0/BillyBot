# chatbot.py
from langchain_ollama import OllamaLLM

SYSTEM_INSTRUCTION = (
    "You are an internal knowledge base assistant. Answer concisely using ONLY the provided policy "
    "context. If the answer is not in the context, say you don't know and suggest uploading more relevant documents."
)

def build_prompt(question: str, docs: list) -> str:
    context_pieces = []
    for i, d in enumerate(docs, start=1):
        src = d.metadata.get("source", f"doc{i}")
        context_pieces.append(f"[{src}]\n{d.page_content}")
    context = "\n\n---\n\n".join(context_pieces)
    prompt = (
        f"{SYSTEM_INSTRUCTION}\n\n"
        f"CONTEXT:\n{context}\n\n"
        f"QUESTION:\n{question}\n\n"
        "Answer briefly. At the end, list sources used."
    )
    return prompt


def answer_question(question: str, chroma_db, top_k: int = 4, model: str = "llama3", temperature: float = 0.0):
    docs = chroma_db.similarity_search(question, k=top_k)
    if not docs:
        return "No relevant documents found in the knowledge base."

    prompt = build_prompt(question, docs)
    llm = OllamaLLM(model=model, temperature=temperature)
    return llm.invoke(prompt)
