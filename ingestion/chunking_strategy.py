import re
from typing import List, Dict, Any
from uuid import uuid4

class RAGChunker:
    def __init__(self):
        # Regex patterns to detect standard sections in a police report
        self.section_patterns = {
            "header": r"(?i)(date of accident|time|location|weather conditions)",
            "driver_a": r"(?i)(unit 1|vehicle 1|driver a)",
            "driver_b": r"(?i)(unit 2|vehicle 2|driver b)",
            "narrative": r"(?i)(officer narrative|description of events|summary)"
        }

    def structural_chunking(self, raw_text: str, claim_id: str) -> List[Dict[str, Any]]:
        """
        Splits the police report into its logical structural components.
        """
        chunks = []
        # In a production environment, this parsing logic would be more robust,
        # likely utilizing an LLM extraction pass or strict regex boundaries.
        # This is a simplified split based on double line breaks for demonstration.
        
        sections = re.split(r'\n\s*\n', raw_text)
        
        for section in sections:
            if not section.strip():
                continue
                
            chunk_type = self._classify_section(section)
            chunks.append({
                "chunk_id": str(uuid4()),
                "text": section.strip(),
                "metadata": {
                    "claim_id": claim_id,
                    "section_type": chunk_type,
                    "is_parent": True
                }
            })
            
        return chunks

    def parent_child_chunking(self, parent_chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Takes the structural parent chunks and breaks the dense narrative 
        down into sentence-level child chunks.
        """
        all_chunks = []
        
        for parent in parent_chunks:
            # Always keep the parent chunk in the database
            all_chunks.append(parent)
            
            # If the chunk is a narrative, generate child chunks (sentences)
            if parent["metadata"]["section_type"] == "narrative":
                # Basic sentence splitting (use NLTK or SpaCy for production)
                sentences = re.split(r'(?<=[.!?]) +', parent["text"])
                
                for sentence in sentences:
                    if len(sentence.strip()) > 10: # Ignore tiny fragments
                        all_chunks.append({
                            "chunk_id": str(uuid4()),
                            "text": sentence.strip(),
                            "metadata": {
                                "claim_id": parent["metadata"]["claim_id"],
                                "section_type": "narrative_child",
                                "is_parent": False,
                                "parent_id": parent["chunk_id"] # Link to parent
                            }
                        })
                        
        return all_chunks

    def _classify_section(self, text: str) -> str:
        """Helper to tag the chunk with its structural type."""
        text_lower = text.lower()
        for section_name, pattern in self.section_patterns.items():
            if re.search(pattern, text_lower):
                return section_name
        return "general"

    def process_document(self, raw_text: str, claim_id: str) -> List[Dict[str, Any]]:
        """Executes the full structural and parent-child chunking pipeline."""
        structural_parents = self.structural_chunking(raw_text, claim_id)
        final_chunks = self.parent_child_chunking(structural_parents)
        return final_chunks