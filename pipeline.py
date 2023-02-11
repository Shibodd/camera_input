class Pipeline:
    def __init__(self, root):
        self.source = root
        self.actors = []

    def add_actor(self, actor):
        self.actors.append(actor)

    def tick(self):
        self.source.tick()
        for actor in self.actors:
            actor.tick()