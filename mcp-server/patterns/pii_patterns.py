import re

EMAIL_PATTERN = re.compile(
    r"\b[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}\b"
)

NAME_FORMAL_PATTERN = re.compile(
    r"\b(?:(?:Mr\.?|Mrs\.?|Ms\.?|Dr\.?|Prof\.?)\s+[A-Z][a-zA-Z'-]+(?:\s+[A-Z][a-zA-Z'-]+)*|[A-Z][a-z][a-zA-Z'-]*(?:\s+[A-Z][a-z][a-zA-Z'-]+)+)\b"
)

NAME_CONTEXT_PATTERN = re.compile(
    r"\b(?:my\s+name\s+is|i\s+am|i'm|this\s+is|call\s+me|hi\s*[,!]?\s*i'?m)\s+([a-zA-Z][a-zA-Z'-]{1,})\b",
    re.IGNORECASE,
)

AGE_PATTERN = re.compile(
    r"\b(?:"
    r"age(?:d)?\s+(?:is\s+)?(?P<num1>\d{1,3})"
    r"|"
    r"(?P<num2>\d{1,3})\s*[-]?\s*(?:years?|yrs?)(?:\s*[-]?\s*old)?"
    r")\b",
    re.IGNORECASE,
)