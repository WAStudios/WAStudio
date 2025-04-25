from get_dependencies import ensure_wa_repo
from stubs.libstub import inject_libstub
from stubs.wow_api import inject_wow_api
from stubs.weak_auras_private import inject_weak_auras_private
from stubs.addon_env import inject_addon_env
from stubs.sandbox_stubs import inject_sandbox_stubs
from wa_getlibs import getlibs
from wase_core.engine import WASEngine
from wase_api.math import register_math

import sys
import os
import glob

# Ensure WASEngine is recognized properly in sys.path
wase_path = os.path.abspath("./WASEngine")
if wase_path not in sys.path:
    sys.path.insert(0, wase_path)

# Step 1: Ensure latest WeakAuras2, WASEngine repos and WeakAuras Libraries
ensure_wa_repo()
#ensure_wase_repo()
getlibs()

# Initialize WASEngine
engine = WASEngine()
lua_runtime = engine.lua
lua_globals = lua_runtime.globals()

# Force-inject IsRetail
lua_runtime.execute("""
  _G.IsRetail = function() return true end
  IsRetail = _G.IsRetail
  """)

# Inject Stubs
inject_sandbox_stubs(lua_runtime)
inject_libstub(lua_runtime)
inject_wow_api(lua_runtime)
inject_weak_auras_private(lua_runtime)
inject_addon_env(lua_runtime)

lib_files = sorted(glob.glob('./libs/**/*.lua', recursive=True))
# Prioritize ChatThrottleLib if embedded
priority_files = [f for f in lib_files if 'ChatThrottleLib.lua' in f]
other_files = [f for f in lib_files if 'ChatThrottleLib.lua' not in f]

# Load Lua Files
for lib_file in priority_files + other_files:
    print(f"--- Checking math before loading {lib_file} ---")

    # Re-inject math to ensure it's available
    register_math(lua_runtime)

    try:
        print("math.min pre-load:", lua_runtime.execute("return math.min(5, 4)"))
    except Exception as e:
        print(f"math.min missing before {lib_file}: {e}")

    with open(lib_file, 'r', encoding='utf-8') as f:
        print(f"Loading {lib_file}...")
        lua_runtime.execute(f.read())

    print(f"--- Finished loading {lib_file} ---\n")


# Load WeakAuras Files with Special Handling for WeakAuras.lua
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

                    # Re-inject ExecEnv and frames
                    lua_env.execute("""
                    local Private = WeakAuras.Private
                    Private.ExecEnv = Private.ExecEnv or {}
                    local ExecEnv = Private.ExecEnv
                    WeakAuras.ExecEnv = ExecEnv

                    Private.frames = Private.frames or {}
                    WeakAuras.frames = Private.frames
                    """)

                    # Re-inject IsRetail before part 2
                    lua_env.execute("""
                    _G.IsRetail = function() return true end
                    IsRetail = _G.IsRetail
                    """)

                    # Load part 2
                    wrapped_post_execenv = f"""
                    local Private = WeakAuras.Private
                    local ExecEnv = Private.ExecEnv
                    {post_execenv}
                    """
                    lua_env.execute(wrapped_post_execenv)
            else:
                with open(full_path, "r", encoding="utf-8") as f:
                    lua_env.execute(f.read())
        else:
            print(f"{file} not found!")

# Load Lua Files
load_wa_lua_files(lua_runtime)

# Simulate Addon Load Events
lua_globals.TriggerEvent("ADDON_LOADED", "WeakAuras")
lua_globals.TriggerEvent("PLAYER_LOGIN")

# Let WASEngine process updates
engine.start_main_loop(duration=3)
