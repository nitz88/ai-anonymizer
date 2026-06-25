from dataclasses import dataclass
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from models.entities import EntityType
from typing import List
from services.session_store import SessionStore
from mcp.server.fastmcp import FastMCP

import re

from models.entities import (
    DetectedEntity,
    AnonymizeResult,
    EntityType,
)

@dataclass
class RawMatch:
    type: str
    value: str
    index: int
    stored_value: str | None = None


class Anonymizer:

    def __init__(self, store: SessionStore):
        self.store = store
        configuration = {
            "nlp_engine_name": "spacy",
            "models": [
                {
                    "lang_code": "en",
                    "model_name": "en_core_web_lg"
                }
            ]
        }

        provider = NlpEngineProvider(
            nlp_configuration=configuration
        )

        nlp_engine = provider.create_engine()

        self.analyzer = AnalyzerEngine(
            nlp_engine=nlp_engine
        )

    

    def _detect_entities(self, text: str) -> list[RawMatch]:

        results = self.analyzer.analyze(
            text=text,
            language="en"
        )

        matches: list[RawMatch] = []

        entity_map = {
            "PERSON": "NAME",
            "EMAIL_ADDRESS": "EMAIL",
            "PHONE_NUMBER": "PHONE",
            "CREDIT_CARD": "CREDIT_CARD",
            "LOCATION": "LOCATION",
            "AGE": "AGE"
        }

        for r in results:

            entity_type = entity_map.get(r.entity_type)

            if entity_type is None:
                continue

            value = text[r.start:r.end]

            matches.append(
                RawMatch(
                    type=entity_type,
                    value=value,
                    stored_value=value,
                    index=r.start,
                )
            )

        matches.sort(key=lambda x: x.index)

        deduped: list[RawMatch] = []
        last_end = -1

        for m in matches:

            end = m.index + len(m.value)

            if m.index >= last_end:
                deduped.append(m)
                last_end = end

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
            key = value.strip().lower()
            reverse_map[key] = token

        counters = {
            "NAME": 0,
            "AGE": 0,
            "EMAIL": 0,
            "PHONE": 0,
            "LOCATION": 0,
            "CREDIT_CARD": 0
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

                if match.type not in counters:
                    counters[match.type] = 0

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