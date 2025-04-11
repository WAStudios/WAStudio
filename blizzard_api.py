# blizzard_api.py

import time
import threading

# Store timers so we can simulate C_Timer.After()
_timer_threads = []

def build_blizzard_api(lua):
    # Simulate GetTime
    lua.globals().GetTime = lambda: time.time()

    # Simulate print
    lua.globals().print = print

    # Simulate C_Timer.After
    def after(seconds, callback):
        def run():
            time.sleep(seconds)
            callback()
        thread = threading.Thread(target=run)
        thread.start()
        _timer_threads.append(thread)

    lua.execute("C_Timer = {}")  # Create C_Timer table
    lua.globals().C_Timer['After'] = after

    # Simulate UnitAura - returns dummy aura data
    def unit_aura(unit, index):
        if unit == "player" and index == 1:
            # Simulate: name, icon, count, debuffType, duration, expirationTime
            return ("Example Buff", "Interface\\Icons\\Spell_Nature_Rejuvenation", 1, "Magic", 10, time.time() + 10)
        return None

    lua.globals().UnitAura = unit_aura

    # TODO: Add more stubs as needed (UnitExists, CreateFrame, etc.)
