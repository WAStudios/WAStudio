-- lua/frame_test.lua
local f = CreateFrame("Frame", "TestFrame")
f:SetScript("OnUpdate", function() print("Updating...") end)
f:SetPoint("CENTER", nil, nil, 100, 50)
f:SetSize(120, 40)
f:Show()