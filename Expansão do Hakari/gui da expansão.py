import tkinter as tk
import random
from PIL import Image, ImageTk
from lógica_da_expansão import Simular_expansao

EXPANSION = Simular_expansao()

class GameGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Hakari's Expansion")
        self.current_dance_image = None
        self.current_scenario = 0

        self.setup_gui()

    #Setting elements
    def setup_gui(self): 
        self.background = tk.Label(root) 
        self.background.place(x = 0, y = 0)

        self.canvas = tk.Canvas(root, width=80, height=80)
        self.canvas.pack()

        self.message = tk.Label(root, text=EXPANSION.message)
        self.tries_message = tk.Label(root, text=f"Tentativas desde o último Jackpot: {EXPANSION.tries}")
        self.message.pack()
        self.tries_message.pack()

        self.slots = tk.Label(root, text=f"| {EXPANSION.slots[0]} | | {EXPANSION.slots[1]} | | {EXPANSION.slots[2]} |")
        self.slots.pack()

        self.spin_button = tk.Button(root, text="Spin", command=self.spin, width=5, height=1)
        self.riichi_button = tk.Button(root, text="Riichi", command=self.riichi, width=5, height=1)
        self.riichi_button.pack(side="right", padx=100)
        self.spin_button.pack(side="left", padx=100)

        self.load_scenarios()
        self.load_dance_images()
        self.create_dance_label()

    #Setting images
    def load_dance_images(self):
        images = [Image.open(f"Expansão do Hakari\dance images\dance_{i}.png").resize((150, 150)) for i in range(1, 4)]
        self.dance_images = [ImageTk.PhotoImage(img) for img in images]

    def create_dance_label(self):
        self.dance = tk.Label(root, image=self.dance_images[0])
        self.dance.image = self.dance_images[0]
        self.image_index = 0
        self.jackpot_animating = False

    def load_scenarios(self):
        images = [Image.open(f"Expansão do Hakari/scenarios/scenario({i}).png").resize((500, 500)) for i in range(1, 5)]
        self.scenarios = [ImageTk.PhotoImage(img) for img in images]
    
    def update_scenario(self):
        self.background.config(image = self.scenarios[self.current_scenario])
    
    #Setting messsages
    def message_update(self):
        self.message.config(text=EXPANSION.message)

    def tries_message_update(self):
        self.tries_message.config(text=f"Tentativas desde o último Jackpot: {EXPANSION.tries}")

    #Game's main elements
    def reset_game_elements(self):
        self.dance.forget()
        self.jackpot_animating = False
        self.canvas.delete("all")  

    def spin(self):
        self.reset_game_elements()
        EXPANSION.play()
        self.message_update()
        self.tries_message_update()

        final_numbers = [EXPANSION.slots[0], EXPANSION.slots[1], EXPANSION.slots[2]]

        self.animate_slots(final_numbers)
        self.animate_balls()

    def riichi(self):
        self.reroll_unset()
        EXPANSION.set_scenario()
        self.current_scenario = EXPANSION.scenario
        self.update_scenario()
        final_number = EXPANSION.slots[2]
        animation_speed = 100
        total_iterations = 20

        def update_last_number(iteration):
                if iteration < total_iterations:
                    random_number = random.choice(range(1, 8))
                    self.slots.config(text=f"| {EXPANSION.slots[0]} | | {EXPANSION.slots[1]} | | {random_number} |")
                    self.root.after(animation_speed, lambda: update_last_number(iteration + 1))
                else:
                    self.slots.config(text=f"| {EXPANSION.slots[0]} | | {EXPANSION.slots[1]} | | {final_number} |")
                    EXPANSION.riichi()
                    self.message_update()
                    if EXPANSION.jackpot == True:
                        self.animate_dance_images()
                        self.canvas.delete("all")
                    elif EXPANSION.message == "Se sentindo sortudo???":
                        self.reroll_set()

        if EXPANSION.slots[0] != 0:
            update_last_number(0)
        else:
            self.message.config(text="Você precisa jogar se quiser ganhar!")

    def reroll_set(self):
        self.message_update()
        self.spin_button.config(text="Sim!", command=lambda: self.reroll(True))
        self.riichi_button.config(text="Não", command=lambda: self.reroll(False))

    def reroll_unset(self):
        self.spin_button.config(text="Spin", command=self.spin)
        self.riichi_button.config(text="Riichi", command=self.riichi)

    def reroll(self, lucky):
        EXPANSION.chance_boost(lucky)
        if lucky == True and EXPANSION.result_change_odd > 50:
            self.reroll_unset()
            self.riichi()
        else:
            
            self.message_update()
            self.reroll_unset()
                

    #Setting animations        
    def animate_slots(self, final_numbers):
        animation_speed = 50
        total_iterations = 20

        def update_numbers(iteration):
            if iteration < total_iterations:
                random_numbers = [random.choice(range(1, 8)) for _ in range(3)]
                self.slots.config(text=f"| {random_numbers[0]} | | {random_numbers[1]} | | {random_numbers[2]} |")
                self.root.after(animation_speed, lambda: update_numbers(iteration + 1))
            else:
                self.slots.config(text=f"| {final_numbers[0]} | | {final_numbers[1]} | | ? |")
                self.message_update()

        update_numbers(0)

    def animate_balls(self):
        x1, y1 = 25, 25
        animation_speed = 50

        def move_ball(x, y):
            self.canvas.delete("ball")
            self.canvas.create_oval(x, y, x - 50, y + 50, fill=EXPANSION.ball, tags="ball")
            x += 5
            if x < 70:
                self.root.after(animation_speed, lambda: move_ball(x, y))

        move_ball(x1, y1)

    #Winning animation
    def animate_dance_images(self):
        self.dance.pack()
        def toggle_image():
            if self.jackpot_animating:
                self.image_index = (self.image_index + 1) % len(self.dance_images)
                self.current_dance_image = self.dance_images[self.image_index]
                self.dance.config(image=self.current_dance_image)
                self.root.after(120, toggle_image)

        self.jackpot_animating = True
        toggle_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = GameGui(root)
    root.geometry("500x500")
    root.mainloop()
