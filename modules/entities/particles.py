import pygame
import random
from typing import List, Tuple
from modules.entities.base_entity import BaseEntity


class FizzyParticle(BaseEntity):
    """
    A lightweight visual entity for fizzy pop/burst effects.
    Fades out exponentially over its lifetime.
    """

    def __init__(self, x: float, y: float, color: Tuple[int, int, int], velocity: Tuple[float, float], lifetime_decay: float) -> None:
        super().__init__(x, y)
        self.color = color
        self.vx, self.vy = velocity
        self.lifetime_decay = lifetime_decay
        self.alpha = 255.0
        self.radius = random.uniform(2.0, 5.0)

    def update(self, dt: float) -> None:
        """
        Updates position based on velocity and handles exponential fade.
        """
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Exponential fade decay (e.g., self.alpha *= self.lifetime_decay)
        self.alpha *= self.lifetime_decay

    def is_alive(self) -> bool:
        """
        Returns True if the particle is still visible enough to be drawn.
        """
        return self.alpha > 5.0

    def draw(self, screen: pygame.Surface) -> None:
        """
        Renders the particle using SRCALPHA and additive blending for a glow effect.
        """
        if self.alpha <= 0:
            return

        size = int(self.radius * 2)
        s = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Combine the base color with the current alpha
        rgba_color = (self.color[0], self.color[1], self.color[2], int(self.alpha))
        pygame.draw.circle(s, rgba_color, (int(self.radius), int(self.radius)), int(self.radius))
        
        # Blit the particle surface with additive blending for full fizz effect
        screen.blit(s, (int(self.x - self.radius), int(self.y - self.radius)), special_flags=pygame.BLEND_RGBA_ADD)


class ParticleManager:
    """
    Manages the lifecycle, updating, and drawing of all active particles.
    """
    def __init__(self) -> None:
        self.active_particles: List[FizzyParticle] = []

    def spawn_burst(self, position: Tuple[float, float], color: Tuple[int, int, int], count: int) -> None:
        """
        Spawns `count` particles at `position` bursting outwards in a circle.
        """
        x, y = position
        for _ in range(count):
            # Random outward velocity
            vx = random.uniform(-200.0, 200.0)
            vy = random.uniform(-200.0, 200.0)
            
            # Slight color variation for a nicer effect
            c = (
                min(255, max(0, color[0] + random.randint(-20, 20))),
                min(255, max(0, color[1] + random.randint(-20, 20))),
                min(255, max(0, color[2] + random.randint(-20, 20)))
            )
            
            # Exponential decay factor (e.g., 0.85 to 0.96)
            decay = random.uniform(0.85, 0.96)
            
            self.active_particles.append(FizzyParticle(x, y, c, (vx, vy), decay))

    def update(self, dt: float) -> None:
        """
        Updates all particles and removes faded ones.
        """
        for particle in self.active_particles[:]:
            particle.update(dt)
            if not particle.is_alive():
                self.active_particles.remove(particle)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Renders all active particles to the screen.
        """
        for particle in self.active_particles:
            particle.draw(screen)
