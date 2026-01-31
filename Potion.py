import pygame


class Potion:
    def __init__(self, nom: str, soin: int):

        self.nom = nom
        self.soin = soin

    def soigner(self,pokemon):

        pokemon.pv_actuels+=self.soin

        if pokemon.pv_actuels > pokemon.pv_max:
            pokemon.pv_actuels = pokemon.pv_max
