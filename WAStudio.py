from get_dependencies import ensure_wa_repo, ensure_wase_repo
from stubs.libstub import inject_libstub
from stubs.wow_api import inject_wow_api
from stubs.weak_auras_private import inject_weak_auras_private
from stubs.addon_env import inject_addon_env
import sys
import os

# Ensure dependencies
ensure_wa_repo()
ensure_wase_repo()

# Import WASEngine
wase_path = os.path.abspath("./WASEngine")
if wase_path not in sys.path:
    sys.path.append(wase_path)
from core.engine import WASEngine

# Initialize WASEngine
engine = WASEngine()
lua_runtime = engine.lua
lua_globals = lua_runtime.globals()

# Inject Stubs
#inject_libstub(lua_runtime)
#inject_wow_api(lua_runtime)
#inject_weak_auras_private(lua_runtime)
#inject_addon_env(lua_runtime)


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