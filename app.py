"""Main wallpaper engine application."""

import pygame
import sys
from .particles import ParticleSystem
from .effects import draw_gradient_line, shift_hue, add_noise


class WallpaperEngine:
    """Main wallpaper engine application."""
    
    def __init__(self, width: int = 800, height: int = 600, fullscreen: bool = False):
        pygame.init()
        
        self.width = width
        self.height = height
        self.fullscreen = fullscreen
        
        # Setup display
        flags = pygame.SRCALPHA
        if fullscreen:
            flags |= pygame.FULLSCREEN
        
        self.screen = pygame.display.set_mode((width, height), flags)
        pygame.display.set_caption("Wallpaper Engine - Particle System")
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60
        
        # Initialize particle system
        self.particles = ParticleSystem(width, height, num_particles=100)
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.particles.handle_mouse_click(mouse_x, mouse_y)
    
    def update(self):
        """Update game state."""
        self.particles.update()
    
    def draw(self):
        """Render frame."""
        # Fade instead of hard clear for motion blur effect
        self.screen.fill((0, 0, 0, 30))
        
        # Create line surface for connections
        line_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Draw particles
        self.particles.draw(self.screen)
        
        # Get particle connections
        connections = self.particles.get_connections()
        
        # Build bucketed lines by alpha to avoid expensive sorts
        buckets = [[] for _ in range(256)]
        for i, j, dist, alpha in connections:
            buckets[alpha].append((i, j, dist))
        
        # Draw lines from low alpha to high alpha
        hue_shift = (pygame.time.get_ticks() * 0.0001) % 1.0
        for alpha in range(256):
            if not buckets[alpha]:
                continue
            a_scale = alpha / 255.0
            for i, j, dist in buckets[alpha]:
                p1 = self.particles.particles[i]
                p2 = self.particles.particles[j]
                c1 = p1.base_color
                c2 = p2.base_color
                c1_scaled = (c1[0], c1[1], c1[2], int(c1[3] * a_scale))
                c2_scaled = (c2[0], c2[1], c2[2], int(c2[3] * a_scale))
                # apply hue shift
                c1_scaled = shift_hue(c1_scaled, hue_shift)
                c2_scaled = shift_hue(c2_scaled, hue_shift)
                # reduce segments for faint lines
                segs_per_px = 0.5 * max(0.25, a_scale)
                draw_gradient_line(
                    line_surface,
                    (p1.x, p1.y),
                    (p2.x, p2.y),
                    c1_scaled,
                    c2_scaled,
                    width=2,
                    segments_per_px=segs_per_px
                )
        
        # Blit connection lines to screen
        self.screen.blit(line_surface, (0, 0))
        
        # Add film grain/noise
        add_noise(self.screen, amount=800, max_alpha=15)
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main application loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)
        
        pygame.quit()
        sys.exit(0)


def main(fullscreen: bool = False):
    """Entry point for the application."""
    app = WallpaperEngine(width=800, height=600, fullscreen=fullscreen)
    app.run()


if __name__ == "__main__":
    main()
