# api_runtime/localization_api.py

def register_localization_api(lua):
    lua.execute("""
L = setmetatable({}, {
  __index = function(t, k)
    return k  -- fallback: return the key itself if not translated
  end
})
""")
    print("[WAStudio] Stubbed global localization table L with fallback")
