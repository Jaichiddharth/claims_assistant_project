from pydantic import BaseModel, Field
from typing import List

class InvolvedParty(BaseModel):
    driver_type: str = Field(description="'Insured' or 'Third-Party'")
    vehicle_damage_points: List[str] = Field(description="Areas of vehicle damaged")
    citations_issued: List[str] = Field(description="Specific citations, e.g., 'Failure to Yield'")

class ExtractedFacts(BaseModel):
    date_of_loss: str
    jurisdiction_state: str = Field(default="IL", description="State where the accident occurred")
    parties: List[InvolvedParty]
    weather_conditions: str
    officer_narrative_summary: str