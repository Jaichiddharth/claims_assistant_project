from typing import Dict, Any

def supervisor_node(state: dict) -> Dict[str, Any]:
    """
    Evaluates the current state of the claim and determines the next required action.
    This node acts as the conditional logic engine for LangGraph routing.
    """
    print("[Supervisor] Assessing current claim state...")
    
    # Check if we have extracted the foundational facts yet
    if not state.get("extracted_facts"):
        print("[Supervisor] Missing facts. Routing to Extraction Agent.")
        return {"route_to": "extraction"}
        
    # Check if liability has been adjudicated
    if not state.get("liability_decision"):
        print("[Supervisor] Facts present, but missing liability. Routing to Liability Agent.")
        return {"route_to": "liability"}
        
    # If facts and liability are present, finish the process
    print("[Supervisor] Adjudication complete. Routing to Formatting Agent.")
    return {"route_to": "format"}