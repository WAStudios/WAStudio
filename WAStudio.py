# WAStudio/WAStudio.py

from get_dependencies import ensure_wa_repo, ensure_wase_repo
import sys
import os

# Step 1: Ensure latest WeakAuras2 and WASEngine
ensure_wa_repo()
ensure_wase_repo()

# Step 2: Add local WASEngine to Python path
wase_path = os.path.abspath("./WASEngine")
if wase_path not in sys.path:
    sys.path.append(wase_path)

from core.engine import WASEngine

# Step 3: Initialize WASEngine
engine = WASEngine()
lua_runtime = engine.lua
lua_globals = lua_runtime.globals()

# Step 4: Bootstrap Required WoW Globals for WeakAuras
lua_runtime.execute("""
WeakAuras = WeakAuras or {}
function GetAddOnMetadata(addon, field)
    return "FakeMetaData"
end
function IsAddOnLoaded(addon)
    return true
end
""")

# Step 5: Load WeakAuras Lua Files
def load_wa_lua_files(lua_env, base_path="WeakAuras2/WeakAuras"):
    lua_files = [
        "WeakAuras.lua",
        "Transmission.lua",
        "Core.lua",
        "RegionTypes/init.lua"
    ]

    for file in lua_files:
        full_path = os.path.join(base_path, file)
        if os.path.exists(full_path):
            with open(full_path, "r", encoding="utf-8") as f:
                lua_env.execute(f.read())
                print(f"Loaded {file}")
        else:
            print(f"{file} not found!")

load_wa_lua_files(lua_runtime)

# Step 6: Trigger Addon Load Simulation
lua_globals.TriggerEvent("ADDON_LOADED", "WeakAuras")
lua_globals.TriggerEvent("PLAYER_LOGIN")

# Step 7: Let WASEngine process updates
engine.start_main_loop(duration=3)