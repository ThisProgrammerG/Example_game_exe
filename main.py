import sys
import json
from itertools import cycle
from pathlib import Path
from typing import NamedTuple

import pygame

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    ASSET_DIRECTORY = Path(sys._MEIPASS) / "assets"
else:
    ASSET_DIRECTORY = Path(__file__).parent / "assets"

IMAGE_DIRECTORY = ASSET_DIRECTORY / "images"


class Animation:
    def __init__(self, images, frame_rate):
        self.images = cycle(images)
        self.time_elapsed = 0
        self.last_time = 0
        self.frame_rate = frame_rate
        self._image = next(self.images)

    @property
    def image(self):
        return self._image

    def update(self, delta_time):
        self.time_elapsed += delta_time
        if self.time_elapsed >= 1 / self.frame_rate:
            self._image = next(self.images)
            self.time_elapsed = 0


class Witch:
    def __init__(self, animation, position):
        self.animation = animation
        self.rect = self.image.get_rect(center=position)

    @property
    def image(self):
        return self.animation.image

    def update(self, delta_time):
        self.animation.update(delta_time)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Text:
    def __init__(self, font, text, position, color):
        self.font = font
        self.text = text
        self.position = position
        self.color = color
        self._image = None
        self.rect = None

        self.render()

    @property
    def image(self):
        return self._image

    def render(self):
        self._image = self.font.render(self.text, True, self.color)
        self.rect = self._image.get_rect(center=self.position)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class SpriteSpecification(NamedTuple):
    rows: int
    columns: int
    scale: int
    frame_rate: int


def load_sprite_sheet(path):
    surface = pygame.image.load(path).convert_alpha()
    surface_rect = surface.get_rect()

    json_path = path.with_suffix(".json")
    with open(json_path) as file:
        specifications = json.load(file)

    sprite_specifications = SpriteSpecification(*specifications.values())

    if sprite_specifications.scale > 1:
        surface = pygame.transform.scale_by(surface, sprite_specifications.scale)
        surface_rect = surface.get_rect()

    width = surface_rect.width // sprite_specifications.columns
    height = surface_rect.height // sprite_specifications.rows

    sprite_sheet = []
    for row in range(0, surface_rect.height, height):
        for column in range(0, surface_rect.width, width):
            rect = (column, row), (width, height)
            image = surface.subsurface(rect)
            sprite_sheet.append(image)

    return Animation(sprite_sheet, frame_rate=sprite_specifications.frame_rate)


def run():
    display = pygame.display.get_surface()
    display_rect = display.get_rect()
    font = pygame.font.SysFont("", 72)
    hello_world = Text(font, "Hello World", display_rect.center, "white")
    animation = load_sprite_sheet(IMAGE_DIRECTORY / "blue_witch" / "B_witch_run.png")
    witch = Witch(animation, (100, display_rect.centery))

    clock = pygame.Clock()
    delta_time = 0
    running = True

    while running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        display.fill("black")
        witch.update(delta_time)
        witch.draw(display)
        hello_world.draw(display)
        pygame.display.flip()
        delta_time = clock.tick() * 0.001


def main():
    pygame.init()
    pygame.display.set_caption("Hello World")
    pygame.display.set_mode((500, 200))

    run()


if __name__ == '__main__':
    main()
