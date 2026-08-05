from typing import TypedDict, List
from core.models import ExtractedFacts, LiabilityDecision

class ClaimState(TypedDict):
    claim_id: str
    raw_text: str
    extracted_facts: ExtractedFacts | None
    rag_context: List[str]
    liability_decision: LiabilityDecision | None
    final_summary: str | None
    errors: List[str]