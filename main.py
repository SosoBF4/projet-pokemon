import pygame
import sys

# Initialisation de Pygame
pygame.init()

class Game:
    def __init__(self):
        self.run = True
        self.clock = pygame.time.Clock()

        # Créer la fenêtre
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Mon Jeu")



    def event(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False




    def update(self):
        # Mettre à jour le joueur et obstacles

        pass


    def display(self):
        # Afficher le fond et les objets
        self.screen.fill((0, 0, 0))  # fond noir par défaut

        pygame.display.flip()

    def Run(self):
        while self.run:
            self.event()
            self.update()
            self.display()
            self.clock.tick(60)  # FPS

# ------------------- Lancer le jeu -------------------
Jeu = Game()
Jeu.Run()

pygame.quit()
sys.exit()
