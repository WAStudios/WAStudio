# api_runtime/api_loader.py

# Priority bootstraps
from .libstub_api import register_libstub_api
from .localization_api import register_localization_api
from .addon_api import register_addon_api
from .chat_api import register_chat_api

# General APIs (keep alphabetical)
from .event_core import register_event_api
from .frame_api import register_frame_api
from .spell_api import register_spell_api
from .time_api import register_time_api
from .unit_api import register_unit_api
from .weak_auras_api import register_weak_auras_api

def build_blizzard_api(lua):
    """
    Register all stubbed Blizzard API functions into the Lua environment.
    Priority APIs are loaded first, followed by the rest in alphabetical order.
    """
    # Priority first
    register_libstub_api(lua)
    register_localization_api(lua)
    register_addon_api(lua)
    register_chat_api(lua)

    # General (alphabetical)
    register_event_api(lua)
    register_frame_api(lua)
    register_spell_api(lua)
    register_time_api(lua)
    register_unit_api(lua)
    register_weak_auras_api(lua)
