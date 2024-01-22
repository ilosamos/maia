"""Embedding search using OpenAI API."""
import openai
import numpy as np

from maia.utils.ml import cosine_similarity
from settings import OPENAI_EMBEDDING_MODEL


def embedding_search(data: list, search_term: str) -> str:
    """Perform embedding search using simple string list and search term."""
    data.append(search_term)

    embeddings_response = openai.embeddings.create(
        input=data,
        model=OPENAI_EMBEDDING_MODEL
    )

    embeddings = embeddings_response.data
    search_term_embedding = embeddings[-1].embedding
    embeddings.pop()

    similarities = [cosine_similarity(search_term_embedding, dat.embedding) for dat in embeddings]
    return np.argmax(similarities)
