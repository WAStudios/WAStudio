-- Create a frame for both events
local f = CreateFrame("Frame", "TestEvents")

f:RegisterEvent("ENCOUNTER_START")
f:RegisterEvent("COMBAT_LOG_EVENT_UNFILTERED")
f:RegisterEvent("PLAYER_LOGIN")

f:SetScript("OnEvent", function(self, event, ...)
  print("Lua OnEvent triggered:", event, ...)
end)
