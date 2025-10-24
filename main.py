from extractor import classify_replication
from utils import build_reference_string, fetch_doi_metadata
from data.replication_study import ReplicationStudy
from fuzzywuzzy import fuzz


def extract_replication_study(replication_doi: str) -> ReplicationStudy:
    """
    Extracts replication and original study information from a replication DOI.
    
    Args:
        replication_doi: The DOI of the replication study
    
    Returns:
        ReplicationStudy object with all extracted information
    """
    # Fetch the replication study metadata
    replication_data = fetch_doi_metadata(replication_doi)
    if not replication_data or replication_data.get('status') != 'ok':
        print(f"Failed to fetch replication study: {replication_doi}")
        return None
    
    message = replication_data.get('message', {})
    
    # Build replication reference
    replication_reference = build_reference_string(message)
    replication_title = message.get('title', [''])[0] if message.get('title') else None
    abstract = message.get('abstract') if message.get('abstract') else None
    
    # Look through references to find the original study
    references = message.get('reference', [])
    original_doi = None
    original_reference = None
    original_title = None
    
    # Get the first reference with a DOI as the original paper
    for ref in references:
        if ref.get('DOI'):
            # Fetch metadata for this referenced DOI to get full details
            ref_doi = ref.get('DOI')
            ref_data = fetch_doi_metadata(ref_doi)
            
            if ref_data and ref_data.get('status') == 'ok':
                original_doi = ref_doi
                original_message = ref_data.get('message', {})
                original_reference = build_reference_string(original_message)
                original_title = original_message.get('title', [''])[0]
                break  # Take the first reference with a DOI
    
    return ReplicationStudy(
        replication_doi=replication_doi,
        replication_reference=replication_reference,
        original_doi=original_doi,
        original_reference=original_reference,
        replication_title=replication_title,
        original_title=original_title,
        abstract=abstract
    )


if __name__ == "__main__":
    replication_doi = "10.1371/journal.pone.0313619"
    
    print("Fetching replication study information...\n")
    study = extract_replication_study(replication_doi)
    
    if study:
        print("=== REPLICATION STUDY ===")
        print(f"DOI_r: {study.replication_doi}")
        print(f"Title_r: {study.replication_title}")
        print(f"Reference_r: {study.replication_reference}\n")
        print(f"DOI_o: {study.original_doi}")
        print(f"Title_o: {study.original_title}")
        print(f"Reference_o: {study.original_reference}\n")
        print(f"Abstract: {study.abstract}\n")
    else:
        print("Failed to extract replication study information")

    result = classify_replication(study.abstract)
    if result:
         print(f"Confidence: {result.confidence}\n")
         print(f"Outcome: {result.outcome}\n")
         print(f"Proof: {result.proof}\n")
         similarity = fuzz.token_set_ratio(result.proof, study.abstract)
         print(f"Similarity: {similarity}%")