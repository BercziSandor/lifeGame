# from lifeGame.creatures.hunter import Hunter
from lifeGame.creatures.creature import Wolf, Hunter, Rabbit
from lifeGame.simulation import Simulation
from lifeGame.storyBoard import StoryBoard


def main():
    sb = StoryBoard(size=(10000.0, 10000.0))
    sb.addCreature(Hunter())
    sb.addCreature(Wolf())
    sb.addCreature(Rabbit())
    sb.addCreature(Rabbit())
    sb.addCreature(Rabbit())
    sb.addCreature(Rabbit())
    r = Rabbit()
    sb.addCreature(r)

    print(sb)

    # s = Simulation(storyBoard=sb)
    # print(f"Status of the simulation at {s.time:.2f}")
    # for c in s.get_creatures():
    #     print(c)

    # s.start()

    # fu=Grass()
    # print(fu)
    #
    # children = fu.get_children()
    # print(f"Children of fu:")
    # [print(x) for x in children]


if __name__ == '__main__':
    main()
