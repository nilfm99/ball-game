import random
from typing import Any

import pymunk


BASE_CRIT_CHANCE = 0.05  # 5% minimum
CRIT_SCALE = 0.0001  # 0.1% per unit of impact speed (tune as needed)
CRIT_MULTIPLIER = 2  # Double damage on crit


def _get_ball_damage(speed: float, crit: bool) -> int:
    base_damage = int(speed / 20)
    return base_damage * CRIT_MULTIPLIER if crit else base_damage


def _crit_roll(impact_speed: float) -> bool:
    crit_chance = min(1.0, BASE_CRIT_CHANCE + impact_speed * CRIT_SCALE)
    return random.random() < crit_chance


def handle_ball_to_ball_collision(
        arbiter: pymunk.Arbiter,
        _space: pymunk.Space,
        _data: Any,
) -> None:
    shape_a, shape_b = arbiter.shapes
    assert shape_a.body is not None
    assert shape_b.body is not None
    ball_a = shape_a.body.user_data
    ball_b = shape_b.body.user_data

    n = arbiter.contact_point_set.normal

    v_a = ball_a.body.velocity
    v_b = ball_b.body.velocity

    # Alignment-based impact speeds (damage basis)
    impact_b_to_a = max(0, v_b.dot(-n))
    impact_a_to_b = max(0, v_a.dot(n))

    # Crit rolls
    crit_a = _crit_roll(impact_b_to_a)
    crit_b = _crit_roll(impact_a_to_b)

    damage_to_a = _get_ball_damage(impact_b_to_a, crit_b)
    damage_to_b = _get_ball_damage(impact_a_to_b, crit_a)

    # First-hitter advantage: whoever was going to do the most damage gets first hit
    a_health = ball_a.health - damage_to_a
    b_health = ball_b.health - damage_to_b

    if a_health <= 0 and b_health <= 0:
        if a_health > b_health:
            damage_to_a = 0
        elif b_health > a_health:
            damage_to_b = 0

    ball_a.deal_damage(damage_to_b, crit_a)
    ball_b.deal_damage(damage_to_a, crit_b)

    ball_a.receive_damage(damage_to_a, crit_b)
    ball_b.receive_damage(damage_to_b, crit_a)


def handle_post_ball_to_ball_collision(
        arbiter: pymunk.Arbiter,
        _space: pymunk.Space,
        _data: Any,
) -> None:
    shape_a, shape_b = arbiter.shapes
    assert shape_a.body is not None
    assert shape_b.body is not None
    ball_a = shape_a.body.user_data
    ball_b = shape_b.body.user_data
    ball_a.remove_if_dead()
    ball_b.remove_if_dead()