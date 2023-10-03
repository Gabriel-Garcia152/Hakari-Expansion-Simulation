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

    def draw(self):
        print(f"Tentativas desde o último Jackpot: {self.tries}")
        if self.ball == "purple":
            slot = random.choice(self.cards)
            for i in range(0, len(self.slots)):
                self.slots[i] = slot
        else:
            for slot in range(0, len(self.slots)):
                self.slots[slot] = random.choice(self.cards)

    def chance_boost(self):
        result_change_odd = random.choice(range(1, 101))
        if result_change_odd <= 50:
            print("Tá se achando demais kkkk")
            print("")
            self.chance = list(range(1,101))
        elif result_change_odd <= 80:
            print("Yume Background")
            print("")
            self.slots[2] = random.choice(range(1, 8))
            self.chance = list(range(1,101))
            self.riichi()
        elif result_change_odd <= 95:
            print("Amanogawa Cut Scene")
            print("")
            self.slots[2] = random.choice(self.cards)
            self.chance = list(range(1, 101))
            self.riichi()
        elif result_change_odd > 95:
            print("Group Indicators")
            print("")
            self.slots[2] = self.slots[0]
            self.chance = list(range(1,101))
            self.riichi()

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

    def riichi(self):
        if self.shoot <= 20:
            print("Transit Card Riichi")
        elif self.shoot <= 50:
            print("Seat Struggle Riichi")
        elif self.shoot < 80:
            print("Potty Emergency Riichi")
        else:
            print("Friday Night Final Train Riichi")

        print(self.slots)
        print("")

        if self.slots[0] == self.slots[1] and self.slots[1] == self.slots[2] and self.slots[0] != 0:
            self.jackpot = True
            self.message = "Seu Sortudo!!"
            self.tries = 0
            self.chance = list(range(1,101))
        elif self.slots[0] == 0:
            self.message = "Você precisa apostar se quiser ganhar!"
        else:
            luck = random.choice(range(1, 101))
            if luck > 90:
                print("Se sentindo sortudo???")
                print("1 - Sim")
                print("2 - Não")
                felling = input()
                if felling == '1':
                    self.chance_boost()
                else:
                    print("Resolveu Correr?")
            else:
                self.message = "Parece que não foi dessa vez!"
        
        self.slots = [0, 0, 0]
