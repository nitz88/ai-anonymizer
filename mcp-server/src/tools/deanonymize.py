from pydantic import Field
import logging
from services.deanonymize import Deanonymizer

def register(mcp, store):
    deanonymizer = Deanonymizer(store)

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

        logging.debug(f"Deanonymizing text: {text} with session_id: {session_id}")
        result, replacements = deanonymizer.deanonymize(
            text=text,
            session_id=session_id,
        )

        return {
            "deanonymizedText": result,
            "replacements": replacements,
        }