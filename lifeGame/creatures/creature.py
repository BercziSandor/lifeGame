import random
from typing import List

import numpy as np

from lifeGame import storyBoard
from lifeGame.utils import Position


class Creature:
    position: Position
    danger_zone: float
    age_hours: float
    time_of_death: float

    def __init__(self, name: str = None, sight_range_m: float = 0.0,
                 age_expected_years: float = 10,
                 age_deviation_years: float = 0, age_years: float = 0.0,
                 sex: str = None,
                 children_expected: int = 1, children_deviation: float = 0,
                 sexual_maturity_at_age_years: float = 0.0,
                 velocity_max_mps: float = None,
                 velocity_exhaustion_rate: float = None,
                 lenght_of_pregnancy_hours: float = None,
                 position: Position = None,
                 nutrition=None, fear_of=[], danger_zone=1.0,
                 energy_for_days: float = 1.0, weight_newborn: float = 0.0,
                 weight_adult: float = 1.0, time_of_birth: float = None):
        self.object_id = id(self)
        if not age_deviation_years:
            age_deviation_years = age_expected_years * 0, 3
        if not sex:
            sex = random.choice(['female', 'male'])
        self.name = name
        self.sight_range_m = sight_range_m
        self.age_hours = age_years * 365 * 24
        self.time_of_birth = time_of_birth
        self.time_of_death = None
        self.sex = sex
        self.sexual_maturity_at_age_hours = sexual_maturity_at_age_years * 364 * 24
        self.is_pregnant = False
        self.lenght_of_pregnancy_hours = lenght_of_pregnancy_hours
        self.children_expected = children_expected
        self.children_deviation = children_deviation
        self.weight_newborn = weight_newborn
        self.weight_adult = weight_adult

        self.nutrition = nutrition
        self.fear_of = fear_of
        self.danger_zone = danger_zone
        self.position: Position = position
        self.storyBoard: storyBoard = None
        if age_deviation_years and age_deviation_years > 0:
            self.die_at_age_years = np.random.normal(age_expected_years,
                                                     age_deviation_years)
        else:
            self.die_at_age_years = age_expected_years

        self.velocity_max = velocity_max_mps
        self.velocity_endurance = velocity_exhaustion_rate
        self.energy_for_hours = energy_for_days * 24

    def __str__(self):
        rv = f"Name:               {self.name}\n"
        rv += f"Race:               {self.__class__.__name__}\n"
        rv += f"Sex:                {self.sex}\n"
        if self.time_of_birth:
            rv += f"Time of birth:      {self.time_of_birth:.1f} (hours)\n"
        rv += f"Death at age[hours]:{self.die_at_age_years * 365 * 24:.1f}\n"

        if self.time_of_death:
            rv += f"Time of death:      {self.time_of_death:.1f}\n"

        rv += f"Age:                {self.age_hours:.1f} hours (" \
              f"{self.age_hours / (24 * 365):.1f} years)\n"

        rv += f"Death at age[year]: {self.die_at_age_years:.12f}\n"
        rv += f"Sight range[m]:     {self.sight_range_m:.1f}\n"
        if self.position:
            rv += f"Position:           {self.position.x:.2f}, " \
                  f"{self.position.y:.2f}\n"
        return rv

    def is_sexual_mature(self):
        return self.age_hours >= self.sexual_maturity_at_age_hours

    def is_living(self, time: float):
        return time > self.time_of_birth and time < self.time_of_death

    def get_children(self) -> List:
        child_count = int(
            np.random.normal(self.children_expected, self.children_deviation))
        return [self.__class__(position=self.position) for _ in
                range(child_count)]

    def attack(self, victim):
        pass  # TODO

    def is_starving(self):
        pass  # TODO

    def get_age_at_in_hours(self, time: float) -> float:
        return time - self.time_of_birth

    def filter_enemies(self, creatures: List['Creature']) -> List:
        enemies = [x for x in creatures if x.__class__.__name__ in self.fear_of]
        return enemies

    def filter_nutrition(self, creatures: List['Creature']) -> List:
        return [x for x in creatures if x.__class__.__name__ in self.nutrition]

    def filter_partner(self, creatures: List['Creature']) -> List:
        if self.is_pregnant or not self.is_sexual_mature():
            return []

        return [x for x in creatures if self.object_id != x.object_id and
                x.__class__.__name__ == self.__class__.__name__ and
                self.sex != x.sex and not x.is_pregnant and
                x.is_sexual_mature()]

    def sort_by_distance(self, creatures: List['Creature']) -> List:
        return sorted(creatures,
                      key=lambda c: self.position.distance_to(c.position))

    def get_weight(self) -> float:
        if self.age_hours > self.sexual_maturity:
            weight = self.weight_adult
        else:
            weight = (self.weight_adult - self.weight_newborn) / \
                     self.sexual_maturity * self.age_hours + self.weight_newborn

        return weight

    def get_energy_reserves_in_hours(self) -> float:
        pass

    def get_next_step(self):
        close_creatures: List[Creature] = self.storyBoard \
            .get_creatures_in_range(self.position, self.sight_range_m)
        close_nutrition = self.filter_nutrition(close_creatures)
        close_enemies = self.filter_nutrition(close_creatures)
        close_partner = self.filter_partner()

        # eat?
        if self.is_starving():
            pass
        # run away?
        # reproduce?


class Hunter(Creature):
    def __init__(self, name=None):
        if name is None:
            first_name = random.choice(['Béla', 'Géza', 'Jani', 'Tamás',
                                        'Pista'])
            last_name = random.choice(['Kovács', 'Nagy', 'Kis', 'Varga'])
            name = f"{last_name} {first_name}"
        super().__init__(name=name, sight_range_m=5000, danger_zone=2000.0,
                         age_expected_years=60, age_deviation_years=20,
                         age_years=max(25, np.random.normal(30, 20)),
                         nutrition=['Rabbit', 'Wolf'],
                         sex='male', children_expected=1,
                         children_deviation=0)


class Grass(Creature):
    def __init__(self, name=None):
        super().__init__(name=name, sight_range_m=0, age_expected_years=1,
                         age_deviation_years=0.0001, children_expected=3,
                         children_deviation=0, sexually_mature_at_age_years=0.2,
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
        super().__init__(name=name, sight_range_m=500, age_expected_years=8,
                         age_deviation_years=1, children_expected=6,
                         children_deviation=5, sexual_maturity_at_age_years=0.5,
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
        super().__init__(name=name, sight_range_m=5000, age_expected_years=7,
                         age_deviation_years=1, children_expected=5,
                         children_deviation=2, sexual_maturity_at_age_years=2,
                         velocity_max_mps=40 / 3.6, velocity_exhaustion_rate=9,
                         nutrition=['Rabbit'],
                         fear_of=['Hunter'],
                         lenght_of_pregnancy_hours=63 * 24, energy_for_days=5.0)
