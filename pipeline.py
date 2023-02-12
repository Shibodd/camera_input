class Pipeline:
    def __init__(self, root):
        if not hasattr(root, "tick") or not hasattr(root.tick, "__call__"):
            raise TypeError("The root of the pipeline must have a tick() method.")
        self.__source = root
        self.__actors = []

    def add_actor(self, actor):
        if not hasattr(actor, "act") or not hasattr(actor.act, "__call__"):
            raise TypeError("An actor must have an act() method.")
        self.__actors.append(actor)

    def tick(self):
        self.__source.tick()
        for actor in self.__actors:
            actor.act()