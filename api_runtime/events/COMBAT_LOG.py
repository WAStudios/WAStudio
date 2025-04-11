# api_runtime/events/COMBAT_LOG.py

def handle_event(lua, *args):
    """
    Simulates COMBAT_LOG_EVENT_UNFILTERED — fires with 20+ arguments depending on event type.
    This just prints the event type and source/target info for now.
    """
    if not args:
        print("[COMBAT_LOG_EVENT_UNFILTERED] Fired with no arguments.")
        return

    subevent = args[0]
    sourceGUID = args[1]
    sourceName = args[2]
    destGUID = args[5]
    destName = args[6]

    print(f"[COMBAT_LOG] {subevent} | {sourceName} → {destName}")
