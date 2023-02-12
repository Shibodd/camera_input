class Pipeline:
    """ Implements a pipeline which, on tick, updates the sources and let the actors pull data from the pipeline. """

    def __init__(self, sources, actors):
        if any(not hasattr(source, "tick") or not hasattr(source.tick, "__call__") for source in sources):
            raise TypeError("The root of the pipeline must have a tick() method.")
        if any(not hasattr(actor, "act") or not hasattr(actor.act, "__call__") for actor in actors):
            raise TypeError("Actors must have an act() method.")

        self.__sources = list(sources)
        self.__actors = list(actors)
        
    def tick(self):
        for source in self.__sources:
            source.tick()
        for actor in self.__actors:
            actor.act()