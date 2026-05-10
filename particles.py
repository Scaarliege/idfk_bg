import pygame
import random
import math
import colorsys


class Particle:
    """Individual particle in the system with position, velocity, and color."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.vx = random.uniform(-0.5, 0.5)  # Velocity
        self.vy = random.uniform(-0.5, 0.5)
        self.size = random.uniform(1, 5)
        self.base_size = self.size  # retain for pulsing effect
        self.phase = random.random() * 2 * math.pi  # phase offset for pulses
        self.opacity = 255
        # base_color will be assigned after particle creation (either color_a or color_b)
        self.base_color: tuple[int, int, int, int] = (255, 255, 255, self.opacity)

    def get_color(self) -> tuple[int, int, int, int]:
        """Return the particle's assigned base color with hue shift."""
        r, g, b, _ = self.base_color
        t = pygame.time.get_ticks() * 0.0001
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        h = (h + t) % 1.0
        r2, g2, b2 = colorsys.hsv_to_rgb(h, s, v)
        return (int(r2 * 255), int(g2 * 255), int(b2 * 255), int(self.opacity))

    def update(self):
        """Update particle position, size, and opacity."""
        # basic motion
        self.x += self.vx
        self.y += self.vy

        # pulsing size/opacity based on time
        t = pygame.time.get_ticks() * 0.002
        self.size = self.base_size + math.sin(t + self.phase) * self.base_size * 0.5
        # keep size positive
        if self.size < 0.5:
            self.size = 0.5
        self.opacity = 200 + 55 * (1 + math.sin(t + self.phase)) / 2

        # Wrap around edges
        if self.x < 0:
            self.x = self.width
        elif self.x > self.width:
            self.x = 0
        if self.y < 0:
            self.y = self.height
        elif self.y > self.height:
            self.y = 0

    def cap_speed(self, max_speed: float):
        """Limit particle velocity to max_speed."""
        speed = math.hypot(self.vx, self.vy)
        if speed > max_speed:
            self.vx = (self.vx / speed) * max_speed
            self.vy = (self.vy / speed) * max_speed

    def draw(self, screen: pygame.Surface):
        """Draw particle to screen."""
        color = self.get_color()
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.size))


class ParticleSystem:
    """Manages a collection of particles."""
    
    def __init__(self, width: int, height: int, num_particles: int = 100):
        self.width = width
        self.height = height
        self.particles = []
        self.connection_radius = 120
        self.cell_size = self.connection_radius
        
        # Create particles with alternating colors
        color_a = self.random_color()
        color_b = (255 - color_a[0], 255 - color_a[1], 255 - color_a[2], 255)
        
        for i in range(num_particles):
            p = Particle(width, height)
            p.base_color = color_a if i < num_particles // 2 else color_b
            self.particles.append(p)
    
    @staticmethod
    def random_color() -> tuple[int, int, int, int]:
        """Generate a random RGBA color."""
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)
    
    def update(self):
        """Update all particles."""
        for particle in self.particles:
            particle.update()
            particle.cap_speed(0.8)
    
    def draw(self, screen: pygame.Surface):
        """Draw all particles to screen."""
        for particle in self.particles:
            particle.draw(screen)
    
    def get_connections(self) -> list[tuple[int, int, float, int]]:
        """Build spatial grid and find particle connections within radius."""
        grid = {}
        
        # Place particles into spatial grid
        for idx, particle in enumerate(self.particles):
            cx = int(particle.x) // self.cell_size
            cy = int(particle.y) // self.cell_size
            grid.setdefault((cx, cy), []).append(idx)
        
        # Find neighbor connections using grid
        connections = []
        for i, p1 in enumerate(self.particles):
            x1 = p1.x
            y1 = p1.y
            cx = int(x1) // self.cell_size
            cy = int(y1) // self.cell_size
            
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    cell = (cx + dx, cy + dy)
                    if cell not in grid:
                        continue
                    for j in grid[cell]:
                        if j <= i:
                            continue
                        p2 = self.particles[j]
                        dx_ = x1 - p2.x
                        dy_ = y1 - p2.y
                        dist = math.hypot(dx_, dy_)
                        if dist < self.connection_radius:
                            alpha = int(255 * (1 - dist / self.connection_radius))
                            if alpha > 0:
                                connections.append((i, j, dist, alpha))
        
        return connections
    
    def handle_mouse_click(self, mouse_x: int, mouse_y: int, grab_radius: float = 100):
        """Apply force to particles near mouse click."""
        for particle in self.particles:
            dist_to_mouse = math.hypot(particle.x - mouse_x, particle.y - mouse_y)
            if dist_to_mouse < grab_radius:
                dx = mouse_x - particle.x
                dy = mouse_y - particle.y
                particle.vx += dx * 0.05
                particle.vy += dy * 0.05
