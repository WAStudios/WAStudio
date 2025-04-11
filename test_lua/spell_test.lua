print("Testing GetSpellInfo:")
local name, rank, icon, castTime, minRange, maxRange = GetSpellInfo(133)
print("Spell:", name, icon, castTime, minRange, maxRange)