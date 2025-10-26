def decode_abstract(inv_index: str) -> str:
    """
    Decodes an abstract from an inverted index.

    Args:
      inv_index: The inverted index to decode.

    Returns:
        Decoded abstract text.
    """
    if not isinstance(inv_index, dict):
        return None
    words = sorted([(pos, word) for word, positions in inv_index.items() for pos in positions])
    return " ".join(word for _, word in words)
