# WAStudio.py - Loads and simulates the WeakAuras2 Lua addon inside a Python sandbox using Lupa

import os
import traceback
from lupa import LuaRuntime
from api_runtime.api_loader import build_blizzard_api
from weakauras_manager import clone_or_update_weakauras
from weakauras_patcher import patch_varargs, inject_wrapper

debug_statements = False

def main():
    if debug_statements:
        print("[WAStudio] Starting WAStudio runtime...")

    # --- STEP 1: Sync or clone the WeakAuras GitHub repo ---
    try:
        clone_or_update_weakauras()
        if debug_statements:
            print("[WAStudio] WeakAuras2 repository is up-to-date.")
    except Exception:
        if debug_statements:
            print("[WAStudio][ERROR] Failed to update WeakAuras2 repo:")
        traceback.print_exc()
        return

    # --- STEP 2: Start the Lua runtime environment ---
    lua = LuaRuntime(unpack_returned_tuples=True)

    # --- STEP 3: Register stubbed Blizzard APIs (C_AddOns, SlashCmdList, etc.) ---
    try:
        build_blizzard_api(lua)
        if debug_statements:
            print("[WAStudio] Blizzard API loaded.")
    except Exception:
        if debug_statements:
            print("[WAStudio][ERROR] Blizzard API init failed:")
        traceback.print_exc()

    # --- STEP 4: Stub the global localization table `L` and inject it into `_G` ---
    try:
        lua.execute("""
        -- Fallback localization table: any missing key returns itself
        L = setmetatable({}, {
          __index = function(t, k)
            return k
          end
        })
        -- Ensure _G exists and contains reference to L
        if _G == nil then _G = {} end
        _G.L = L
        """)
        if debug_statements:
            print("[WAStudio] Stubbed global localization table L and injected into _G.")
    except Exception:
        if debug_statements:
            print("[WAStudio][ERROR] Failed to stub global L:")
        traceback.print_exc()

    # --- STEP 5: Stub the WeakAuras global and mark libraries as OK ---
    try:
        lua.execute("if not WeakAuras then WeakAuras = {} end")
        lua.globals().WeakAuras["IsLibsOK"] = lambda: True
        if debug_statements:
            print("[WAStudio] Stubbed WeakAuras and IsLibsOK.")
    except Exception:
        if debug_statements:
            print("[WAStudio][ERROR] Failed to stub WeakAuras:")
        traceback.print_exc()

    # --- STEP 6: Create the shared 'Private' table to mimic real addon environments ---
    try:
        private_table = lua.table()
        lua.globals().Private = private_table
        if debug_statements:
            print("[WAStudio] Created Private table.")
    except Exception:
        if debug_statements:
            print("[WAStudio][ERROR] Failed to create Private table:")
        traceback.print_exc()

    # --- STEP 7: Load and preprocess WeakAuras.test_lua ---
    wa_main_path = os.path.join("WeakAuras2", "WeakAuras", "WeakAuras.test_lua")
    if not os.path.exists(wa_main_path):
        if debug_statements:
            print("[WAStudio][ERROR] WeakAuras.test_lua not found.")
        return

    try:
        # Read the full source code from the WeakAuras main Lua file
        with open(wa_main_path, "r", encoding="utf-8") as f:
            if debug_statements:
                print("[WAStudio] Reading WeakAuras.test_lua...")
            wa_lines = f.readlines()

        # Strip unsupported top-level vararg lines (e.g., `local AddonName = ...`)
        wa_lines = patch_varargs(wa_lines)
        wa_code_cleaned = "".join(wa_lines)

        # Wrap the cleaned source into a function body that can be executed
        # This includes handling of `local L = _G.L or {}` inside the function
        inner_body = inject_wrapper(wa_code_cleaned)

        # Final named function wrapper to assign to `WAStudio_Loader`
        full_wrapper = (
            "function WAStudio_Loader(addonName, Private)\n"
            "  local L = _G and _G.L or {}\n"  # Re-inject L in function scope
            f"{inner_body}\n"
            "end"
        )

        # Compile the function into the Lua runtime
        if debug_statements:
            print("[WAStudio] Compiling WAStudio_Loader...")
        lua.execute(full_wrapper)

        # Call it with addon name + shared Private table
        if debug_statements:
            print("[WAStudio] Executing WAStudio_Loader...")
        lua.globals().WAStudio_Loader("WeakAuras", private_table)

        if debug_statements:
            print("[WAStudio] ✅ Execution finished successfully.")

    except Exception:
        if debug_statements:
            print("[WAStudio][FATAL ERROR] Exception during execution:")
        traceback.print_exc()


# Entry point for standalone script execution
if __name__ == "__main__":
    main()