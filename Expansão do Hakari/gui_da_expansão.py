import tkinter as tk
import random
from PIL import Image, ImageTk
from lógica_da_expansão import SimulateExpansion

EXPANSION = SimulateExpansion()

class GameGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Hakari's Domain Expansion")
        self.current_dance_image = None
        self.current_scenario = 0

        self.setup_gui()

    #Setting elements
    def setup_gui(self): 
        self.background = tk.Label(root, width=500, height=500) 
        self.background.place(x = 0, y = 0)

        self.canvas = tk.Canvas(root, width=80, height=80)
        self.canvas.pack()

        self.message = tk.Label(root, text=EXPANSION.message)
        self.tries_message = tk.Label(root, text=f"Tentativas desde o último Jackpot: {EXPANSION.tries}")
        self.message.pack()
        self.tries_message.pack()

        self.slots = tk.Label(root, text=f"| {EXPANSION.slots[0]} | | {EXPANSION.slots[1]} | | {EXPANSION.slots[2]} |")
        self.slots.pack()

        self.spin_button = tk.Button(root, text="Spin", command=lambda: self.spin(None), width=5, height=1)
        self.spin_button.place(x=205, y=400)
        self.root.bind("<KeyPress-s>", self.spin)

        self.riichi_button = tk.Button(root, text="Riichi", command=lambda: self.riichi(None), width=5, height=1)
        self.riichi_button.place(x=255, y=400)
        self.root.bind("<KeyPress-r>", self.riichi)

        self.load_scenarios()
        self.load_dance_images()
        self.create_dance_label()
        self.update_scenario()

    #***Setting images***
    
    #Loading Dance Images
    def load_dance_images(self):
        images = [Image.open(f"Expansão do Hakari\dance images\dance_{i}.png").resize((150, 150)) for i in range(1, 4)]
        self.dance_images = [ImageTk.PhotoImage(img) for img in images]

    #Creating Dance Label
    def create_dance_label(self):
        self.dance = tk.Label(self.root, image=self.dance_images[0], width=150, height=150)
        self.dance.image = self.dance_images[0]
        self.image_index = 0
        self.jackpot_animating = False

    #Loading Scenario Images
    def load_scenarios(self):
        images = [Image.open(f"Expansão do Hakari/scenarios/scenario({i}).png").resize((500, 500)) for i in range(0, 9)]
        self.scenarios = [ImageTk.PhotoImage(img) for img in images]
    
    #Updating Background Image
    def update_scenario(self):
        self.current_scenario = EXPANSION.scenario_id
        self.background.config(image = self.scenarios[self.current_scenario])
    
    #***Setting messsages***

    #Updating Main Message Label
    def message_update(self):
        self.message.config(text=EXPANSION.message)

    #Updating Tries Message Label
    def tries_message_update(self):
        self.tries_message.config(text=f"Tentativas desde o último Jackpot: {EXPANSION.tries}")

    #***Game's main elements***

    #Reseting Main Game Elements
    def reset_game_elements(self):
        self.dance.place_forget()
        self.jackpot_animating = False
        self.canvas.delete("all")  

    #Spinning Logic
    def spin(self, event=None):
        self.reset_game_elements()
        EXPANSION.play()
        self.message_update()
        self.tries_message_update()
        self.update_scenario()

        final_numbers = [EXPANSION.slots[0], EXPANSION.slots[1], EXPANSION.slots[2]]

        self.animate_slots(final_numbers)
        self.animate_balls()

    #Riichi Stage Logic
    def riichi(self, event=None):
        self.reroll_unset()
        EXPANSION.set_scenario()
        self.update_scenario()

        if EXPANSION.slots[0] != 0:
            self.update_last_number(0)
        else:
            self.message.config(text="Você precisa jogar se quiser ganhar!")

    #Setting Reroll Elements
    def reroll_set(self):
        self.message_update()
        self.spin_button.config(text="Sim!", command=lambda: self.reroll(True))
        self.riichi_button.config(text="Não", command=lambda: self.reroll(False))
        self.root.bind("<KeyPress-s>", lambda event: self.reroll(True))
        self.root.bind("<KeyPress-r>", lambda event: self.reroll(False))

    #Unsetting Reroll Elements
    def reroll_unset(self):
        self.spin_button.config(text="Spin", command=lambda: self.spin(None))
        self.riichi_button.config(text="Riichi", command=lambda: self.riichi(None))
        self.root.bind("<KeyPress-s>", self.spin)
        self.root.bind("<KeyPress-r>", self.riichi)

    #Reroll Logic
    def reroll(self, lucky):
        EXPANSION.result_change(lucky)
        if lucky == True and EXPANSION.result_change_chance > 50:
            self.message_update()
            self.update_scenario()
            self.riichi()
        else:
            self.message_update()
            self.reroll_unset()
                
    #Setting animations    
    def update_last_number(self, iteration):
        self.message_update()
        final_number = EXPANSION.slots[2]
        animation_speed = 100
        total_iterations = 20

        if iteration < total_iterations:
            random_number = random.choice(range(1, 8))
            self.slots.config(text=f"| {EXPANSION.slots[0]} | | {EXPANSION.slots[1]} | | {random_number} |")
            self.root.after(animation_speed, lambda: self.update_last_number(iteration + 1))
        else:
            self.slots.config(text=f"| {EXPANSION.slots[0]} | | {EXPANSION.slots[1]} | | {final_number} |")
            EXPANSION.riichi()
            self.message_update()
            if EXPANSION.jackpot_reached == True:
                self.animate_dance_images()
                self.update_scenario()
                self.canvas.delete("all")
            elif EXPANSION.message == "Acha que pode mudar o jogo???":
                self.reroll_set()

    #Animating Spinning Slots
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

    #Animating Ball's Shoots
    def animate_balls(self):
        x1, y1 = 25, 25
        animation_speed = 50

        def move_ball(x, y):
            self.canvas.delete("ball")
            self.canvas.create_oval(x, y, x - 50, y + 50, fill=EXPANSION.ball_color, tags="ball")
            x += 5
            if x < 70:
                self.root.after(animation_speed, lambda: move_ball(x, y))

        move_ball(x1, y1)

    #Winning Animation 
    def animate_dance_images(self):
        self.dance.place(x=175, y=240)
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