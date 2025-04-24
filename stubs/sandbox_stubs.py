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
    _G.StaticPopupDialogs = _G.StaticPopupDialogs or {}
    StaticPopupDialogs = _G.StaticPopupDialogs

    math = math or {}
    math.min = math.min or function(a, b) if a < b then return a else return b end end
    math.max = math.max or function(a, b) if a > b then return a else return b end end
    math.floor = math.floor or function(x) return x - (x % 1) end
    math.ceil = math.ceil or function(x) if x % 1 == 0 then return x else return x - (x % 1) + 1 end end
    math.abs = math.abs or function(x) if x < 0 then return -x else return x end end
    _G.math = math


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
    C_AddOns.GetAddOnMetadata = function(addon, field)
        if field == "Version" then
            return "Dev"
        elseif field == "X-Flavor" then
            return "Mainline"
        end
        return nil
    end

    -- Force Mainline flavor (Retail)
    _G.flavor = 10

    -- WeakAuras flavor detection stubs
    WeakAuras.BuildInfo = 110000
    WeakAuras.IsRetail = function() return true end
    WeakAuras.IsClassicEra = function() return false end
    WeakAuras.IsCataClassic = function() return false end
    WeakAuras.IsClassicOrCata = function() return false end
    WeakAuras.IsCataOrRetail = function() return true end
    WeakAuras.IsTWW = function() return true end

    if not _G.IsRetail then
        local isRetailFunc = function() return true end
        _G.IsRetail = isRetailFunc
        IsRetail = isRetailFunc
    end

    -- SlashCmdList stub
    _G.SlashCmdList = _G.SlashCmdList or {}
    SlashCmdList = _G.SlashCmdList

    -- WeakAuras misc stubs
    WeakAuras.IsLibsOK = function() return true end
    WeakAuras.prettyPrint = function(msg) print("[WA]", msg) end
    WeakAuras.versionString = "WAStudioSim"

    UnitLevel = function(unit) return 80 end

    _G.LDB = {
        NewDataObject = function(name, tbl)
            return tbl
        end
    }

    _G.L = _G.L or setmetatable({}, {
        __index = function(_, key)
            return key
        end
    })
    """)

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
