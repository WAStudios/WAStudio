# WAStudio/stubs/libstub.py

def inject_libstub(lua_runtime):
    lua_runtime.execute("""
    LibStub = LibStub or function(libname, silent)
        local libs = _G._Libs or {}
        _G._Libs = libs
        if not libs[libname] then
            libs[libname] = {
                Embed = function(self, target)
                    return target
                end
            }
        end
        return libs[libname]
    end
    """)
    print("LibStub injected.")
