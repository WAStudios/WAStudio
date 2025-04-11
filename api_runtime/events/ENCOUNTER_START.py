# api_runtime/events/ENCOUNTER_START.py

def handle_event(lua, encounterID, encounterName, difficultyID, groupSize):
    """
    Simulates logic that should occur when ENCOUNTER_START fires.
    This gets called by event_core.trigger_event().
    """
    print(f"[ENCOUNTER_START] Encounter started!")
    print(f"  ID: {encounterID}")
    print(f"  Name: {encounterName}")
    print(f"  Difficulty: {difficultyID}")
    print(f"  Group Size: {groupSize}")
