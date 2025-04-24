from get_dependencies import ensure_wa_repo, ensure_wase_repo
from stubs.libstub import inject_libstub
from stubs.wow_api import inject_wow_api
from stubs.weak_auras_private import inject_weak_auras_private
from stubs.addon_env import inject_addon_env
from stubs.sandbox_stubs import inject_sandbox_stubs

import sys
import os

# Ensure WASEngine is recognized properly in sys.path
wase_path = os.path.abspath("./WASEngine")
if wase_path not in sys.path:
    sys.path.insert(0, wase_path)

# Step 1: Ensure latest WeakAuras2 and WASEngine repos
ensure_wa_repo()
ensure_wase_repo()

# Import AFTER sys.path adjustment
from core.engine import WASEngine
from api.frames import Frame  # <-- Frame now imports cleanly

# --- Optional: Test the Frame is correct ---
test_frame_obj = Frame("TestFrameExpose")
print("Frame has SetAllPoints:", hasattr(test_frame_obj, "SetAllPoints"))

# Initialize WASEngine
engine = WASEngine()

test_frame = engine.api_create_frame("TestFrameCheck")
print("Frame has SetAllPoints:", hasattr(test_frame, "SetAllPoints"))

lua_runtime = engine.lua
lua_globals = lua_runtime.globals()

# Inject Stubs
inject_libstub(lua_runtime)
inject_wow_api(lua_runtime)
inject_weak_auras_private(lua_runtime)
inject_addon_env(lua_runtime)

# Step 4: Inject All Necessary Stubs for WeakAuras to Run
inject_sandbox_stubs(lua_runtime)

# Step 4: Load WeakAuras Files with Special Handling for WeakAuras.lua
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
            if file == "WeakAuras.lua":
                with open(full_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    pre_execenv = "".join(lines[:406])
                    post_execenv = "".join(lines[406:])

                    # Load part 1
                    lua_env.execute(pre_execenv)
                    print("WeakAuras.lua part 1 loaded (up to line 406)")

                    # Re-inject Private.ExecEnv
                    lua_env.execute("""
                    local Private = WeakAuras.Private
                    Private.ExecEnv = Private.ExecEnv or {}
                    local ExecEnv = Private.ExecEnv
                    WeakAuras.ExecEnv = ExecEnv
                    print("Rebinding ExecEnv from Private mid-load:", ExecEnv ~= nil)
                    
                    Private.frames = Private.frames or {}
                    WeakAuras.frames = Private.frames
                    print("Private.frames initialized mid-load:", Private.frames ~= nil)
                    """)

                    # Prepend locals for part 2
                    wrapped_post_execenv = f"""
local Private = WeakAuras.Private
local ExecEnv = Private.ExecEnv
{post_execenv}
"""
                    lua_env.execute(wrapped_post_execenv)
                    print("WeakAuras.lua part 2 loaded (after ExecEnv)")
            else:
                with open(full_path, "r", encoding="utf-8") as f:
                    lua_env.execute(f.read())
                    print(f"Loaded {file}")
        else:
            print(f"{file} not found!")

# Step 5: Load Lua Files
load_wa_lua_files(lua_runtime)

# Step 6: Trigger Addon Load Simulation
lua_globals.TriggerEvent("ADDON_LOADED", "WeakAuras")
lua_globals.TriggerEvent("PLAYER_LOGIN")

# Step 7: Let WASEngine process updates
engine.start_main_loop(duration=3)