from aoc2018.day24e1 import Group, IMMUNE_SYSTEM, INFECTION, Battle
import pytest

@pytest.fixture
def immune_system1():
    return Group.parse(1, IMMUNE_SYSTEM, "17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2")

@pytest.fixture
def immune_system2():
    return Group.parse(2, IMMUNE_SYSTEM, "989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3")

@pytest.fixture
def infection1():
    return Group.parse(1, INFECTION, "801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1")

@pytest.fixture
def infection2():
    return Group.parse(2, INFECTION, "4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4")


def test_should_pick_target(immune_system1, infection1, infection2):
    target = immune_system1.pick_target([infection1, infection2])
    assert target == infection2


def test_should_pick_based_on_initiative(infection1, immune_system1, immune_system2):
    target = infection1.pick_target([immune_system1, immune_system2])
    assert target == immune_system1


def test_should_attack(infection2, immune_system2):
    before = immune_system2.unit_count
    infection2.attack(immune_system2)
    assert before - 84 == immune_system2.unit_count


def test_picking_targets_first_highest_initiative():
    e1 = Group.parse(1, IMMUNE_SYSTEM, "20 units each with 200 hit points with an attack that does 300 bludgeoning damage at initiative 2")
    g1 = Group.parse(1, INFECTION, "10 units each with 200 hit points with an attack that does 300 bludgeoning damage at initiative 1")
    g2 = Group.parse(2, INFECTION, "10 units each with 200 hit points with an attack that does 300 bludgeoning damage at initiative 2")
    g3 = Group.parse(3, INFECTION, "10 units each with 200 hit points with an attack that does 300 bludgeoning damage at initiative 3")

    b = Battle([e1], [g1, g2, g3])
    b.pick_targets()
    assert g3 in b.targets


def test_picking_targets_first_highest_effective_power():
    e1 = Group.parse(1, IMMUNE_SYSTEM, "20 units each with 200 hit points with an attack that does 300 bludgeoning damage at initiative 2")
    g1 = Group.parse(1, INFECTION, "10 units each with 200 hit points with an attack that does 300 bludgeoning damage at initiative 1")
    g2 = Group.parse(2, INFECTION, "100 units each with 200 hit points with an attack that does 300 bludgeoning damage at initiative 2")
    g3 = Group.parse(3, INFECTION, "10 units each with 200 hit points with an attack that does 300 bludgeoning damage at initiative 3")

    b = Battle([e1], [g2, g1, g3])
    b.pick_targets()
    assert g2 in b.targets


def test_picking_targets_pick_one_with_largest_effective_power():
    e1 = Group.parse(1, IMMUNE_SYSTEM, "20 units each with 200 hit points with an attack that does 300 bludgeoning damage at initiative 2")
    g1 = Group.parse(1, INFECTION, "10 units each with 200 hit points with an attack that does 300 bludgeoning damage at initiative 1")
    g2 = Group.parse(2, INFECTION, "100 units each with 200 hit points with an attack that does 300 bludgeoning damage at initiative 2")
    g3 = Group.parse(3, INFECTION, "10 units each with 200 hit points with an attack that does 300 bludgeoning damage at initiative 3")

    b = Battle([e1], [g2, g1, g3])
    b.pick_targets()
    assert b.targets[e1] == g2


def test_picking_targets_pick_one_thow_wich_will_deal_the_most_damage():
    e1 = Group.parse(1, IMMUNE_SYSTEM, "20 units each with 200 hit points with an attack that does 300 bludgeoning damage at initiative 2")
    g1 = Group.parse(1, INFECTION, "10 units each with 200 hit points (weak to bludgeoning) with an attack that does 300 bludgeoning damage at initiative 1")
    g2 = Group.parse(2, INFECTION, "10 units each with 200 hit points with an attack that does 300 bludgeoning damage at initiative 2")
    g3 = Group.parse(3, INFECTION, "10 units each with 200 hit points with an attack that does 300 bludgeoning damage at initiative 3")

    b = Battle([e1], [g2, g1, g3])
    b.pick_targets()
    assert b.targets[e1] == g1


def test_picking_targets_pick_one_with_highest_initiative():
    e1 = Group.parse(1, IMMUNE_SYSTEM, "20 units each with 200 hit points with an attack that does 300 bludgeoning damage at initiative 2")
    g1 = Group.parse(1, INFECTION, "10 units each with 200 hit points with an attack that does 300 bludgeoning damage at initiative 1")
    g2 = Group.parse(2, INFECTION, "10 units each with 200 hit points with an attack that does 300 bludgeoning damage at initiative 2")
    g3 = Group.parse(3, INFECTION, "10 units each with 200 hit points with an attack that does 300 bludgeoning damage at initiative 3")

    b = Battle([e1], [g2, g1, g3])
    b.pick_targets()
    assert b.targets[e1] == g3


def test_picking_targets_shouldnt_pick_anything_if_cant_deal_damage():
    e1 = Group.parse(1, IMMUNE_SYSTEM, "20 units each with 200 hit points with an attack that does 300 bludgeoning damage at initiative 2")
    g1 = Group.parse(1, INFECTION, "10 units each with 200 hit points (immune to bludgeoning) with an attack that does 300 bludgeoning damage at initiative 1")
    g2 = Group.parse(2, INFECTION, "10 units each with 200 hit points (immune to bludgeoning) with an attack that does 300 bludgeoning damage at initiative 2")
    g3 = Group.parse(3, INFECTION, "10 units each with 200 hit points (immune to bludgeoning) with an attack that does 300 bludgeoning damage at initiative 3")

    b = Battle([e1], [g2, g1, g3])
    b.pick_targets()
    assert b.targets == {g3: e1}
