def build_prompt(question: str, chunks: list[dict]) -> str:
    context = ""
    for chunk in chunks:

        context += (
            f"\n[{chunk['chunk_id']}]\n"
            f"{chunk['content']}\n"
        )

    prompt = f"""
        You are a computational biology research assistant.

        Answer the question using ONLY the supplied context.

        Rules:
        1. Do not use external knowledge.
        2. Do not invent facts.
        3. If context is insufficient, say so.
        4. Cite the chunk IDs supporting your answer.
        5. Return valid JSON only.

        Context:
        {context}

        Question:
        {question}

        Required JSON format:

        {{
            "answer": "Your answer",
            "citations": ["chunk_001", "chunk_002"]
        }}
        """

    return prompt