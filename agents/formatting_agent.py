from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from core.config import settings

def formatting_node(state: dict) -> Dict[str, Any]:
    """
    Drafts the final, human-readable adjuster summary.
    """
    print("[Formatting Agent] Drafting final adjuster summary...")
    
    facts = state.get("extracted_facts")
    liability = state.get("liability_decision")
    
    llm = ChatOpenAI(model=settings.MODEL_REASONING, temperature=0.2)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an insurance assistant. Write a concise, professional 1-paragraph summary of the claim adjudication based on the facts and liability decision."),
        ("user", "Facts: {facts}\nLiability: {liability}")
    ])
    
    # Mocking LLM text output
    summary_text = (
        f"Based on the police report from {facts['date_of_loss']}, Driver B was found 100% at fault "
        f"for the collision involving Driver A. Driver B was issued citations for Speeding and Failure "
        f"to Yield, which serve as the primary contributing causes for the rear-end damage to Driver A's vehicle."
    )
    
    print("[Formatting Agent] Summary generated.")
    return {"final_summary": summary_text}