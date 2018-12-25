from aoc2018.day24e1 import Group, IMMUNE_SYSTEM
import pytest


def group(unit_count, unit_hit_points, attack_type, unit_power, week_to=None, immune_to=None, initiative=1):
    return Group(1, IMMUNE_SYSTEM, unit_count, unit_hit_points, attack_type, unit_power, initiative, weak_to, immune_to)

