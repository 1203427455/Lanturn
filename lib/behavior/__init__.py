class BlackBoard(object):
    def __init__(self):
        self.data = {}

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value

class Task(object):
    def update(self):
        raise NotImplementedError()

class ParentTask(Task):
    def __init__(self):
        self.children = []

class Sequence(ParentTask):
    def __init__(self, blackboard):
        super(Sequence, self).__init__()
        self.bb = blackboard

    def update(self):
        for child in children:
            result = child.update()
            if not result:
                return False

        return True
        
class Selector(ParentTask):
    def __init__(self, blackboard):
        super(Sequence, self).__init__()
        self.bb = blackboard

    def update(self):
        for child in children:
            result = child.update()
            if result:
                return True

        return False
