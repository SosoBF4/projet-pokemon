import pygame

class Pokemon:
    def __init__(self, nom: str, pv_max: int,
                 attaque: int, defense: int, vitesse: int,
                 type_pokemon: int, image_path: str):

        self.nom = nom
        self.pv_max = pv_max
        self.attaque = attaque
        self.defense = defense
        self.vitesse = vitesse
        self.type_pokemon = type_pokemon

        # PV en combat
        self.pv_actuels = pv_max

        # pygame
        self.image_path = image_path