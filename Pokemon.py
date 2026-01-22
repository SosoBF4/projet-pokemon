import pygame

class Pokemon:
    def __init__(self, id_pokemon: int, nom: str, pv_max: int,
                 attaque: int, defense: int, vitesse: int,
                 id_type: int, image_path: str):

        self.id_pokemon = id_pokemon
        self.nom = nom
        self.pv_max = pv_max
        self.attaque = attaque
        self.defense = defense
        self.vitesse = vitesse
        self.id_type = id_type

        # PV en combat
        self.pv_actuels = pv_max

        # pygame
        self.image_path = image_path
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()