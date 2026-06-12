from dataclasses import dataclass
import re

from models.entities import (
    DetectedEntity,
    AnonymizeResult,
    EntityType,
)

from patterns.pii_patterns import (
    EMAIL_PATTERN,
    NAME_FORMAL_PATTERN,
    NAME_CONTEXT_PATTERN,
    AGE_PATTERN,
)

from services.session_store import SessionStore


@dataclass
class RawMatch:
    type: EntityType
    value: str
    index: int
    stored_value: str | None = None


class Anonymizer:

    def __init__(self, store: SessionStore):
        self.store = store

    def _detect_entities(
        self,
        text: str,
    ) -> list[RawMatch]:

        matches: list[RawMatch] = []

        # EMAIL

        for match in EMAIL_PATTERN.finditer(text):
            matches.append(
                RawMatch(
                    type="EMAIL",
                    value=match.group(0),
                    stored_value=match.group(0),
                    index=match.start(),
                )
            )

        # FORMAL NAME

        for match in NAME_FORMAL_PATTERN.finditer(text):
            value = match.group(0).strip()

            matches.append(
                RawMatch(
                    type="NAME",
                    value=value,
                    stored_value=value,
                    index=match.start(),
                )
            )

        # CONTEXT NAME

        for match in NAME_CONTEXT_PATTERN.finditer(text):

            name_word = match.group(1)

            name_index = (
                match.start()
                + match.group(0).rfind(name_word)
            )

            matches.append(
                RawMatch(
                    type="NAME",
                    value=name_word,
                    stored_value=name_word,
                    index=name_index,
                )
            )

        # AGE

        for match in AGE_PATTERN.finditer(text):

            numeric_age = (
                match.groupdict().get("num1")
                or match.groupdict().get("num2")
            )

            if not numeric_age:
                continue

            age_start = (
                match.start() +
                match.group(0).find(numeric_age)
            )

            matches.append(
                RawMatch(
                    type="AGE",
                    value=numeric_age,
                    stored_value=numeric_age,
                    index=age_start,
                )
            )

        matches.sort(key=lambda x: x.index)

        deduped: list[RawMatch] = []

        last_end = -1

        for item in matches:

            current_end = (
                item.index + len(item.value)
            )

            if item.index >= last_end:
                deduped.append(item)
                last_end = current_end

        return deduped

    def anonymize(
        self,
        text: str,
        session_id: str | None = None,
        hasPii: bool = False
    ) -> AnonymizeResult:
        
        session_id = (
            session_id
            or self.store.generate_session_id()
        )

        token_map = self.store.get_or_create(
            session_id
        )

        reverse_map: dict[str, str] = {}

        for token, value in token_map.items():
            reverse_map[value.lower()] = token

        counters = {
            "NAME": 0,
            "AGE": 0,
            "EMAIL": 0,
        }

        token_pattern = re.compile(
            r"^\[([A-Z]+)_(\d+)\]$"
        )

        for token in token_map.keys():

            match = token_pattern.match(token)

            if not match:
                continue

            entity_type = match.group(1)
            number = int(match.group(2))

            if (
                entity_type in counters
                and number > counters[entity_type]
            ):
                counters[entity_type] = number

        raw_matches = self._detect_entities(text)

        entities: list[DetectedEntity] = []

        result = text

        for match in reversed(raw_matches):

            normalized = match.value.lower()

            if normalized in reverse_map:

                token = reverse_map[normalized]

            else:

                counters[match.type] += 1

                token = (
                    f"[{match.type}_"
                    f"{counters[match.type]}]"
                )

                value_to_store = (
                    match.stored_value
                    or match.value
                )

                token_map[token] = value_to_store

                reverse_map[normalized] = token

            before = result[: match.index]

            after = result[
                match.index + len(match.value) :
            ]

            result = before + token + after

            entities.insert(
                0,
                DetectedEntity(
                    type=match.type,
                    value=match.value,
                    token=token,
                    start=match.index,
                    end=(
                        match.index
                        + len(match.value)
                    ),
                ),
            )

        return AnonymizeResult(
            anonymized_text=result,
            entities=entities,
            session_id=session_id,
            hasPii=len(entities) > 0
        )