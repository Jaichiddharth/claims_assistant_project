import json
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from core.config import settings
# Assuming ExtractedFacts is your Pydantic model defined in core/models.py
# from core.models import ExtractedFacts 

def extraction_node(state: dict) -> Dict[str, Any]:
    """
    Parses the raw OCR text into structured JSON.
    """
    print("[Extraction Agent] Initiating data mining on raw text...")
    
    raw_text = state.get("raw_text", "")
    
    # Initialize the LLM and bind the Pydantic schema for strict JSON output
    llm = ChatOpenAI(model=settings.MODEL_EXTRACTION, temperature=0.1)
    # structured_llm = llm.with_structured_output(ExtractedFacts) # Uncomment when Pydantic model is imported
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert data extraction algorithm. Extract the required entities from the following police report. If data is missing, output 'UNKNOWN'."),
        ("user", "{raw_text}")
    ])
    
    # Mocking the LLM execution for the pipeline
    # response = structured_llm.invoke(prompt.format_prompt(raw_text=raw_text))
    
    mock_facts = {
        "date_of_loss": "2026-08-01",
        "jurisdiction_state": "IL",
        "parties": [
            {"role": "Driver B", "vehicle": "Honda Accord", "citations_issued": ["Failure to Yield", "Speeding"]},
            {"role": "Driver A", "vehicle": "Toyota Camry", "citations_issued": []}
        ]
    }
    
    print("[Extraction Agent] Facts extracted successfully.")
    # Returns a dictionary that LangGraph will merge into the global ClaimState
    return {"extracted_facts": mock_facts}