# api_runtime/spell_api.py

def register_spell_api(lua):
    """
    Register GetSpellInfo(spellID or name) to simulate basic spell metadata.
    """

    # Fake spell database — this is just a starting point
    fake_spell_db = {
        133: {
            "name": "Fireball",
            "icon": "Interface\\Icons\\Spell_Fire_FlameBolt",
            "castTime": 2500,
            "minRange": 0,
            "maxRange": 40
        },
        116: {
            "name": "Frostbolt",
            "icon": "Interface\\Icons\\Spell_Frost_FrostBolt02",
            "castTime": 2000,
            "minRange": 0,
            "maxRange": 40
        }
    }

    def get_spell_info(spell_id_or_name):
        # Default values if we don’t find the spell
        spell = {
            "name": f"FakeSpell_{spell_id_or_name}",
            "icon": "Interface\\Icons\\INV_Misc_QuestionMark",
            "castTime": 0,
            "minRange": 0,
            "maxRange": 40
        }

        # If input is a number and we have a match
        if isinstance(spell_id_or_name, (int, float)):
            info = fake_spell_db.get(int(spell_id_or_name))
            if info:
                spell.update(info)

        # Return values in the order WoW expects
        return (
            spell["name"],
            None,               # rank — obsolete
            spell["icon"],
            spell["castTime"],
            spell["minRange"],
            spell["maxRange"]
        )

    lua.globals().GetSpellInfo = get_spell_info
