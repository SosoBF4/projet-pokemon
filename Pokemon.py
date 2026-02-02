import pygame

class Pokemon:
    def __init__(self, nom: str, pv_max: int,
                 attaque: int, defense: int, vitesse: int, image_path: str,type_pokemon: int):

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



    def attaquer(self, pokemon_adverse):
            # multiplicateur par défaut
            multiplicateur = 1
    
            # FEU
            if self.type_pokemon == 2:
                if pokemon_adverse.type_pokemon == 3:      # PLANTE
                    multiplicateur = 2
                elif pokemon_adverse.type_pokemon in (1, 2):  # EAU ou FEU
                    multiplicateur = 0.5
    
            # EAU
            elif self.type_pokemon == 1:
                if pokemon_adverse.type_pokemon == 2:      # FEU
                    multiplicateur = 2
                elif pokemon_adverse.type_pokemon == 3:    # PLANTE
                    multiplicateur = 0.5
    
            # ELECTRIQUE
            elif self.type_pokemon == 4:
                if pokemon_adverse.type_pokemon == 1:      # EAU
                    multiplicateur = 2
                elif pokemon_adverse.type_pokemon in (3, 4):  # PLANTE ou ELECTRIQUE
                    multiplicateur = 0.5
    
            # PLANTE
            elif self.type_pokemon == 3:
                if pokemon_adverse.type_pokemon == 1:      # EAU
                    multiplicateur = 2
                elif pokemon_adverse.type_pokemon in (2, 3):  # FEU ou PLANTE
                    multiplicateur = 0.5
    
            # calcul des dégâts

            base = (self.attaque // 2) - (pokemon_adverse.defense // 2)
            base = max(1, base)
            

            degats = int((self.attaque * multiplicateur) / 3)
    
            # on enlève les PV
            pokemon_adverse.pv_actuels -= degats
    
            # éviter les PV négatifs
            if pokemon_adverse.pv_actuels < 0:
                pokemon_adverse.pv_actuels = 0
    

    
    
    
    
    
    
            