from __future__ import annotations
from enum import Enum, auto
from typing import Any
import log
import traceback

#log.Log.flags.add("EXCEPTION")
log.Log.flags.add("EVENT")

class Event:
    """Generic Event passed between blocks and nodes

    Typically contains data to pass down a chain
    
    field: t - type of event
    """
    t:T
    data:Any
    source:Widget|None
    dest:Widget

    class T(Enum):
        SEND = auto()
        RECV = auto()
        RESET = auto()

    def __init__(self, t, dest:Widget, data=None, source:Widget|None=None) -> None:
        self.t = t
        self.data = data
        self.source = source
        self.dest = dest
    
    def __str__(self) -> str:
        return f"<Event {self.t}: {self.source} -> {self.dest}, data={self.data}>"

class Widget:
    """
    Anything that can handle events
    """
    evlog = log.Log("EVENT")

    def handle(self, event:Event) -> None:
        self.evlog(event)
        
class Port:
    _val: Any
    _has: bool
    _repeat: bool

    def __init__(self, repeat:bool=False) -> None:
        self._val = None
        self._has = False
        self._repeat = repeat
    
    def has(self) -> bool:
        return self._has
    
    def get(self) -> Any:
        assert self._has
        if self._repeat:
            self._has = False
        return self._val
    
    def peek(self) -> Any|None:
        if self._has:
            return self._val
        else:
            return None
    
    def set(self, value:Any) -> None:
        assert not self._has
        self._has = True
        self._val = value
    
    def reset(self) -> None:
        self._val = None
        self._has = False

class InPort(Port):
    """
    Passes data into a block
    
    Receives from OutputNode
    """
    _link:OutPort|None

    def __init__(self, repeat: bool = False) -> None:
        super().__init__(repeat)
        self._link = None
    
    def try_pull(self) -> bool:
        assert not self.has()
        if self._link is not None:
            self._link.try_push()
    
class OutPort(Port):
    """
    Passes data out of a block
    
    Sends to InputNode(s)
    """
    _links:set[InPort]

    def __init__(self, repeat: bool = False) -> None:
        super().__init__(repeat)
        self._links = set()
    
    def link(self, target:InPort) -> None:
        assert target not in self._links
        assert target._link is None
        self._links.add(target)
        target._link = self
    
    def unlink(self, target:InPort) -> None:
        assert target in self._links
        assert target._link is self
        self._links.remove(target)
        target._link = None
    
    def unlink_all(self) -> None:
        for target in self._links:
            assert target._link is self
            target._link = None
        self._links = set()
    
    def try_push(self) -> bool:
        assert self.has()
        if (not self._repeat) or all((not dest.has() for dest in self._links)):
            v = self.get()
            for dest in self._links:
                dest.set(v)
            return True
        else:
            return False
        

class Node(Widget):
    inputs:dict[str, InPort]
    outputs:dict[str, OutPort]
    code:str

    exlog = log.Log("EXCEPTION")
    
    def __init__(self) -> None:
        super().__init__()
        self.inputs = {}
        self.outputs = {}
        self.code = str
    
    def handle(self, event:Event) -> None:
        super().handle(event)
    
    def run(self) -> None:
        exec_vars = {k:v.get() for k,v in self.inputs.items()}
        try:
            exec(self.code, globals(), exec_vars)
        except Exception:
            self.exlog(traceback.format_exc())

        for k,v in exec_vars.items():
            try:
                self.outputs[k].set(v)
            except KeyError:
                pass
        
class Scene():
    blocks:list[Node]
    
    def __init__(self) -> None:
        self.blocks = [basic_node_1i1o() for _ in range(3)]

def basic_node_1i1o():
    b = Node()
    b.inputs["i"] = InPort()
    b.outputs["o"] = OutPort()
    b.code = "o = i"
    return b