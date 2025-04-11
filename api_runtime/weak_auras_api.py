# api_runtime/weak_auras_api.py

def register_weak_auras_api(lua):
    """
    Set up the global WeakAuras table that the addon attaches to.
    """
    # If WeakAuras doesn't exist, create an empty table
    lua.execute("WeakAuras = WeakAuras or {}")

    print("[WAStudio] Initialized global WeakAuras table")
