import pygame
import sqlite3
import random
import sys

# Initialisation de Pygame
pygame.init()


class Game:
    def __init__(self):
        self.run = True
        self.clock = pygame.time.Clock()

        # Fenêtre
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Pokemon")
        icon = pygame.image.load("image/logo.png").convert_alpha()
        pygame.display.set_icon(icon)

        # État du jeu
        self.state = "menu"  # menu ou game
        # Polices
        self.title_font = pygame.font.SysFont("arial", 120, bold=True)
        self.button_font = pygame.font.SysFont("arial", 40)

        # Bouton
        self.button_rect = pygame.Rect(300, 430, 600, 110)

        #pokemon
        self.pokemon={}

    def charger_pokemon(self):
        conn = sqlite3.connect("./sql/pokemon.db")
        cur = conn.cursor()

        cur.execute("""
            SELECT nom, pv_max, attaque, defense, vitesse, image, id_type
            FROM pokemon
        """)

        for row in cur.fetchall():
            nom = row[0]
            self.pokemon[nom] = list(row[1:])

        conn.close()

    
    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

            if self.state == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(event.pos):
                        self.state = "preparation"

    def update(self):
        pass

    
    
    def draw_menu(self):
        self.screen.fill((155, 0, 0))

        # Titre
        title_surface = self.title_font.render("POKÉMON", True, (255, 204, 0))
        title_rect = title_surface.get_rect(center=(600, 250))
        self.screen.blit(title_surface, title_rect)

        # Bouton
        pygame.draw.rect(self.screen, (220, 0, 0), self.button_rect, border_radius=15)
        pygame.draw.rect(self.screen, (0, 0, 0), self.button_rect, 4, border_radius=15)

        text_surface = self.button_font.render("Commencer les combats", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.button_rect.center)
        self.screen.blit(text_surface, text_rect)

    
    
    def draw_preparation(self):
        # fond bleu à gauche
        pygame.draw.rect(self.screen, (0, 0, 255), (0, 0, 1200 // 2, 800))

        # fond rouge à droite
        pygame.draw.rect(self.screen, (255, 0, 0), (1200 // 2, 0, 1200 // 2, 800))


        player1 = self.button_font.render("Player1", True, (255, 255, 255))
        self.screen.blit(player1, (150, 80))
        player2 = self.button_font.render("Player2", True, (255, 255, 255))
        self.screen.blit(player2, (880, 80))


    
    
    def display(self):

        
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "preparation":
            self.draw_preparation()


        pygame.display.flip()

    def Run(self):
        self.charger_pokemon()
        while self.run:
            self.event()
            self.update()
            self.display()
            self.clock.tick(60)


# ------------------- Lancer le jeu -------------------
Jeu = Game()
Jeu.Run()

pygame.quit()
sys.exit()
