print("Testing LibStub...")

local AceAddon = LibStub("AceAddon-3.0")
local addon = AceAddon.NewAddon("MyAddon")
addon:RegisterEvent("PLAYER_LOGIN")