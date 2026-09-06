def invoke_with_retry(structured_llm, prompt: str):
    try:
        return structured_llm.invoke(prompt)
    except Exception:
        return structured_llm.invoke(
            prompt + "\n\nIMPORTANT: You must call the tool directly. Do not write prose. Keep all text fields under 25 words."
        )


def invoke_with_fallback(agent_role: str, schema, prompt: str):
    from app.llm.gateway import get_llm

    try:
        llm = get_llm(agent_role)
        structured_llm = llm.with_structured_output(schema)
        return invoke_with_retry(structured_llm, prompt)
    except Exception:
        groq_llm = get_llm(agent_role, provider_override="groq")
        groq_structured = groq_llm.with_structured_output(schema)
        return invoke_with_retry(groq_structured, prompt)