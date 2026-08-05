# Pseudocode for Qdrant Hybrid Search

def search_claim_context(query: str, claim_id: str):
    # 1. Generate Dense Vector for semantic meaning (e.g., "who is at fault")
    query_vector = embedding_model.embed(query)
    
    # 2. Generate Sparse Vector (BM25) for exact keyword matches (e.g., "Citation #1234")
    sparse_vector = bm25_encoder.encode(query)
    
    # 3. Execute Hybrid Query with hard metadata filtering
    results = qdrant_client.search(
        collection_name="police_reports",
        query_vector=query_vector,
        query_sparse=sparse_vector,
        query_filter={"claim_id": claim_id}, # HARD FILTER: Never mix claim data
        limit=5
    )
    
    return [hit.payload["text"] for hit in results]