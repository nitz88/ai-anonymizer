from pydantic import Field
import logging
from services.anonymize import Anonymizer

def register(mcp, store):
    anonymizer = Anonymizer(store)

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