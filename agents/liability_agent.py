from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from core.config import settings
from tools.ragretriever import retrieve_case_precedents
from tools.policylookup import lookup_traffic_code

def liability_node(state: dict) -> Dict[str, Any]:
    """
    Determines fault by comparing extracted facts against traffic laws and policy guidelines.
    """
    print("[Liability Agent] Adjudicating fault...")
    
    facts = state.get("extracted_facts", {})
    jurisdiction = facts.get("jurisdiction_state", "IL")
    
    # 1. Tool Execution: Look up local laws based on citations
    laws = []
    for party in facts.get("parties", []):
        for citation in party.get("citations_issued", []):
            laws.append(lookup_traffic_code(citation, jurisdiction))
            
    # 2. Tool Execution: RAG retrieval for similar past claims
    # Querying the vector DB using the synthesized facts
    context = retrieve_case_precedents(str(facts), state.get("claim_id"))
    
    llm = ChatOpenAI(model=settings.MODEL_REASONING, temperature=0.0)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Liability Claims Adjuster. Determine fault strictly based on the provided facts and legal codes. You must append citation source IDs to your reasoning."),
        ("user", "Facts: {facts}\n\nApplicable Laws: {laws}\n\nRAG Precedents: {context}")
    ])
    
    # Mocking LLM output
    mock_decision = {
        "primary_fault_attributed_to": "Driver B",
        "liability_split": {"Driver B": 100, "Driver A": 0},
        "primary_contributing_cause": "Speeding (Excessive Speed)",
        "confidence_score": 0.96
    }
    
    print(f"[Liability Agent] Fault determined: {mock_decision['primary_fault_attributed_to']} (Confidence: {mock_decision['confidence_score']})")
    
    # Update state with the liability decision and the RAG context used
    return {
        "liability_decision": mock_decision,
        "rag_context": context + laws
    }