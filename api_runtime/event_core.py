# api_runtime/event_core.py

from .events import ENCOUNTER_START, COMBAT_LOG, PLAYER_LOGIN
from .frame_api import FakeFrame

# Stores which frames are listening for which events
registered_event_frames = {}

# Event dispatcher registry
event_handlers = {
    "ENCOUNTER_START": ENCOUNTER_START.handle_event,
    #"COMBAT_LOG_EVENT_UNFILTERED": COMBAT_LOG.handle_event,
    #"PLAYER_LOGIN": PLAYER_LOGIN.handle_event,
}

def register_event(frame, event_name):
    print(f"[{frame.name}] Registered for event: {event_name}")
    registered_event_frames.setdefault(event_name, []).append(frame)

def unregister_event(frame, event_name):
    print(f"[{frame.name}] Unregistered from event: {event_name}")
    if event_name in registered_event_frames:
        registered_event_frames[event_name] = [
            f for f in registered_event_frames[event_name] if f != frame
        ]

def trigger_event(lua, event_name, *args):
    frames = registered_event_frames.get(event_name, [])
    print(f"[WAStudio] Triggering event: {event_name} on {len(frames)} frames")

    for frame in frames:
        handler = frame.scripts.get("OnEvent")
        if handler:
            try:
                handler(frame, event_name, *args)
            except Exception as e:
                print(f"[{frame.name}] OnEvent error: {e}")

    # Optional event logic (e.g., debug triggers)
    if event_name in event_handlers:
        event_handlers[event_name](lua, *args)

def register_event_api(lua):
    """
    Called from api_loader.py — patches FakeFrame with event methods
    """
    setattr(FakeFrame, "RegisterEvent", lambda self, event: register_event(self, event))
    setattr(FakeFrame, "UnregisterEvent", lambda self, event: unregister_event(self, event))

    print("[WAStudio] Event system initialized.")
