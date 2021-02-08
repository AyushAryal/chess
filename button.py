import pygame

class Button:
    def __init__(self, rect, text, font=pygame.font.SysFont(None, 12), bg_color=pygame.Color(0, 0, 0), text_color=pygame.Color(255, 255, 255), callback=lambda _: None):
        self.rect = rect
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.font = font
        self.callback = callback

    @staticmethod
    def draw_rect_alpha(surface, color, rect):
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect(), border_radius=20)
        surface.blit(shape_surf, rect)

    def draw(self, window):
        x, y, width, height = self.rect
        Button.draw_rect_alpha(window, self.bg_color, self.rect)
        text = self.font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=((x*2+width)//2, (2*y+height)//2))
        window.blit(text, text_rect)