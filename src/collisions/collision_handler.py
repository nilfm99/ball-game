import random
from typing import Any

import pymunk


class CollisionHandler:
    BASE_CRIT_CHANCE = 0.05  # 5% minimum
    CRIT_SCALE = 0.00005  # 0.05% per unit of impact speed (tune as needed)
    CRIT_MULTIPLIER = 2  # Double damage on crit

    @staticmethod
    def get_ball_damage(speed: float, crit: bool) -> int:
        base_damage = int(speed / 20)
        return base_damage * CollisionHandler.CRIT_MULTIPLIER if crit else base_damage

    @staticmethod
    def crit_roll(impact_speed: float) -> bool:
        crit_chance = min(1.0, CollisionHandler.BASE_CRIT_CHANCE + impact_speed * CollisionHandler.CRIT_SCALE)
        return random.random() < crit_chance

    @staticmethod
    def handle_ball_collision(
            arbiter: pymunk.Arbiter,
            space: pymunk.Space,
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
        crit_a = CollisionHandler.crit_roll(impact_b_to_a)
        crit_b = CollisionHandler.crit_roll(impact_a_to_b)

        if crit_a:
            ball_a.set_crit()
        if crit_b:
            ball_b.set_crit()

        damage_to_a = CollisionHandler.get_ball_damage(impact_b_to_a, crit_b)
        damage_to_b = CollisionHandler.get_ball_damage(impact_a_to_b, crit_a)

        a_health = ball_a.health - damage_to_a
        b_health = ball_b.health - damage_to_b

        if a_health <= 0 and b_health <= 0:
            # First-hitter advantage: whoever was going to do the most damage gets first hit
            if a_health > b_health:
                a_health = ball_a.health
            elif b_health > a_health:
                b_health = ball_b.health

        ball_a.health = max(0, a_health)
        ball_b.health = max(0, b_health)

        if ball_a.health <= 0:
            space.remove(ball_a.body, shape_a)
        if ball_b.health <= 0:
            space.remove(ball_b.body, shape_b)

        if damage_to_a > 0:
            ball_a.set_hit(damage_to_a)
        if damage_to_b > 0:
            ball_b.set_hit(damage_to_b)
