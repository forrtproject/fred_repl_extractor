from enum import Enum
from urllib.parse import quote
import requests

class SOURCE(Enum):
    CROSS_REF = 1
    OPEN_ALEX = 2


def fetch_doi_metadata(doi: str, source: SOURCE = SOURCE.CROSS_REF) -> dict:
    """Fetches metadata for a given DOI from the Crossref API."""
    encoded_doi = quote(doi, safe='')
    url = ""
    if source == SOURCE.CROSS_REF:
        url = f'https://api.crossref.org/works/{encoded_doi}'
    else:
        url = f'https://api.openalex.org/works/https://doi.org/{encoded_doi}' 
    headers = {'accept': 'application/json'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching DOI {doi}: {e}")
        return None
    

def build_reference_string(message: dict) -> str:
    """Build a human-readable reference string from work data."""
    
    # Extract authors
    authors = message.get('author', [])
    author_str = ', '.join([f"{a.get('family', '')} {a.get('given', '')}" 
                            for a in authors[:3]])  # First 3 authors
    if len(authors) > 3:
        author_str += " et al."
    
    # Extract title
    title = message.get('title', [''])[0] if message.get('title') else ''
    
    # Extract year
    issued = message.get('issued', {}).get('date-parts', [[]])[0]
    year = issued[0] if issued else 'n.d.'
    
    # Extract journal and volume/issue/pages
    container_title = message.get('container-title', [''])[0] if message.get('container-title') else ''
    volume = message.get('volume', '')
    issue = message.get('issue', '')
    page = message.get('page', '')
    
    # Build reference
    ref = f"{author_str} ({year}). {title}. {container_title}"
    if volume:
        ref += f", {volume}"
    if issue:
        ref += f"({issue})"
    if page:
        ref += f", {page}"
    ref += "."
    
    return ref


