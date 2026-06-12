from mcp.server.fastmcp import FastMCP
from pydantic import Field
import logging

from services.session_store import SessionStore
from tools.anonymize import Anonymizer
from tools.deanonymize import Deanonymizer
from prompts.annonymize_prompt import build_anonymization_prompt;

mcp = FastMCP("mcp-anonymizer-for-session",
              instructions="Anonymizes data",
              debug=True,
              log_level="DEBUG",
              json_response=True)

logging.basicConfig(level=logging.DEBUG)
store = SessionStore()

anonymizer = Anonymizer(store)
deanonymizer = Deanonymizer(store)

@mcp.tool(
    name="anonymize_text",
    description="""
        Detects and anonymizes personally identifiable information (PII)
        such as names, email addresses, and ages from text.

        Returns anonymized text and a session ID that can later be used
        with deanonymize_text to restore the original values.
    """
)
def anonymize_text(
        text: str = Field(description="Input text containing names, emails, ages or other personally identifiable information to anonymize."),
        session_id: str | None = Field(
            description="Optional session identifier used to maintain consistent anonymization across multiple requests. If  omitted, a new session is created automatically.",
            default=None
        )):
    """Anonymizes the given text and stores token mappings in the session store."""

    logging.debug(f"Anonymizing text: {text} with session_id: {session_id}")
    result = anonymizer.anonymize(
        text=text,
        session_id=session_id,
    )
    logging.debug(f"Anonymization result: {result}")

    return {
        "anonymizedText": result.anonymized_text,
        "entities": [
            entity.__dict__
            for entity in result.entities
        ],
        "sessionId": result.session_id,
        "hasPii": result.hasPii
    }


@mcp.tool(
    name="deanonymize_text",
    description="""
    Restores original names, emails and other anonymized values
    using the session created by anonymize_text.

    Requires the session ID returned by the anonymization step.
    """,
)
def deanonymize_text(text: str = Field(description="The text to deanonymize"), session_id: str = Field(description="The session ID to retrieve token mappings")):
    """
    Restore anonymized text.
    """
    result, replacements = deanonymizer.deanonymize(
        text=text,
        session_id=session_id,
    )

    return {
        "deanonymizedText": result,
        "replacements": replacements,
    }


@mcp.tool(
    name="get_session_map",
    description="""
    Retrieves the mapping of anonymization tokens to their original values for a given session ID.

    This can be used for debugging or auditing purposes to see what real values correspond to each token.
    """,
)
def get_session_map(
    session_id: str = Field(description="The session ID to retrieve the token map for."),
):
    """
    Returns all anonymization token mappings
    for a session.
    """

    token_map = store.get(session_id)

    if not token_map:
        return {
            "sessionId": session_id,
            "entries": [],
        }

    entries = []

    for token, value in token_map.items():
        entries.append(
            {
                "token": token,
                "originalValue": value,
            }
        )

    return {
        "sessionId": session_id,
        "entries": entries,
    }


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


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
# if __name__ == "__main__":
#     mcp.run(transport="stdio")