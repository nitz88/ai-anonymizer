from pydantic import Field
from .annonymize_prompt import build_anonymization_prompt

def register_prompts(mcp):
    @mcp.prompt(
        name="anonymize_before_send",
        description="""
        Builds a prompt to instruct the model to use anonymized tokens
        naturally in its responses without asking for the real values.
        """,
    )
    def anonymize_before_send(
        session_id: str = Field(description="The session ID to include in the prompt for context."),
        extra_context: str | None = Field(description="Optional additional context to include in the prompt.", default=None),
    ):
        return build_anonymization_prompt(
            session_id=session_id,
            extra_context=extra_context,
        )