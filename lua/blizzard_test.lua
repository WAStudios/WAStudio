print("Blizzard API Test:")
print("Time:", GetTime())

C_Timer.After(2, function()
  print("This was printed after 2 seconds")
end)

local name, icon, count, debuffType, duration, expiration = UnitAura("player", 1)
print("Aura:", name, icon, count, debuffType, duration, expiration)