# api_runtime/chat_api.py

def register_chat_api(lua):
    # Define the SlashCmdList table globally
    lua.execute("SlashCmdList = {}")

    # Optional: simulate SLASH_* constants (if needed later)
    lua.execute("SLASH_WEAKAURAS1 = '/wa'")
    lua.execute("SLASH_WEAKAURAS2 = '/weakauras'")

    print("[WAStudio] Stubbed SlashCmdList and basic slash aliases")
