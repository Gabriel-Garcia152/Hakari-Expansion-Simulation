import random

class SimulateExpansion:
    def __init__(self):
        #Visual Elements
        self.cards = list(range(1, 8))
        self.slots = [0, 0, 0]
        self.ball_color = None

        #Chance Related Elements
        self.jackpot_reached = False
        self.current_jackpot_chance = 0
        self.increasing_jackpot_chance = list(range(1,101))
        self.result_change_chance = 0
        
        #Message Elements
        self.tries = 0
        self.message = "Se sente com sorte?"

        #Background Image ID
        self.scenario_id = 0

    def draw_cards(self):
        if self.ball_color == "purple":
            #Guaranted Jackpot if ball color equals purple
            slot = random.choice(self.cards)
            for i in range(0, len(self.slots)):
                self.slots[i] = slot
        else:
            for slot in range(0, len(self.slots)):
                self.slots[slot] = random.choice(self.cards)

    def result_change(self, felling_lucky):
        if felling_lucky == True:
            self.result_change_chance = random.choice(range(0, 101))
            if self.result_change_chance <= 30:
                self.message = "Tá se achando demais kkkk"
                self.result_change_chance = 0
                self.slots = [0, 0, 0]
            elif self.result_change_chance <= 50:
                self.set_scenario()
                self.slots[2] = random.choice(range(1, 8))
                self.debug("result_change")
                self.result_change_chance = 0
            elif self.result_change_chance <= 75:
                self.set_scenario("result_change")
                self.slots[2] = random.choice(self.cards)
                self.debug("result_change")
                self.result_change_chance = 0
            elif self.result_change_chance > 75:
                self.set_scenario()
                self.slots[1] = self.slots[0]
                self.slots[2] = self.slots[0]
                self.debug("result_change")
                self.increasing_jackpot_chance = list(range(1,101))
                self.result_change_chance = 0
        else:
            self.message = "Resolveu Correr?"

    def play(self):
        self.jackpot_reached = False
        self.scenario_id = 0
        self.current_jackpot_chance = random.choice(self.increasing_jackpot_chance)
        if self.tries != 0:
            self.increasing_jackpot_chance = list(range(self.current_jackpot_chance, 101))

        self.tries += 1

        if self.current_jackpot_chance <= 50:
            self.ball_color = "green"
            self.cards = list(range(1, 8))
        elif self.current_jackpot_chance > 50 and self.current_jackpot_chance <= 75:
            self.ball_color = "red"
            self.cards = list(range(3, 8))
        elif self.current_jackpot_chance > 75 and self.current_jackpot_chance <= 99:
            self.ball_color = "yellow"
            self.cards = list(range(2, 5))
        else:
            self.ball_color = "purple"

        self.draw_cards()

        self.message = "Se sente com sorte?"
        self.debug("play")

    def set_scenario(self):
        if self.result_change_chance == 0 and not self.jackpot_reached:
            if self.current_jackpot_chance <= 20:
                self.scenario_id = 1 #Transit Card Riichi
            elif self.current_jackpot_chance <= 50:
                self.scenario_id = 2 #Seat Struggle Riichi
            elif self.current_jackpot_chance < 80:
                self.scenario_id = 3 #Potty Emergency Riichi
            else:
                self.scenario_id = 4 #Friday Night Final Train Riichi
        elif not self.jackpot_reached:
            if self.result_change_chance <= 50:
                self.scenario_id = 5 #Yume Background
            elif self.result_change_chance <= 75:
                self.scenario_id = 6 #Amanogawa Cut Scene
            else:
                self.scenario_id = 7 #Group Indicators
        else:
            self.scenario_id = 8 #Jackpot scenario

    def riichi(self):
        if len(set(self.slots)) == 1 and self.slots[0] != 0:
            self.jackpot_reached = True
            self.debug("riichi")
            self.set_scenario()
            self.jackpot_event()
        elif self.slots[0] == 0:
            self.message = "Você precisa apostar se quiser ganhar!"
        else:
            luck = random.choice(range(1, 101))
            if luck > 30:
                self.message = "Acha que pode mudar o jogo???"
            else:
                self.message = "Parece que não foi dessa vez!"

    #Reset variables after winning
    def jackpot_event(self):
        self.message = "Seu Sortudo!!"
        self.tries = 0
        self.increasing_jackpot_chance = list(range(1,101))
        self.slots = [0, 0, 0]
        self.debug("jackpot_event")

    def debug(self, called):
        print("")
        print(f"Chamado por {called}")
        print(f"Mensagem: '{self.message}'")
        print(f"Tentativas: {self.tries}")
        print(f"Slots: | {self.slots[0]} | {self.slots[1]} | {self.slots[2]} |")
        print(f"Cor: {self.ball_color}")
        print(f"Chance de Jackpot: {self.current_jackpot_chance}")
        print(f"ID do Cenário: {self.scenario_id}")
        print(f"Chance de Reroll: {self.result_change_chance}")
        print("")