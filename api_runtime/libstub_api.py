# api_runtime/libstub_api.py

def register_libstub_api(lua):
    """
    Stub LibStub to return dummy addon libraries when requested.
    """

    # Dummy library registry
    fake_libs = {}

    # Simulate LibStub() global
    def lib_stub(name, silent=False):
        if name in fake_libs:
            return fake_libs[name]

        # If it's new, create a dummy table for it
        lib = {
            "dummy": True,
            "libName": name,
            "Embed": lambda *args: print(f"[LibStub:{name}] Embed({', '.join(str(arg) for arg in args)})")
        }

        # You can pre-define dummy functions for common libraries
        if name == "AceAddon-3.0":
            lib["NewAddon"] = lambda *args, **kwargs: {
                "name": args[0],
                "dummyAddon": True,
                "RegisterEvent": lambda *a: None,
                "UnregisterEvent": lambda *a: None,
                "RegisterChatCommand": lambda *a: None,
            }

        if name == "CustomNames":

            def get_custom_name(key):
                print(f"[CustomNames] Get('{key}') → '{key}' (stubbed)")
                return key  # Return key as dummy name

            lib["Get"] = get_custom_name

            # https://warcraft.wiki.gg/wiki/API_UnitName
            def get_unit_name(unitID):
                print(f"[CustomNames] UnitName('{unitID}') → '{unitID}' (stubbed)")
                return unitID

            lib["UnitName"] = get_unit_name

            # https://warcraft.wiki.gg/wiki/API_UnitName#GetUnitName
            def get_get_unit_name(unit):
                print(f"[CustomNames] GetUnitName('{unit}') → '{unit}' (stubbed)")
                return unit

            lib["GetUnitName"] = get_get_unit_name

            # https://warcraft.wiki.gg/wiki/API_UnitName
            def get_unit_full_name(unit):
                print(f"[CustomNames] UnitFullName('{unit}') → '{unit}' (stubbed)")
                return unit

            lib["UnitFullName"] = get_unit_full_name



        if not silent:
            print(f"[LibStub] Returning fake library: {name}")

        fake_libs[name] = lib
        return lib

    # Register the global LibStub function
    lua.globals().LibStub = lib_stub
