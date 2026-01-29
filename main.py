import pygame
import sqlite3
import random
import sys
from Pokemon import Pokemon
from Potion import Potion

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

        self.button_rect2= pygame.Rect(450, 350, 250, 70)

        #pokemon
        self.pokemon={}

        #liste pokemon joeur

        self.player1=[]
        self.player2=[]

        self.potion1=[]
        self.potion2=[]

        self.liste_choix1={}
        self.liste_choix2={}

        self.pokemon_actuel1=[]
        self.pokemon_actuel2=[]

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


        #choix des pokemon


        cles = random.sample(list(self.pokemon.keys()), 5)
        for cle in cles:
            self.liste_choix1[cle] = self.pokemon[cle]
        
        cles = random.sample(list(self.pokemon.keys()), 5)
        for cle in cles:
            self.liste_choix2[cle] = self.pokemon[cle]
        
        for nom in self.liste_choix1:
            stats = self.liste_choix1[nom]
            self.player1.append(
                Pokemon(
                    nom,
                    stats[0],  # pv
                    stats[1],  # attaque
                    stats[2],  # defense
                    stats[3],  # vitesse
                    stats[4],  # image
                    stats[5]   # type
                )
            )
        
        for nom in self.liste_choix2:
            stats = self.liste_choix2[nom]
            self.player2.append(
                Pokemon(
                    nom,
                    stats[0],
                    stats[1],
                    stats[2],
                    stats[3],
                    stats[4],
                    stats[5]
                )
            )

        self.pokemon_actuel1.append(self.player1[0])
        self.pokemon_actuel2.append(self.player2[0])

        

        conn = sqlite3.connect("./sql/pokemon.db")
        cur = conn.cursor()
        
        cur.execute("""
            SELECT nom, soin
            FROM potion
        """)
        
        row = cur.fetchone()  # ✅ première ligne uniquement

        nom = row[0]     # ✅ variable nom
        soin = row[1]    # ✅ variable soin 
    
        conn.close()

        for i in range(2):

            self.potion1.append(Potion(nom,soin))

        for i in range(2):
            self.potion2.append(Potion(nom,soin))


        


        



    

    
    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

            if self.state == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(event.pos):
                        self.state = "preparation"

            if self.state == "preparation":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect2.collidepoint(event.pos):
                        self.state = "combat"

    def update(self):
        pass

    
    
    def draw_menu(self):
        
        background = pygame.image.load("./image/menu.png").convert()
        # Agrandir à la taille de la fenêtre (1200x800)
        background = pygame.transform.scale(background, (1200, 900))
        # Afficher le fond
        self.screen.blit(background, (0, 0))

        



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


        player1 = self.button_font.render("Player1", True, (255, 223, 100))
        self.screen.blit(player1, (170, 80))

        
        if self.player1:

            positions1 = [(100,200), (300,200), (100,400), (300,400), (200,600)]  # 5 positions
            for i, nom in enumerate(self.liste_choix1):
                pos = positions1[i]
                img_path = self.liste_choix1[nom][4]
                img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.scale(img, (150,150))
                self.screen.blit(img, pos)
            
            
            
            


        player2 = self.button_font.render("Player2", True, (255, 223, 100))
        self.screen.blit(player2, (880, 80))




        if self.player2:
            positions2 = [(700,200), (900,200), (700,400), (900,400), (800,600)]  # 5 positions
            for i, nom in enumerate(self.liste_choix2):
                pos = positions2[i]
                img_path = self.liste_choix2[nom][4]
                img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.scale(img, (150,150))
                self.screen.blit(img, pos)

        
        
        
        pygame.draw.rect(self.screen, (100, 0, 0), self.button_rect2, border_radius=15)
        pygame.draw.rect(self.screen, (0, 0, 0), self.button_rect2, 4, border_radius=15)
        text_surface = self.button_font.render("Combattre", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.button_rect2.center)
        self.screen.blit(text_surface, text_rect)



    def draw_combat(self):
        background = pygame.image.load("./image/fond_combat.png").convert()
        # Agrandir à la taille de la fenêtre (1200x800)
        background = pygame.transform.scale(background, (1200, 900))
        # Afficher le fond
        self.screen.blit(background, (0, 0))


        player1_barre=pygame.draw.rect(self.screen, (255, 255, 255), (140, 240, 350, 120),border_radius=25 )
        player2_barre=pygame.draw.rect(self.screen, (255, 255, 255), (800, 610, 350, 120),border_radius=25 )

        pourcentage1=self.pokemon_actuel1[0].pv_actuels/self.pokemon_actuel1[0].pv_max
        largeur_barre1 = int(310 * pourcentage1)
        pygame.draw.rect(
        self.screen,
        (0, 200, 0),                 # vert
        (160, 290, largeur_barre1, 15),
        border_radius=8
        )     


        Pokemon1_titre = pygame.font.SysFont("arial", 28, True).render(self.pokemon_actuel1[0].nom, True, (0, 0, 0))
        self.screen.blit(
            Pokemon1_titre,
            Pokemon1_titre.get_rect(topleft=player1_barre.topleft)
        )

   

        Pokemon2_titre = pygame.font.SysFont("arial", 28, True).render(self.pokemon_actuel2[0].nom, True, (0, 0, 0))
        self.screen.blit(
            Pokemon2_titre,
            Pokemon2_titre.get_rect(topleft=player2_barre.topleft)
        )


        pourcentage2=self.pokemon_actuel2[0].pv_actuels/self.pokemon_actuel2[0].pv_max
        largeur_barre2 = int(310 * pourcentage2)
        pygame.draw.rect(
        self.screen,
        (0, 200, 0),                 # vert
        (820, 660, largeur_barre2, 15),
        border_radius=8

        )


        pokemon1 = pygame.image.load(str(self.pokemon_actuel1[0].image_path)).convert_alpha()
        pokemon1 = pygame.transform.scale(pokemon1, (300, 300))  # ← taille ici
        self.screen.blit(pokemon1, (140, 440))


        pokemon2 = pygame.image.load(str(self.pokemon_actuel2[0].image_path)).convert_alpha()
        pokemon2 = pygame.transform.scale(pokemon2, (300, 350))  # ← taille ici
        self.screen.blit(pokemon2, (800, 240))
        


        
        
    

    
    
    def display(self):

        
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "preparation":
            self.draw_preparation()

        elif self.state == "combat":
            self.draw_combat()


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
