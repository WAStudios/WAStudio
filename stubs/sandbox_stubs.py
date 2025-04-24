# stubs/sandbox_stubs.py

import random

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

    -- Stub flavor environment correctly before WeakAuras loads
    local flavorFromTocToNumber = {
      Vanilla = 1,
      TBC = 2,
      Wrath = 3,
      Cata = 4,
      Mainline = 10
    }
    
    -- Force Mainline flavor (Retail)
    _G.flavor = 10
    
    -- Stub C_AddOns.GetAddOnMetadata to avoid nil when retrieving "Version" or "X-Flavor"
    _G.C_AddOns = _G.C_AddOns or {}
    C_AddOns.GetAddOnMetadata = function(addon, field)
      if field == "Version" then
        return "Dev"
      elseif field == "X-Flavor" then
        return "Mainline"
      end
      return nil
    end
    
    -- Stub WeakAuras early, to avoid IsRetail() failing before definition
    _G.WeakAuras = _G.WeakAuras or {}
    WeakAuras.BuildInfo = 110000  -- Force TWW for later compatibility
    WeakAuras.IsRetail = function() return true end
    WeakAuras.IsClassicEra = function() return false end
    WeakAuras.IsCataClassic = function() return false end
    WeakAuras.IsClassicOrCata = function() return false end
    WeakAuras.IsCataOrRetail = function() return true end
    WeakAuras.IsTWW = function() return true end

    -- IsRetail global + local stub
    if not _G.IsRetail then
        local isRetailFunc = function()
            return true
        end
        _G.IsRetail = isRetailFunc
        IsRetail = isRetailFunc  -- Also in local/global for direct access
        print("IsRetail force-injected (global + local).")
    else
        print("IsRetail already exists.")
    end
    
    print("IsRetail (direct call):", IsRetail())
    print("_G.IsRetail (global call):", _G.IsRetail())

    -- SlashCmdList stub
    _G.SlashCmdList = _G.SlashCmdList or {}
    SlashCmdList = _G.SlashCmdList

    -- WeakAuras IsLibsOK stub
    WeakAuras.IsLibsOK = function() return true end
    WeakAuras.prettyPrint = function(msg) print("[WA]", msg) end
    WeakAuras.versionString = "WAStudioSim"

    UnitLevel = function(unit) return 80 end

    print("ExecEnv pre-load exists:", WeakAuras.ExecEnv ~= nil)

    _G.LDB = {
      NewDataObject = function(name, tbl)
        print("LDB.NewDataObject called with:", name)
        return tbl
      end
    }

    _G.L = _G.L or setmetatable({}, {
      __index = function(_, key)
        return key
      end
    })
    print("Localization table L stubbed.")
    """)

    # Lua-style random handling
    def lua_random(*args):
        if len(args) == 0:
            return random.random()
        elif len(args) == 1:
            return random.randint(1, args[0])
        elif len(args) == 2:
            return random.randint(args[0], args[1])
        else:
            raise ValueError("random() accepts 0, 1, or 2 arguments in Lua")

    lua_runtime.globals()['random'] = lua_random
    lua_runtime.globals()['math'] = {'random': lua_random, 'randomseed': random.seed}

    print("All critical WeakAuras-related stubs injected from sandbox_stubs.")