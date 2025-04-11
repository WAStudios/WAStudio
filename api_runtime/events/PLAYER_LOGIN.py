# api_runtime/events/PLAYER_LOGIN.py

def handle_event(lua):
    """
    Simulates PLAYER_LOGIN — useful to initialize default states, if needed later.
    """
    print("[PLAYER_LOGIN] Player has logged in.")
