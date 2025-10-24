from dotenv import load_dotenv
# import google.generativeai as genai
from google import genai
from dataclasses import dataclass
from enum import Enum
import os
from pydantic import BaseModel

class ReplicationOutcome(Enum):
    """Enum for replication outcomes"""
    SUCCESSFUL = "successful"
    FAILED = "failed"
    MIXED = "mixed"


class ReplicationClassification(BaseModel):
    """Data model for replication classification result"""
    outcome: ReplicationOutcome
    confidence: str  # high, medium, low
    proof: str

load_dotenv()

def classify_replication(
    replication_abstract: str
) -> ReplicationClassification:
    """
    Uses Google Gemini to classify if a replication was successful, failed, or mixed.
    
    Args:
        api_key: Google Gemini API key
        replication_abstract: The abstract of the replication study
        original_study_title: The title of the original study being replicated
    
    Returns:
        ReplicationClassification object with outcome and reasoning
    """
    
    # Create the prompt
    prompt = f"""You are an expert in research methodology and replication studies. 
Analyze the following replication abstract and determine whether the replication study was successful, failed, or mixed in its outcomes.

REPLICATION STUDY ABSTRACT:
{replication_abstract}

Based on only this abstract, determine:

1. OUTCOME: Was the replication successful, failed , or mixed?
    success when the authors interpret their replication as successful (e.g., “we successfully replicated…”)
    failure when the authors interpret their replication as unsuccessful (e.g., “we failed to replicate…”)
    mixed when the authors describe their results as mixed or as a partial replication. If they report a detail that was diffferent but still conclude success or failure overall, then the outcome should be success or failure. You must trust them on the overall judgement.

2. CONFIDENCE: How confident are you in this classification? (high/medium/low)

3. PROOF: The exact text in the abstract that validates that it was successful, failed or mixed
"""
    
    try:
        client = genai.Client()
        response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config={
            'response_mime_type': 'application/json',
            'response_schema': ReplicationClassification,
        },
        )

        return response.parsed
    except:
        print(f"Error calling Gemini API: {e}")
        return None
    

if __name__ == "__main__":
    
    # Example data
    original_title = "Further Analysis of the Response Deprivation Hypothesis: Application of the Disequilibrium Model to Novel Clinical Contexts"
    
    replication_abstract = """
    Response disequilibrium theory suggests that a response deficit in a contingent activity (e.g., iPad time) 
    can increase engage- ment in an instrumental activity (e.g., work completion) to access the contingent activity. The 
    purpose of the current study was to conduct a systematic replication of Falligant and Rooker The Psychological Record, 
    71, 307-311, (2021) to further demonstrate the generality and applicability of this approach in clinical contexts. 
    Results of the current study align with prior research demonstrating the ability of the disequilibrium approach to 
    quantify the magnitude and direction of predicted change in instrumental activities based on measures of free operant baseline 
    responding. We discuss study findings from a practical standpoint and offer recommendations for future research on the use of 
    response disequilibrium theory for increas- ing instrumental activities in clinical practice and research.
    """
    
    print("Classifying replication study...")
    result = classify_replication(replication_abstract, original_title)
    if not result:
        print("Failed to classify replication")
    else:
        print("\n" + "="*60)
        print("REPLICATION CLASSIFICATION RESULT")
        print("="*60)
        print(f"Outcome: {result.outcome.value.upper()}")
        print(f"Confidence: {result.confidence}")
        print(f"\nProof:")
        print(f"  {result.proof}")
        print("="*60 + "\n")