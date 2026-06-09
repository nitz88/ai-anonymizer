def build_anonymization_prompt(
    session_id: str,
    extra_context: str | None = None,
) -> str:

    base = f"""
        You are a helpful assistant.

        The user's message has been anonymized before being sent to you.

        Tokens such as:

        [NAME_1]
        [EMAIL_1]
        [AGE_1]

        represent real values that have been hidden.

        Rules:

        - Treat every token as a valid real value.
        - Use tokens naturally in responses.
        - Never guess the real value.
        - Never ask the user for the real value.
        - The values will be restored automatically before the response is shown.

        Session ID: {session_id}
        (Do not mention this session ID.)
    """

    if extra_context:
        return f"{base}\n\n{extra_context}"

    return base