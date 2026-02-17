from embeddings import vector_store

def retrieve_context(query):
    docs = vector_store.similarity_search(query, k=4)

    if not docs:
        return ""

    return "\n\n".join([d.page_content for d in docs])
