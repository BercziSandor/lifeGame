import random
from typing import Set, List

# from lifeGame.creatures.creature import Creature
from lifeGame.utils import Position


class StoryBoard:
    creatures: set

    def __init__(self, creatures: Set = set(),
                 size: tuple[float, float] = (
                         100, 100)):
        self.size = size
        self.creatures: Set = set()
        [self.addCreature(c) for c in creatures]

    def __str__(self):
        rv = ""
        rv += f"Size:            {self.size[0]} x {self.size[1]}\n"
        rv += f"Creatures:\n"
        for c in self.creatures:
            rv += str(c)
            rv += "\n"

            creatures_in_range = self.get_creatures_in_range(c.position,
                                                             c.sight_range_m)
            rv += "\nPossible partners nearby:\n"
            for p in c.filter_partner(creatures_in_range):
                rv += str(p)
            rv += "\nEnemies nearby:\n"
            for p in c.filter_enemies(creatures_in_range):
                rv += str(p)
            rv += "\nNutrition nearby:\n"
            for p in c.filter_nutrition(creatures_in_range):
                rv += str(p)
            rv += "-------------------------------\n"

        return rv

    def addCreature(self, creature, position: Position = None):
        if not creature.position:
            if position:
                creature.position = position
            else:
                creature.position = Position(
                    random.uniform(0, self.size[0]),
                    random.uniform(0, self.size[1])
                )
        creature.storyBoard = self
        self.creatures.add(creature)

    def get_creatures_in_range(self, pos: Position, range: float) -> List:
        # c: Creature
        return [c for c in self.creatures if pos.distance_to(
            c.position) < range]
