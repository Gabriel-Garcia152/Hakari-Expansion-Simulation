import random

class Simular_expansao:
    def __init__(self):
        self.cards = list(range(1, 8))
        self.chance = list(range(1,101))
        self.ball = None
        self.shoot = 0
        self.slots = [0, 0, 0]
        self.tries = 0
        self.message = "Se sente com sorte?"
        self.jackpot = False
        self.scenario = 0
        self.result_change_odd = 0

    def draw(self):
        if self.ball == "purple":
            slot = random.choice(self.cards)
            for i in range(0, len(self.slots)):
                self.slots[i] = slot
        else:
            for slot in range(0, len(self.slots)):
                self.slots[slot] = random.choice(self.cards)

    def chance_boost(self, felling_lucky):
        if felling_lucky == True:
            self.result_change_odd = random.choice(range(1, 101))
            if self.result_change_odd <= 50:
                self.message = "Tá se achando demais kkkk"
                self.chance = list(range(1,101))
                self.slots = [0, 0, 0]
            elif self.result_change_odd <= 80:
                self.scenario = 4 #Yume Background
                self.slots[2] = random.choice(range(1, 8))
                self.chance = list(range(1,101))
                self.riichi()
            elif self.result_change_odd <= 95:
                self.scenario = 5 #Amanogawa Cut Scene
                self.slots[2] = random.choice(self.cards)
                self.chance = list(range(1, 101))
                self.riichi()
            elif self.result_change_odd > 95:
                self.scenario = 6 #Group Indicators
                self.slots[2] = self.slots[0]
                self.chance = list(range(1,101))
                self.riichi()
        else:
            self.message = "Resolveu Correr?"

    def play(self):
        self.jackpot = False
        self.shoot = random.choice(self.chance)
        if self.tries != 0:
            self.chance = list(range(self.shoot, 101))

        self.tries += 1

        if self.shoot <= 50:
            self.ball = "green"
            self.cards = list(range(1, 8))
        elif self.shoot > 50 and self.shoot <= 75:
            self.ball = "red"
            self.cards = list(range(3, 8))
        elif self.shoot > 75 and self.shoot <= 99:
            self.ball = "yellow"
            self.cards = list(range(2, 5))
        else:
            self.ball = "purple"

        self.draw()

        self.message = "Se sente com sorte?"
        print(self.ball)
        print(f"{self.slots[0]} {self.slots[1]}")
        print("")

    def set_scenario(self):
        if self.shoot <= 20:
            self.scenario = 0 #Transit Card Riichi
        elif self.shoot <= 50:
            self.scenario = 1 #Seat Struggle Riichi
        elif self.shoot < 80:
            self.scenario = 2 #Potty Emergency Riichi
        else:
            self.scenario = 3 #Friday Night Final Train Riichi

    def riichi(self):
        if len(set(self.slots)) == 1 and self.slots[0] != 0:
            self.jackpot = True
            self.message = "Seu Sortudo!!"
            self.tries = 0
            self.chance = list(range(1,101))
            self.slots = [0, 0, 0]
        elif self.slots[0] == 0:
            self.message = "Você precisa apostar se quiser ganhar!"
        else:
            luck = random.choice(range(1, 101))
            if luck > 90:
                self.message = "Se sentindo sortudo???"
            else:
                self.message = "Parece que não foi dessa vez!"
                self.slots = [0, 0, 0]
