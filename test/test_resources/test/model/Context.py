class obj:
    def __init__(self, value):
        self.type = type(value)
        self.value = value

    def __dict__(self):
        return dict(type=self.type,
                    value=self.value)


class Signal:
    def __init__(self):
            self.status=obj("")



class Status:
    def __init__(self):
            self.itsSignal=obj(False)



class Context:
    def __init__(self):
        self.Signal = Signal()
        self.Status = Status()
        self.Trigger = obj("")