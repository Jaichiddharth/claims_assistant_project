import boto3
import re
from typing import Dict, Any
from core.config import settings

class PoliceReportParser:
    def __init__(self):
        # Initialize AWS Textract client
        self.textract = boto3.client(
            'textract',
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

    def extract_text(self, file_bytes: bytes) -> str:
        """
        Calls AWS Textract to extract raw text from a document.
        Handles scanned PDFs and handwritten officer notes.
        """
        response = self.textract.detect_document_text(
            Document={'Bytes': file_bytes}
        )
        
        extracted_lines = []
        for item in response.get('Blocks', []):
            if item['BlockType'] == 'LINE':
                extracted_lines.append(item['Text'])
                
        raw_text = "\n".join(extracted_lines)
        
        if settings.ENABLE_PII_SCRUBBING:
            return self._scrub_pii(raw_text)
        return raw_text

    def _scrub_pii(self, text: str) -> str:
        """
        Replaces sensitive information with generic tokens to protect privacy
        and prevent the LLM from processing unmasked user data.
        """
        # Example Regex for standard US License Plates / SSNs / Phone Numbers
        # In production, use a robust library like Microsoft Presidio
        
        # Mask Phone Numbers
        text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE_NUMBER]', text)
        
        # Mask SSN
        text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN_REDACTED]', text)
        
        return text

    def parse_document(self, file_path: str) -> Dict[str, Any]:
        """Main pipeline to ingest a file and return scrubbed text."""
        with open(file_path, "rb") as document:
            file_bytes = document.read()
            
        clean_text = self.extract_text(file_bytes)
        
        return {
            "source_file": file_path,
            "parsed_text": clean_text,
            "status": "success"
        }