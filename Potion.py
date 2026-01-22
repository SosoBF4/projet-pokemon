import pygame


class Potion:
    def __init__(self, id_potion: int, nom: str, soin: int, image_path: str):

        self.id_potion = id_potion
        self.nom = nom
        self.soin = soin

        # pygame
        self.image_path = image_path
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()