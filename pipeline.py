class Pipeline:
    def __init__(self, root, actors*):
        if not hasattr(root, "tick") or not hasattr(root.tick, "__call__"):
            raise TypeError("The root of the pipeline must have a tick() method.")
        self.__source = root

        if any(not hasattr(actor, "act") or not hasattr(actor.act, "__call__") for actor in actors):
            raise TypeError("Actors must have an act() method.")
        self.__actors = list(actors)
        
    def tick(self):
        self.__source.tick()
        for actor in self.__actors:
            actor.act()