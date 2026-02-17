# Simple in-memory session storage

memory_store = {}

def save_memory(session_id, message):
    if session_id not in memory_store:
        memory_store[session_id] = []
    memory_store[session_id].append(message)

def load_memory(session_id):
    return memory_store.get(session_id, [])
