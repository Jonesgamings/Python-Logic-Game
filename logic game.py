import time

POWER = "POWER"
UNPOWER = "UNPOWER"
OUTPUT = "OUTPUT"
INPUT = "INPUT"

class ID:

    ids = 0

    @classmethod
    def generate_id(cls):
        cls.ids += 1
        return cls.ids

class Event:

    def __init__(self, type_, sender, reciever, time_sent) -> None:
        self.type = type_
        self.sender = sender
        self.reciever = reciever
        self.time_sent = time_sent

    def run(self):
        if self.type == POWER:
            self.reciever.power(self.sender)

        elif self.type == UNPOWER:
            self.reciever.unpower(self.sender)

        else:
            pass

class EventManager:
        
    events = []
    update_time = 1
    max_time = 20

    last_ran = 0
    time_started = time.time()

    @classmethod 
    def create_power_event(cls, sender, reciever):
        cls.events.append(Event(POWER, sender, reciever, time.time()))

    @classmethod
    def create_unpower_event(cls, sender, reciever):
        cls.events.append(Event(UNPOWER, sender, reciever, time.time()))

    @classmethod
    def check_events(cls):
        if time.time() >= cls.last_ran + cls.update_time:
            cls.last_ran = time.time()
            for event in cls.events:
                if time.time() >= cls.max_time + event.time_sent: return False
                event.run()

        return True
    
class Component:

    def __init__(self) -> None:
        self.powered = False
        self.id = ID.generate_id()

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, self.__class__): return False
        if self.id != __value.id: return False

        return True
    
    def draw(self, window):
        pass

    def update(self):
        pass

    def check_event(self, event):
        pass

    def power(self, who):
        pass

    def unpower(self, who):
        pass
    
class Wire(Component):

    def __init__(self, start, end) -> None:
        super().__init__()
        self.start_node = start
        self.end_node = end

    def draw(self, window):
        pass

    def update(self):
        pass
 
    def check_event(self, event):
        pass
    
    def power(self, who):
        self.powered = True
        if who == self.start_node:
            EventManager.create_power_event(self, self.end_node)

        elif who == self.end_node:
            EventManager.create_power_event(self, self.start_node)

        else:
            pass

    def unpower(self, who):
        self.powered = False
        if who == self.start_node:
            EventManager.create_unpower_event(self, self.end_node)

        elif who == self.end_node:
            EventManager.create_unpower_event(self, self.start_node)

        else:
            pass
    
class Node(Component):

    def __init__(self) -> None:
        super().__init__()
        self.wires = []

    def draw(self, window):
        pass

    def update(self):
        pass

    def check_event(self, event):
        pass
    
    def power(self, who):
        self.powered = True
        for wire in self.wires:
            if wire == who: continue
            EventManager.create_power_event(self, wire)

    def unpower(self, who):
        self.powered = False
        for wire in self.wires:
            if wire == who: continue
            EventManager.create_unpower_event(self, wire)

class GateNode(Node):

    def __init__(self, parent, type_) -> None:
        super().__init__()
        self.parent = parent
        self.type = type_

    def power(self, who):
        if self.type == OUTPUT:
            for wire in self.wires:
                EventManager.create_power_event(self, wire)

        else:
            self.parent.power(who)

    def unpower(self, who):
        if self.type == OUTPUT:
            for wire in self.wires:
                EventManager.create_unpower_event(self, wire)

        else:
            self.parent.unpower(who)

class ORGate(Component):

    def __init__(self) -> None:
        super().__init__()
        self.input_node = GateNode(self, INPUT)
        self.output_node = GateNode(self, OUTPUT)

    def power(self, who):
        if who == self.output_node: return
        self.output_node.power(self)

    def unpower(self, who):
        if who == self.output_node: return
        for wire in self.input_node.wires:
            if wire.powered: 
                self.output_node.power()
                return

        self.output_node.unpower()

if __name__ == "__main__":
    pass