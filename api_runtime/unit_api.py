# api_runtime/unit_api.py

import time

def register_unit_api(lua):
    """
    Register unit-related API stubs:
    - UnitAura()
    - UnitExists()
    - UnitName()
    """
    # Simulate UnitAura - returns dummy aura data
    def unit_aura(unit, index):
        if unit == "player" and index == 1:
            return (
                "Example Buff",
                "Interface\\Icons\\Spell_Nature_Rejuvenation",
                1,          # count
                "Magic",    # debuffType
                10,         # duration
                time.time() + 10  # expiration
            )
        return None

    lua.globals().UnitAura = unit_aura

    # Simulate UnitExists
    lua.globals().UnitExists = lambda unit: unit in ("player", "target", "boss1")

    # Simulate UnitName
    lua.globals().UnitName = lambda unit: f"Unit_{unit}"