import random
from typing import List

import numpy as np

from lifeGame import storyBoard
from lifeGame.utils import Position


class Creature:
    position: Position
    danger_zone: float

    def __init__(self, name: str = None, sight_range_m: float = 0.0,
                 age_expected: float = 10,
                 age_deviation: float = 0, age: float = 0, sex: str = None,
                 children_expected: int = 1, children_deviation: float = 0,
                 sexual_maturity: float = None, velocity_max_mps: float = None,
                 velocity_exhaustion_rate: float = None,
                 lenght_of_pregnancy_hours: float = None,
                 position: Position = None,
                 nutrition=None, fear_of=None, danger_zone=1.0,
                 energy_for_days: float = 1.0):
        self.object_id = id(self)
        if not age_deviation:
            age_deviation = age_expected * 0, 3
        if not sex:
            sex = random.choice(['female', 'male'])
        self.name = name
        self.sight_range_m = sight_range_m
        self.age = age
        self.sex = sex
        self.sexual_maturity = sexual_maturity
        self.is_pregnant = False
        self.lenght_of_pregnancy_hours = lenght_of_pregnancy_hours
        self.children_expected = children_expected
        self.children_deviation = children_deviation

        self.nutrition = nutrition
        self.fear_of = fear_of
        self.danger_zone = danger_zone
        self.position: Position = position
        self.storyBoard: storyBoard = None
        if age_deviation and age_deviation > 0:
            self.die_at_age = np.random.normal(age_expected, age_deviation)
        else:
            self.die_at_age = age_expected

        self.velocity_max = velocity_max_mps
        self.velocity_endurance = velocity_exhaustion_rate
        self.energy_for_hours = energy_for_days * 24

    def __str__(self):
        rv = f"Name:               {self.name}\n"
        rv += f"Race:               {self.__class__.__name__}\n"
        rv += f"Sex:                {self.sex}\n"
        rv += f"Age[year]:          {self.age:.1f}\n"
        rv += f"Death at age[year]: {self.die_at_age:.1f}\n"
        rv += f"Sight range[m]:     {self.sight_range_m:.1f}\n"
        if self.position:
            rv += f"Position:           {self.position.x:.2f}, " \
                  f"{self.position.y:.2f}\n"
        return rv

    def is_sexual_mature(self):
        return self.age >= self.sexual_maturity

    def get_children(self) -> List:
        child_count = int(
            np.random.normal(self.children_expected, self.children_deviation))
        return [self.__class__(position=self.position) for _ in
                range(child_count)]

    def attack(self, victim):
        pass  # TODO

    def is_starving(self):
        pass  # TODO

    def filter_enemies(self, creatures: List) -> List:
        enemies = [x for x in creatures if x.__class__.__name__ in self.fear_of]
        return enemies

    def filter_nutrition(self, creatures: List) -> List:
        return [x for x in creatures if x.__class__.__name__ in self.nutrition]

    def filter_partner(self, creatures: List) -> List:
        if self.is_pregnant or not self.is_sexual_mature():
            return []

        return [x for x in creatures if self.object_id != x.object_id and
                x.__class__.__name__ == self.__class__.__name__ and
                self.sex != x.sex and not x.is_pregnant and
                 x.is_sexual_mature()]

    def sort_by_distance(self, creatures: List) -> List:
        return sorted(creatures,
                      key=lambda c: self.position.distance_to(c.position))

    def get_next_step(self):
        close_creatures: List[Creature] = self.storyBoard \
            .get_creatures_in_range(self.position, self.sight_range_m)
        close_nutrition = self.filter_nutrition(close_creatures)
        close_enemies = self.filter_nutrition(close_creatures)
        close_partner = self.filter_partner()

        # eat?

        # escape?
        # reproduce?

        # if self.is_starving():


class Hunter(Creature):
    def __init__(self, name=None):
        if name is None:
            first_name = random.choice(['Béla', 'Géza', 'Jani', 'Tamás',
                                        'Pista'])
            last_name = random.choice(['Kovács', 'Nagy', 'Kis', 'Varga'])
            name = f"{last_name} {first_name}"
        super().__init__(name=name, sight_range_m=5000, danger_zone=2000.0,
                         age_expected=60, age_deviation=20,
                         age=max(25, np.random.normal(30, 20)),
                         nutrition=['Rabbit', 'Wolf'],
                         sex='male', children_expected=1,
                         children_deviation=0)


class Grass(Creature):
    def __init__(self, name=None):
        super().__init__(name=name, sight_range_m=0, age_expected=1,
                         age_deviation=0.0001, children_expected=3,
                         children_deviation=0, sexual_maturity=0.2,
                         sex=None,
                         velocity_max_mps=0, velocity_exhaustion_rate=0,
                         energy_for_days=1.0 / 10)


class Rabbit(Creature):
    def __init__(self, name=None):
        if name is None:
            name = random.choice(
                ["Bogyó", "Csoki", "Mogyi", "Tapsi", "Pompom", "Cukor", "Pufók",
                 "Zokni", "Pacsi", "Répa", "Málna", "Muki", "Csibész"]
            )
        super().__init__(name=name, sight_range_m=500, age_expected=8,
                         age_deviation=1, children_expected=6,
                         children_deviation=5, sexual_maturity=0.5,
                         velocity_max_mps=60 / 3.6, velocity_exhaustion_rate=3,
                         nutrition=['Grass'],
                         fear_of=['Wolf'],
                         lenght_of_pregnancy_hours=32 * 24, energy_for_days=3.0)


class Wolf(Creature):
    def __init__(self, name=None):
        if name is None:
            name = random.choice(
                ["Vihar", "Vadur", "Cselek", "Zafír", "Csillag", "Farkas",
                 "Rozsda", "Vadász", "Szél", "Morzsa", "Bátor", "Tűzvész",
                 "Zenge", "Zord", ]
            )
        super().__init__(name=name, sight_range_m=5000, age_expected=7,
                         age_deviation=1, children_expected=5,
                         children_deviation=2, sexual_maturity=2,
                         velocity_max_mps=40 / 3.6, velocity_exhaustion_rate=9,
                         nutrition=['Rabbit'],
                         fear_of=['Hunter'],
                         lenght_of_pregnancy_hours=63 * 24, energy_for_days=5.0)
