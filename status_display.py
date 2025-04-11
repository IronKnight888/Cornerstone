import pygame

class StatusDisplay:
    def __init__(self):
        pygame.init()
        self.width, self.height = 300, 150
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Status Display")

        self.font = pygame.font.SysFont(None, 48)
        self.running = True

        self.color_text = "⚪ NONE"
        self.score = 0

    def update(self, color_text, score):
        self.color_text = color_text
        self.score = score
        self.draw()

    def draw(self):
        self.screen.fill((255, 255, 255))  # white background

        color_surface = self.font.render(f"{self.color_text}", True, (0, 0, 0))
        score_surface = self.font.render(f"Score: {self.score}", True, (0, 0, 0))

        self.screen.blit(color_surface, (20, 30))
        self.screen.blit(score_surface, (20, 80))

        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def close(self):
        pygame.quit()
