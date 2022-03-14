# TEE PELI TÄHÄN
import pygame
import os
import random
pygame.init()

naytto_korkeus = 500
naytto_leveys = 900
naytto = pygame.display.set_mode((naytto_leveys, naytto_korkeus))

JUOKSU = [pygame.image.load("viljo3.png"),pygame.image.load("viljo3.png")]
HYPPY = pygame.image.load("viljo3.png")
KYYKKY = [pygame.image.load("viljo_kyykky2.png"), pygame.image.load("viljo_kyykky2.png")]

pikku_kisu = [pygame.image.load("pikku_kisu1.1.png"), pygame.image.load("pikku_kisu2.png"), pygame.image.load("pikku_kisu3.png")]
iso_katti = [pygame.image.load("iso_katti1.png"), pygame.image.load("iso_katti2.png"), pygame.image.load("iso_katti3.1.png")]

lintu = [pygame.image.load("birdy2.png"), pygame.image.load("birdy2.png")]

pilvi = pygame.image.load("pilvi.png")

maa = pygame.image.load("maa.png")


class Viljo:
    X_KOHTA = 50
    Y_KOHTA = 285
    Y_KOHTA_KYYKKY = 320
    HYPPY_NOPEUS = 8.5

    def __init__(self):
        self.kyykky_img = KYYKKY
        self.juoksu_img = JUOKSU
        self.hyppy_img = HYPPY

        self.viljo_kyykky = False
        self.viljo_juoksu = True
        self.viljo_hyppy = False

        self.askel_indeksi = 0
        self.hyppy_nopeus = self.HYPPY_NOPEUS
        self.image = self.juoksu_img[0]
        self.viljo_rect = self.image.get_rect()
        self.viljo_rect.x = self.X_KOHTA
        self.viljo_rect.y = self.Y_KOHTA

    def paivita(self, userInput):
        if self.viljo_kyykky:
            self.kyykky()
        if self.viljo_juoksu:
            self.juoksu()
        if self.viljo_hyppy:
            self.hyppy()

        if self.askel_indeksi >= 10:
            self.askel_indeksi = 0

        if userInput[pygame.K_UP] and not self.viljo_hyppy:
            self.viljo_kyykky = False
            self.viljo_juoksu = False
            self.viljo_hyppy = True
        elif userInput[pygame.K_DOWN] and not self.viljo_hyppy:
            self.viljo_kyykky = True
            self.viljo_juoksu = False
            self.viljo_hyppy = False
        elif not (self.viljo_hyppy or userInput[pygame.K_DOWN]):
            self.viljo_kyykky = False
            self.viljo_juoksu = True
            self.viljo_hyppy = False

    def kyykky(self):
        self.image = self.kyykky_img[self.askel_indeksi // 5]
        self.viljo_rect = self.image.get_rect()
        self.viljo_rect.x = self.X_KOHTA
        self.viljo_rect.y = self.Y_KOHTA_KYYKKY
        self.askel_indeksi += 1

    def juoksu(self):
        self.image = self.juoksu_img[self.askel_indeksi // 5]
        self.viljo_rect = self.image.get_rect()
        self.viljo_rect.x = self.X_KOHTA
        self.viljo_rect.y = self.Y_KOHTA
        self.askel_indeksi += 1

    def hyppy(self):
        self.image = self.hyppy_img
        if self.viljo_hyppy:
            self.viljo_rect.y -= self.hyppy_nopeus * 4
            self.hyppy_nopeus -= 0.8
        if self.hyppy_nopeus < - self.HYPPY_NOPEUS:
            self.viljo_hyppy = False
            self.hyppy_nopeus = self.HYPPY_NOPEUS

    def piirra(self, naytto):
        naytto.blit(self.image, (self.viljo_rect.x, self.viljo_rect.y))


class Pilvi:
    def __init__(self):
        self.x = naytto_leveys + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = pilvi
        self.width = self.image.get_width()

    def paivita(self):
        self.x -= peli_nopeus
        if self.x < -self.width:
            self.x = naytto_leveys + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def piirra(self, naytto):
        naytto.blit(self.image, (self.x, self.y))


class Este:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = naytto_leveys

    def paivita(self):
        self.rect.x -= peli_nopeus
        if self.rect.x < -self.rect.width:
            esteet.pop()

    def piirra(self, naytto):
        naytto.blit(self.image[self.type], self.rect)


class PikkuKissa(Este):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 372


class IsoKissa(Este):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 344


class Lintu(Este):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def piirra(self, naytto):
        if self.index >= 9:
            self.index = 0
        naytto.blit(self.image[self.index//5], self.rect)
        self.index += 1


def main():
    global peli_nopeus, x_kohta_tausta, y_kohta_tausta, pisteet, esteet
    juoksu = True
    kello = pygame.time.Clock()
    pelaaja = Viljo()
    pilvi = Pilvi()
    peli_nopeus = 20
    x_kohta_tausta = 100
    y_kohta_tausta = 440
    pisteet = 0
    fontti = pygame.font.SysFont('comic sans', 20)
    esteet = []
    death_count = 0

    def score():
        global pisteet, peli_nopeus
        pisteet += 1
        if pisteet % 100 == 0:
            peli_nopeus += 1

        text = fontti.render("Pisteet: " + str(pisteet), True, (255,130,171))
        textRect = text.get_rect()
        textRect.center = (800, 40)
        naytto.blit(text, textRect)

    def tausta():
        global x_kohta_tausta, y_kohta_tausta
        image_width = maa.get_width()
        naytto.blit(maa, (x_kohta_tausta, y_kohta_tausta))
        naytto.blit(maa, (image_width + x_kohta_tausta, y_kohta_tausta))
        if x_kohta_tausta <= -image_width:
            naytto.blit(maa, (image_width + x_kohta_tausta, y_kohta_tausta))
            x_kohta_tausta = 0
        x_kohta_tausta -= peli_nopeus

    while juoksu:
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                juoksu = False

        naytto.fill((176,226,255))
        userInput = pygame.key.get_pressed()

        pelaaja.piirra(naytto)
        pelaaja.paivita(userInput)

        if len(esteet) == 0:
            if random.randint(0, 2) == 0:
                esteet.append(PikkuKissa(pikku_kisu))
            elif random.randint(0, 2) == 1:
                esteet.append(IsoKissa(iso_katti))
            elif random.randint(0, 2) == 2:
                esteet.append(Lintu(lintu))

        for este in esteet:
            este.piirra(naytto)
            este.paivita()
            if pelaaja.viljo_rect.colliderect(este.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        tausta()

        pilvi.piirra(naytto)
        pilvi.paivita()

        score()

        kello.tick(30)
        pygame.display.update()


def menu(death_count):
    global pisteet
    juoksu = True
    while juoksu:
        naytto.fill((176,226,255))
        font = pygame.font.SysFont('comic sans', 30)
        font2 = pygame.font.SysFont('comic sans', 25)
        font3 = pygame.font.SysFont('comic sans', 40)
        if death_count == 0:
            text3 = font3.render("Viljo the Game", True, (255,130,171))
            text3Rect = text3.get_rect()
            text3Rect.center = (naytto_leveys // 2 , naytto_korkeus // 2-200)
            naytto.blit(text3,text3Rect)
            text = font2.render("Paina mitä vain näppäintä aloittaaksesi", True, (255,130,171))
            text2 = font.render("Ohjaa nuolinäppäimillä ja auta Viljoa kissojen ja lintujen ohi!", True, (255,130,171))
            textRect = text.get_rect()
            textRect.center = (naytto_leveys // 2, naytto_korkeus// 2 +100)
            naytto.blit(text, textRect)
            text2Rect = text2.get_rect()
            text2Rect.center = (naytto_leveys // 2, naytto_korkeus// 2+50)
            naytto.blit(text2, text2Rect)
            naytto.blit(pygame.image.load("viljo_alku.png"), (390, 80))           
        elif death_count > 0:
            text = font2.render("Paina mitä vain näppäintä aloittaaksesi uudelleen", True, (255,130,171))
            score = font.render("Pisteesi: " + str(pisteet), True, (255,130,171))
            havio = font.render("Hävisit pelin...", True, (255,130,171))
            havioRect = havio.get_rect()
            havioRect.center = (naytto_leveys // 2, 30)
            naytto.blit(havio, havioRect)
            scoreRect = score.get_rect()
            scoreRect.center = (naytto_leveys // 2, naytto_korkeus // 2 + 100)
            naytto.blit(score, scoreRect)
            textRect = text.get_rect()
            textRect.center = (naytto_leveys // 2, naytto_korkeus// 2 +60)
            naytto.blit(text, textRect)
            naytto.blit(pygame.image.load("viljo_loppu.png"), (350, 70))
        pygame.display.update()
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                juoksu = False
                pygame.quit()
            if tapahtuma.type == pygame.KEYDOWN:
                main()


menu(death_count=0)