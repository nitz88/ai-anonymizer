from dataclasses import dataclass
from typing import Literal

EntityType = Literal["NAME", "AGE", "EMAIL"]


@dataclass
class DetectedEntity:
    type: EntityType
    value: str
    token: str
    start: int
    end: int


@dataclass
class AnonymizeResult:
    anonymized_text: str
    entities: list[DetectedEntity]
    session_id: str
    hasPii: bool