# stubs/sandbox_stubs.py

def inject_sandbox_stubs(lua_runtime):
    lua_runtime.execute("""
    -- WeakAuras + Private globals
    _G.WeakAuras = _G.WeakAuras or {}
    WeakAuras = _G.WeakAuras
    _G.Private = WeakAuras.Private
    WeakAuras.Private = WeakAuras.Private or {}
    WeakAuras.L = WeakAuras.L or {}
    WeakAuras.ExecEnv = WeakAuras.ExecEnv or {}

    -- select(2, ...) environment simulation
    select = function(index, ...)
        if index == 2 then
            return WeakAuras.Private
        end
        return nil
    end

    -- C_AddOns stub
    _G.C_AddOns = _G.C_AddOns or {}
    C_AddOns = _G.C_AddOns
    C_AddOns.IsAddOnLoaded = function(name) return true end
    C_AddOns.LoadAddOn = function(name) return true end
    
    function IsRetail()
        return true  -- WAStudio emulates Retail for now
    end

    -- SlashCmdList stub
    _G.SlashCmdList = _G.SlashCmdList or {}
    SlashCmdList = _G.SlashCmdList

    -- WeakAuras IsLibsOK stub
    WeakAuras.IsLibsOK = function() return true end

    -- WeakAuras basic methods stub
    WeakAuras.prettyPrint = function(msg) print("[WA]", msg) end
    WeakAuras.versionString = "WAStudioSim"

    -- UnitLevel stub
    UnitLevel = function(unit) return 80 end

    -- ExecEnv Debug
    print("ExecEnv pre-load exists:", WeakAuras.ExecEnv ~= nil)
    
    random = random or function(a, b)
      if not a then
        return math.random()
      elseif not b then
        return math.random(a)
      else
        return math.random(a, b)
      end
    end

    _G.LDB = {
      NewDataObject = function(name, tbl)
        print("LDB.NewDataObject called with:", name)
        return tbl
      end
    }

    _G.L = _G.L or setmetatable({}, {
      __index = function(_, key)
        return key  -- fallback: return key as string
      end
    })
    print("Localization table L stubbed.")


    """)
    print("All critical WeakAuras-related stubs injected from sandbox_stubs.")
