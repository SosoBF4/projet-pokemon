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

        self.button_rect3 = pygame.Rect(400, 100, 400, 110)

        self.button_attaque = pygame.Rect(50, 100, 200, 60)

        self.button_attaque2 = pygame.Rect(600, 100, 200, 60)

        self.button_potion= pygame.Rect(320, 100, 200, 60)
        
        
        self.button_potion2= pygame.Rect(870, 100, 200, 60)



        pygame.mixer.init()     #Music
        pygame.mixer.music.set_volume(0.4)

        self.musique_actuelle = None
        
        
        
        self.musiques = {                     
                    "menu": "./music/Introduction.mp3",
                    "preparation": "./music/Introduction.mp3",
                    "combat": "./music/Combat.mp3",
                    "victoire":"./music/Victoire.mp3"
                }
        
        self.son_retirer = pygame.mixer.Sound("./music/mort.mp3")
        self.son_envoyer = pygame.mixer.Sound("./music/nouveau.mp3")
        
        self.son_retirer.set_volume(0.6)
        self.son_envoyer.set_volume(0.6)


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

        self.choix=[]


        self.tour_player1 = 1

        self.gagnant=""
        self.perdent=""


        self.pokemon_ko = False
        self.timer_ko = 0


    def reset_game(self):
        # états
        self.state = "menu"
        self.tour_player1 = 1
        self.gagnant = ""
        self.perdent = ""
    
        # listes
        self.pokemon.clear()
        self.player1.clear()
        self.player2.clear()
        self.potion1.clear()
        self.potion2.clear()
        self.liste_choix1.clear()
        self.liste_choix2.clear()
        self.pokemon_actuel1.clear()
        self.pokemon_actuel2.clear()
        self.choix.clear()
    
        # recharger tout
        self.charger_pokemon()
    
    
    
    def changer_musique(self, state):
        # menu et preparation = même musique

        
        if state in ("menu", "preparation"):
            musique_voulue = "menu"
        else:
            musique_voulue = state
    
        if self.musique_actuelle != musique_voulue:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.musiques[musique_voulue])
            pygame.mixer.music.play(-1)
            self.musique_actuelle = musique_voulue
    

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
        self.player1.pop(0)
        self.pokemon_actuel2.append(self.player2[0])
        self.player2.pop(0)

        

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

            if self.gagnant!="":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect2.collidepoint(event.pos):
                        self.state = "victoire"

            if self.state == "combat" and event.type == pygame.MOUSEBUTTONDOWN:

                # PLAYER 1
                if self.tour_player1 == 1:
                    if self.button_attaque.collidepoint(event.pos):
                        self.choix.append( "attaque")
                        self.tour_player1 = 2
            
                    elif self.button_potion.collidepoint(event.pos):
                        self.choix.append( "potion")
                        self.tour_player1 = 2
            
                # PLAYER 2
                elif self.tour_player1 == 2:
                    if self.button_attaque2.collidepoint(event.pos):
                        self.choix.append("attaque")
                        self.tour_player1 = 3
            
                    elif self.button_potion2.collidepoint(event.pos):
                        self.choix.append(("potion"))
                        self.tour_player1 = 3



            if self.state == "victoire":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.button_rect3.collidepoint(event.pos):
                            self.reset_game()
   
            
            
            
            
        
            
            
            
            
    def update(self):

        
        if self.pokemon_ko:
            if pygame.time.get_ticks() - self.timer_ko > 1000:
               self.pokemon_ko = False

               # PLAYER 1 KO
               if self.pokemon_actuel1[0].pv_actuels == 0:
                   if self.player1:
                       self.son_retirer.play()
                       self.pokemon_actuel1[0] = self.player1.pop(0)
                       self.son_envoyer.play()
                   else:
                       self.gagnant = "Player2"
                       self.perdent = "Player1"
                       self.state = "victoire"

               # PLAYER 2 KO

               elif self.pokemon_actuel2[0].pv_actuels == 0:
                    if self.player2:
                        self.son_retirer.play()
                        self.pokemon_actuel2[0] = self.player2.pop(0)
                        self.son_envoyer.play()
                    else:
                        self.gagnant = "Player1"
                        self.perdent = "Player2"
                        self.state = "victoire"
              
              
              
              
              
              
              
              
              

        
        
    
        
        
        
        
        
        
        
        
        
        
        
        if len(self.choix) == 2:
            p1 = self.pokemon_actuel1[0]
            p2 = self.pokemon_actuel2[0]
        
            # ----- ACTION PLAYER 1 -----
            if self.choix[0] == "attaque":
                if p1.pv_actuels > 0:
                    p1.attaquer(p2)
        
            elif self.choix[0] == "potion":
                if self.potion1 and p1.pv_actuels > 0:
                    self.potion1[0].soigner(p1)
                    self.potion1.pop(0)
        
            # ----- ACTION PLAYER 2 -----
            if self.choix[1] == "attaque":
                if p2.pv_actuels > 0:
                    p2.attaquer(p1)
        
            elif self.choix[1] == "potion":
                if self.potion2 and p2.pv_actuels > 0:
                    self.potion2[0].soigner(p2)
                    self.potion2.pop(0)
        
            # ----- FIN DU TOUR -----
            self.choix.clear()
            self.tour_player1 = 1


        # PLAYER 1 KO
        if self.pokemon_actuel1[0].pv_actuels <= 0:
            self.pokemon_actuel1[0].pv_actuels = 0
            if self.player1:  # il reste des Pokémon
                self.son_retirer.play()
                pygame.time.delay(3000)
                self.son_envoyer.play()
                pygame.time.delay(1000)
                self.pokemon_actuel1[0] = self.player1.pop(0)
            else:  # plus de Pokémon → Player2 gagne
                self.gagnant = "Player2"
                self.perdent= "Player1"
                self.state = "victoire"

        # PLAYER 2 KO
        if self.pokemon_actuel2[0].pv_actuels <= 0:
            self.pokemon_actuel2[0].pv_actuels = 0
            if self.player2:  # il reste des Pokémon
                self.son_retirer.play()
                pygame.time.delay(3000)
                self.son_envoyer.play()
                pygame.time.delay(1000)
                self.pokemon_actuel2[0] = self.player2.pop(0)
            else:  # plus de Pokémon → Player1 gagne
                self.gagnant = "Player1"
                self.perdent= "Player2"
                self.state = "victoire"


        
        
        
        

        

        
        

        
        
        
        

        

        
        
        self.changer_musique(self.state)


        






            

        
                

        
        
    
        
        
        
        
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


        self.pokemon_name_font = pygame.font.SysFont("arial", 18, True)

        
        if self.player1:
            positions1 = [(100,200), (300,200), (100,400), (300,400), (200,600)]
        
            for i, nom in enumerate(self.liste_choix1):
                x, y = positions1[i]
        
                # Image
                img_path = self.liste_choix1[nom][4]
                img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.scale(img, (150,150))
                self.screen.blit(img, (x, y))
        
                # Nom du Pokémon
                nom_txt = self.pokemon_name_font.render(nom, True, (255, 223, 100))
                nom_rect = nom_txt.get_rect(center=(x + 75, y + 165))
                self.screen.blit(nom_txt, nom_rect)

        
        
        
        
        
        
        
        
            
            
            


        player2 = self.button_font.render("Player2", True, (255, 223, 100))
        self.screen.blit(player2, (880, 80))




        if self.player2:
            positions2 = [(700,200), (900,200), (700,400), (900,400), (800,600)]
        
            for i, nom in enumerate(self.liste_choix2):
                x, y = positions2[i]
        
                # Image
                img_path = self.liste_choix2[nom][4]
                img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.scale(img, (150,150))
                self.screen.blit(img, (x, y))
        
                # Nom du Pokémon
                nom_txt = self.pokemon_name_font.render(nom, True, (255, 223, 100))
                nom_rect = nom_txt.get_rect(center=(x + 75, y + 165))
                self.screen.blit(nom_txt, nom_rect)
        
        
        
        
        
        
        

        
        
        
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


        Pokemon1_titre = pygame.font.SysFont("arial", 28, True).render(
        self.pokemon_actuel1[0].nom, True, (0, 0, 0)
        )
        self.screen.blit(
            Pokemon1_titre,
            Pokemon1_titre.get_rect(topleft=(player1_barre.left + 10, player1_barre.top + 10))
        )
        
        Pokemon2_titre = pygame.font.SysFont("arial", 28, True).render(
            self.pokemon_actuel2[0].nom, True, (0, 0, 0)
        )
        self.screen.blit(
            Pokemon2_titre,
            Pokemon2_titre.get_rect(topleft=(player2_barre.left + 10, player2_barre.top + 10))
        )
        


        vie1 = pygame.font.SysFont("arial", 28, True).render(
        f"{self.pokemon_actuel1[0].pv_actuels}/{self.pokemon_actuel1[0].pv_max}",
        True,
        (0, 0, 0)
        )
        self.screen.blit(
            vie1,
            vie1.get_rect(
                bottomleft=(player1_barre.left + 10, player1_barre.bottom - 10)
            )
        )
        
        vie2 = pygame.font.SysFont("arial", 28, True).render(
            f"{self.pokemon_actuel2[0].pv_actuels}/{self.pokemon_actuel2[0].pv_max}",
            True,
            (0, 0, 0)
        )
        self.screen.blit(
            vie2,
            vie2.get_rect(
                bottomleft=(player2_barre.left + 10, player2_barre.bottom - 10)
            )
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

        #Commande 

        if self.tour_player1==1:

            player1 = self.button_font.render("Player1", True, (0, 0, 255))
            self.screen.blit(player1, (250, 10))
    
            pygame.draw.rect(self.screen, (180, 30, 30), self.button_attaque, border_radius=15)
            pygame.draw.rect(self.screen, (180, 30, 30), self.button_attaque, 4, border_radius=15)
            text_surface = self.button_font.render("Attaquer", True, (255, 255, 255))
            text_attaque = text_surface.get_rect(center=self.button_attaque.center)
            self.screen.blit(text_surface, text_attaque)
    
            if pourcentage1<0.8 and len(self.potion1)!=0:
                pygame.draw.rect(self.screen, (40, 170, 90), self.button_potion, border_radius=15)
                pygame.draw.rect(self.screen, (40, 170, 90), self.button_potion, 4, border_radius=15)
                text_surface = self.button_font.render("Soigner", True, (255, 255, 255))
                text_potion = text_surface.get_rect(center=self.button_potion.center)
                self.screen.blit(text_surface, text_potion)

        if self.tour_player1 ==2:

            player2 = self.button_font.render("Player2", True, (255, 0, 0))
            self.screen.blit(player2, (770, 10))


            pygame.draw.rect(self.screen, (180, 30, 30), self.button_attaque2, border_radius=15)
            pygame.draw.rect(self.screen, (180, 30, 30), self.button_attaque2, 4, border_radius=15)
            text_surface = self.button_font.render("Attaquer", True, (255, 255, 255))
            text_attaque = text_surface.get_rect(center=self.button_attaque2.center)
            self.screen.blit(text_surface, text_attaque)

            if pourcentage2<0.8 and len(self.potion2)!=0:
                pygame.draw.rect(self.screen, (40, 170, 90), self.button_potion2, border_radius=15)
                pygame.draw.rect(self.screen, (40, 170, 90), self.button_potion2, 4, border_radius=15)
                text_surface = self.button_font.render("Soigner", True, (255, 255, 255))
                text_potion = text_surface.get_rect(center=self.button_potion2.center)
                self.screen.blit(text_surface, text_potion)

    
    def draw_victoire(self):

        background = pygame.image.load("./image/victoire.png").convert()
        # Agrandir à la taille de la fenêtre (1200x800)
        background = pygame.transform.scale(background, (1200, 800))
        # Afficher le fond
        self.screen.blit(background, (0, 0))

        self.date_font = pygame.font.Font(None, 80)

        victoire = self.date_font.render(self.gagnant, True, (255, 223, 100))
        self.screen.blit(victoire, (820, 650))
        
        perdu = self.date_font.render(self.perdent, True, (255, 223, 100))
        self.screen.blit(perdu, (200, 650))

        pygame.draw.rect(self.screen, (220, 0, 0), self.button_rect3, border_radius=15)
        pygame.draw.rect(self.screen, (0, 0, 0), self.button_rect3, 4, border_radius=15)
        text_surface = self.button_font.render("Aller au menu", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.button_rect3.center)
        self.screen.blit(text_surface, text_rect)

        

        
        

        
        

    
        




        

        


        
        
    

    
    
    def display(self):

        
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "preparation":
            self.draw_preparation()

        elif self.state == "combat":
            self.draw_combat()

        elif self.state == "victoire":

            self.draw_victoire()


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
