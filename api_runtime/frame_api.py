# api_runtime/frame_api.py
from lupa import as_attrgetter

class FakeFrame:
    def __init__(self, frame_type, name=None, parent=None, template=None):
        self.frame_type = frame_type
        self.name = name or "UnnamedFrame"
        self.visible = False
        self.scripts = {}
        self.position = ("CENTER", 0, 0)
        self.size = (64, 64)
        print(f"[CreateFrame] Created: {self.name} ({self.frame_type})")

    def SetScript(self, event, func):
        self.scripts[event] = func
        print(f"[{self.name}] SetScript({event})")

    def Show(self):
        self.visible = True
        print(f"[{self.name}] Show()")

    def Hide(self):
        self.visible = False
        print(f"[{self.name}] Hide()")

    def SetPoint(self, point, relativeTo=None, relativePoint=None, x=0, y=0):
        self.position = (point, x, y)
        print(f"[{self.name}] SetPoint({point}, {x}, {y})")

    def SetSize(self, width, height):
        self.size = (width, height)
        print(f"[{self.name}] SetSize({width}, {height})")

    # Optional: log unimplemented calls to help during dev
    def __getattr__(self, item):
        def log_missing(*args, **kwargs):
            print(f"[{self.name}] Called missing method: {item}({args})")
        return log_missing


def register_frame_api(lua):
    def create_frame(frame_type, name=None, parent=None, template=None):
        frame = FakeFrame(frame_type, name, parent, template)
        return as_attrgetter(frame)  # We need to wrap FakeFrame in a Lua table, so Lua can access its methods the way it expects.

    lua.globals().CreateFrame = create_frame