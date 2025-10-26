from decode_abstract import decode_abstract
from pyalex import config
import pyalex as px
import pandas as pd

px.config.email = "idiayeifeanyi@yahoo.com"
config.max_retries = 5
config.retry_backoff_factor = 0.1
config.retry_http_codes = [429, 500, 503]

def replication_doi_search(doi: str) -> pd.DataFrame:
    """
    Search for a replication DOI in OpenAlex and return the results as a Pandas DataFrame.

    Args:
        doi (str): The DOI to search for.

    Returns:
        pd.DataFrame: A Pandas DataFrame containing the search results.
    """
    try:
        search = px.Works().search(doi).get()
        title = []
        abstract = []
        authorships = []
        publication_year = []
        publication_date = []
        related_works = []
        referenced_works = []
        dois = []

        # extract the publication's metadata
        for s in search:
            title.append(s['title'])
            abstract.append(decode_abstract(s['abstract_inverted_index']))
            authorships.append(s['authorships'])
            publication_year.append(s['publication_year'])
            publication_date.append(s['publication_date'])
            related_works.append(s['related_works'])
            referenced_works.append(s['referenced_works'])
            dois.append(s['doi'])

      # store the metadata in a dictionary
        pubs = {
            "Title": title,
            "Abstract": abstract,
            "Authorships": authorships,
            "Publication Year": publication_year,
            "Publication Date": publication_date,
            "Related Works": related_works,
            "Referenced Works": referenced_works,
            "DOI": dois
        }

        # turn the dictionary into a pandas dataframe
        pubs_df = pd.DataFrame(pubs)

        return pubs_df

    except Exception as e:
        print(e)

if __name__ == "__main__":
    replication_doi_search("10.1002/acp.1376")
