import math
import re
from aoc2018 import readlines


ATTACK_TYPES = {'fire', 'cold', 'slashing', 'bludgeoning', 'radiation'}


IMMUNE_SYSTEM = 0
INFECTION = 1



class Group:
    def __init__(self, number, group_type, unit_count, unit_hit_points, attack_type, unit_power, initiative, weak_to, immune_to):
        if weak_to is None:
            weak_to = []
        if immune_to is None:
             immune_to = []
        if any([not a in ATTACK_TYPES for a in immune_to + weak_to]):
            raise Exception('Illegal attack type!' + str(immune_to) + str(weak_to) )
        self.number = number
        self.group_type = group_type
        self.unit_count = unit_count
        self.unit_hit_points = unit_hit_points
        self.attack_type = attack_type
        self.unit_power = unit_power
        self.initiative = initiative
        self.weak_to = weak_to
        self.immune_to = immune_to

    def __eq__(self, other):
        return self.initiative == other.initiative

    def __lt__(self, other):
        return self.initiative < other.initiative

    def __hash__(self):
        return hash(self.initiative)

    def __str__(self):
        imwee = ""
        if self.immune_to:
            imwee = "immune to %s" % ', '.join(self.immune_to)
        if self.weak_to:
            if imwee:
                imwee += '; '
            imwee += "weak to %s" % ', '.join(self.weak_to)
        if imwee:
            imwee = '(%s) ' % imwee

        return "%d units each with %d hit points %swith an attack that does %d %s damage at initiative %d" % (self.unit_count, self.unit_hit_points, imwee, self.unit_power, self.attack_type, self.initiative)

    __repr__ = __str__

    @property
    def effective_power(self):
        return int(self.unit_count * self.unit_power)

    @property
    def hit_points(self):
        return int(self.unit_count * self.unit_hit_points)

    @classmethod
    def parse(cls, number, group_type, line):
        """
        >>> Group.parse(0, INFECTION, "7550 units each with 8773 hit points (immune to radiation; weak to fire, slashing) with an attack that does 11 radiation damage at initiative 11")
        7550 units each with 8773 hit points (immune to radiation; weak to fire, slashing) with an attack that does 11 radiation damage at initiative 11
        """
        LINE_REGEX = re.compile("(\d+) units each with (\d+) hit points ?(?:\((.+)\))? with an attack that does (\d+) (\w+) damage at initiative (\d+)")
        unit_count, hit_points, imm_wee, power, attack_type, initiative = LINE_REGEX.match(line).groups()
        unit_count = int(unit_count)
        hit_points = int(hit_points)
        power = int(power)
        initiative = int(initiative)
        imm_wee = imm_wee or ""

        immune_to = []
        weak_to = []

        for data in imm_wee.split('; '):
            if not data:
                continue
            if data.startswith('immune to'):
                immune_to = data[len('immune to '):].split(', ')
            else:
                weak_to = data[len('weak to '):].split(', ')

        return cls(number, group_type, unit_count, hit_points, attack_type, power, initiative, weak_to, immune_to)

    def pick_target(self, enemies):
        enemies = [e for e in enemies if self.estimate_damage(e)]
        if enemies:
            return sorted(enemies, key=lambda e: (self.estimate_damage(e), e.effective_power, e.initiative))[-1]

    def estimate_damage(self, enemy):
        ep = self.effective_power
        if self.attack_type in enemy.weak_to:
            return ep * 2
        if self.attack_type in enemy.immune_to:
            return None
        return ep

    def attack(self, enemy):
        damage = self.estimate_damage(enemy)
        if damage > enemy.hit_points:
            enemy.unit_count = 0
        else:
            enemy.unit_count = math.ceil((enemy.hit_points - damage) / enemy.unit_hit_points)


class Battle:
    def __init__(self, immune_system, infection):
        self._immune_system = sorted(immune_system, key=lambda g: (g.effective_power, g.initiative), reverse=True)
        self._infection = sorted(infection, key=lambda g: (g.effective_power, g.initiative), reverse=True)
        self.targets = {}

    @property
    def immune_system(self):
        return [g for g in self._immune_system if g.unit_count > 0]

    @property
    def infection(self):
        return [g for g in self._infection if g.unit_count > 0]

    def pick_targets(self):
        self.targets = {}

        immune_system_as_target = list(self.immune_system)
        infection_as_target = list(self.infection)

        for g in self.infection:
            t = g.pick_target(immune_system_as_target)
            if t:
                self.targets[g] = t
                immune_system_as_target.remove(t)

        for g in self.immune_system:
            t = g.pick_target(infection_as_target)
            if t:
                self.targets[g] = t
                infection_as_target.remove(t)

    def fight(self):
        for g in sorted(self.immune_system + self.infection, key=lambda g: (g.initiative), reverse=True):
            if g not in self.targets:
                continue
            target = self.targets[g]
            if g.group_type == IMMUNE_SYSTEM:
                t = 'Immune System'
            else:
                t = 'Infection'

            units_before = target.unit_count
            g.attack(target)
            killed = units_before - target.unit_count


def parse(lines):
    immune_system = []
    infection = []
    group_type = IMMUNE_SYSTEM
    group_number = 1
    for line in lines[1:]:
        if not line:
            continue
        if line.startswith('Infection'):
            group_type = INFECTION
            group_number = 1
            now_infections = True
            continue

        g = Group.parse(group_number, group_type, line)
        group_number += 1
        if group_type == INFECTION:
            infection.append(g)
        else:
            immune_system.append(g)
    return immune_system, infection


def simulate(immune_system, infection):
    previous_state = 0
    while immune_system and infection:
        battle = Battle(immune_system, infection)
        battle.pick_targets()
        battle.fight()

        immune_system = battle.immune_system
        infection = battle.infection

        current_state = sum([g.unit_count for g in immune_system + infection])
        if previous_state == current_state:
            print('tie detected!')
            break
        previous_state = current_state
    return immune_system, infection


def solve(lines):
    immune_system, infection = parse(lines)
    immune_system, infection = simulate(immune_system, infection)

    return sum([g.unit_count for g in immune_system + infection])


lines = """Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4""".split('\n')


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())

    print(solve(readlines()))
