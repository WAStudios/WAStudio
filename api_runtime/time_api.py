# api_runtime/time_api.py

import time
import threading

# Used to track background threads started by C_Timer.After (for cleanup/testing)
_timer_threads = []

def register_time_api(lua):
    """
    Register simulated time-based API functions into the Lua runtime:
    - GetTime()
    - C_Timer.After()
    """
    # Simulate GetTime
    lua.globals().GetTime = lambda: time.time()

    # Simulate C_Timer.After
    def after(seconds, callback):
        def run():
            time.sleep(seconds)
            callback()
        thread = threading.Thread(target=run)
        thread.start()
        _timer_threads.append(thread)

    # Create the C_Timer table in Lua
    lua.execute("C_Timer = {}")
    lua.globals().C_Timer['After'] = after
888