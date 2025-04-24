# WAStudio/WAStudio.py

from core.engine import WASEngine
from get_wa import ensure_wa_repo
import os

# Step 1: Ensure latest WeakAuras2
ensure_wa_repo()

# Step 2: Initialize WASEngine
engine = WASEngine()
lua = engine.lua.globals()

# Step 3: Load WeakAuras.lua
wa_lua_file = os.path.join("WeakAuras2", "WeakAuras", "WeakAuras.lua")
if os.path.exists(wa_lua_file):
    with open(wa_lua_file, "r", encoding="utf-8") as f:
        lua.execute(f.read())
        print("WeakAuras.lua loaded.")
else:
    print("WeakAuras.lua not found!")

# Step 4: Trigger Addon Load Simulation
lua.TriggerEvent("ADDON_LOADED", "WeakAuras")
lua.TriggerEvent("PLAYER_LOGIN")

# Step 5: Let WASEngine process updates for a bit
engine.start_main_loop(duration=3)
