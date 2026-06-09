import re

from services.session_store import SessionStore


class Deanonymizer:
    def __init__(self, store: SessionStore):
        self.store = store

    def deanonymize(
        self,
        text: str,
        session_id: str,
    ) -> tuple[str, int]:

        token_map = self.store.get(session_id)

        if not token_map:
            return text, 0

        replacements = 0
        result = text

        for token, original_value in token_map.items():
            count = result.count(token)

            if count:
                replacements += count
                result = result.replace(
                    token,
                    original_value,
                )

        return result, replacements