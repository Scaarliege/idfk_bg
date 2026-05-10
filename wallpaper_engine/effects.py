import pygame
import math
import colorsys
import random


def apply_blur(surf: pygame.Surface, iterations: int = 2, scale: float = 0.5) -> pygame.Surface:
    """Smooth blur by scaling down and back up."""
    size = surf.get_size()
    scale = max(0.28, min(0.6, scale))
    for _ in range(iterations):
        down = pygame.transform.smoothscale(
            surf,
            (max(1, int(size[0] * scale)), max(1, int(size[1] * scale)))
        )
        surf = pygame.transform.smoothscale(down, size)
    return surf


def make_vignette(width: int, height: int) -> pygame.Surface:
    """Create a radial vignette mask (white center to black edges)."""
    vig = pygame.Surface((width, height), pygame.SRCALPHA)
    cx, cy = width / 2, height / 2
    maxdist = math.hypot(cx, cy)
    for y in range(height):
        for x in range(width):
            d = math.hypot(x - cx, y - cy)
            # intensity falls off quadratically with distance
            val = int(255 * (1 - (d / maxdist) ** 2))
            if val < 0:
                val = 0
            vig.set_at((x, y), (val, val, val, 255))
    return vig


def shift_hue(color: tuple, shift: float) -> tuple:
    """Rotate the hue of an RGBA color by shift amount (0..1)."""
    r, g, b, a = color
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    h = (h + shift) % 1.0
    r2, g2, b2 = colorsys.hsv_to_rgb(h, s, v)
    return (int(r2 * 255), int(g2 * 255), int(b2 * 255), a)


def add_noise(surface: pygame.Surface, amount: int = 1000, max_alpha: int = 30):
    """Add random noise/grain to surface."""
    noise = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    w, h = surface.get_size()
    for _ in range(amount):
        x = random.randrange(w)
        y = random.randrange(h)
        a = random.randint(0, max_alpha)
        noise.set_at((x, y), (255, 255, 255, a))
    surface.blit(noise, (0, 0))


def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation between a and b."""
    return a + (b - a) * t


def lerp_color(c1: tuple, c2: tuple, t: float) -> tuple:
    """Linearly interpolate between two colors."""
    return (
        int(lerp(c1[0], c2[0], t)),
        int(lerp(c1[1], c2[1], t)),
        int(lerp(c1[2], c2[2], t)),
        int(lerp(c1[3], c2[3], t))
    )


def draw_gradient_line(
    surface: pygame.Surface,
    start_pos: tuple,
    end_pos: tuple,
    color_a: tuple,
    color_b: tuple,
    width: int = 2,
    segments_per_px: float = 0.5
):
    """Draw a line with gradient color interpolation."""
    x1, y1 = start_pos
    x2, y2 = end_pos
    dx = x2 - x1
    dy = y2 - y1
    dist = math.hypot(dx, dy)
    if dist == 0:
        return
    
    # determine number of segments (controls smoothness)
    steps = max(1, int(dist * segments_per_px))
    for i in range(steps):
        t0 = i / steps
        t1 = (i + 1) / steps
        sx = x1 + dx * t0
        sy = y1 + dy * t0
        ex = x1 + dx * t1
        ey = y1 + dy * t1
        # color at midpoint gives smoother appearance
        tm = (t0 + t1) / 2
        col = lerp_color(color_a, color_b, tm)
        pygame.draw.line(surface, col, (sx, sy), (ex, ey), width)
