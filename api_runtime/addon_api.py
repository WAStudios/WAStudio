# api_runtime/addon_api.py

def register_addon_api(lua):
    def is_addon_loaded(name):
        print(f"[C_AddOns] IsAddOnLoaded('{name}') → true")
        return True

    lua.execute("C_AddOns = {}")
    lua.globals().C_AddOns["IsAddOnLoaded"] = is_addon_loaded

    print("[WAStudio] Stubbed C_AddOns.IsAddOnLoaded")
