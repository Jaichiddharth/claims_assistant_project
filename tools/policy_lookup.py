def lookup_traffic_code(citation_string: str, state_code: str) -> str:
    """
    Looks up specific statutory rules based on the citation text.
    """
    print(f"  [Tool: PolicyLookup] Fetching statutes for '{citation_string}' in {state_code}...")
    
    # Mocking a database/API lookup for traffic codes
    statute_db = {
        "IL": {
            "Speeding": "625 ILCS 5/11-601: No vehicle may be driven upon any highway of this State at a speed which is greater than is reasonable and proper.",
            "Failure to Yield": "625 ILCS 5/11-904: Driver approaching a stop sign shall yield the right-of-way to any vehicle in the intersection."
        }
    }
    
    state_laws = statute_db.get(state_code, {})
    
    # Simple keyword match for demonstration
    for key, statute in state_laws.items():
        if key.lower() in citation_string.lower():
            return f"Statute Match: {statute}"
            
    return "No exact statute match found in local database."