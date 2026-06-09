import secrets
import string

class SessionStore:
    def __init__(self):
        self._sessions: dict[str, dict[str, str]] = {}

    def get_or_create(self, session_id: str) -> dict[str, str]:
        if session_id not in self._sessions:
            self._sessions[session_id] = {}

        return self._sessions[session_id]

    def get(self, session_id: str) -> dict[str, str] | None:
        return self._sessions.get(session_id)

    def clear(self, session_id: str) -> bool:
        return self._sessions.pop(session_id, None) is not None

    def list_sessions(self) -> list[str]:
        return list(self._sessions.keys())
    
    @staticmethod
    def generate_session_id(
        length: int = 12,
    ) -> str:
        alphabet = (
            string.ascii_lowercase
            + string.digits
        )

        return "".join(
            secrets.choice(alphabet)
            for _ in range(length)
        )