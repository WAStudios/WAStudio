# weakauras_patcher.py
import re

debug_statements = False

def patch_varargs(lua_lines):
    """
    Scans through each line of Lua source code and removes unsafe top-level uses of `...` (varargs).

    Problem:
      In normal Lua addons (like WeakAuras), it's common to write:
          local addonName, Private = ...
      or:
          local Private = select(2, ...)

      These are fine in WoW's environment, but they are illegal outside of a vararg function
      (i.e., in a top-level `lua.execute()` context).

    Solution:
      We strip those specific lines out to avoid Lua syntax errors.
      For all other lines that contain `...`, we emit warnings for the user,
      as they may still cause issues in some contexts.
    """
    filtered = []

    for line in lua_lines:
        # Match lines like: `local addonName, Private = ...` or `local AddonName = ...`
        ellipsis_assign = re.search(r"local\s+\w+(,\s*\w+)?\s*=\s*\.\.\.", line)

        # Match lines like: `local Private = select(2, ...)`
        ellipsis_select = "select(2, ...)" in line

        if ellipsis_assign or ellipsis_select:
            if debug_statements:
                print("[WAStudio][Patch] Removed top-level ellipsis line:", line.strip())
            continue  # Skip this unsafe line entirely

        if "..." in line:
            if debug_statements:
                print("[WAStudio][Warning] Line still contains ellipsis (possibly unsafe):", line.strip())

        filtered.append(line)

    return filtered


def inject_wrapper(lua_code):
    """
    Wraps the full Lua source code into a named function called `WAStudio_Loader`.

    Why:
      Lua top-level code like WeakAuras.lua is not meant to run directly.
      We need to wrap it inside a named function so we can invoke it safely with:
          lua.execute(...)
          lua.globals().WAStudio_Loader("WeakAuras", Private)

    Notes:
      - `addonName` and `Private` are standard arguments passed by WoW in real addons.
      - We reintroduce `L` from the global environment (_G) to avoid nil access errors.
    """
    return (
            "function WAStudio_Loader(addonName, Private)\n"
            "  local L = _G and _G.L or {}\n"
            + indent_lua_code(lua_code) +
            "\nend"
    )


def indent_lua_code(code):
    """
    Indents every line of code by 2 spaces to nest it properly inside the WAStudio_Loader function.

    This avoids syntax issues and keeps structure clear.
    """
    return "\n".join("  " + line for line in code.splitlines())

