import tkinter as tk
import random
from PIL import Image, ImageTk
from lógica_da_expansão import Simular_expansao

EXPANSION = Simular_expansao()

class GameGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Hakari's Expansion")
        self.current_image = None

        self.setup_gui()

    #setting elements
    def setup_gui(self):
        frame = tk.Frame(root)
        frame.pack()

        self.canvas = tk.Canvas(frame, width=100, height=100)
        self.canvas.pack()

        self.message = tk.Label(frame, text=EXPANSION.message)
        self.tries_message = tk.Label(frame, text=f"Tentativas desde o último Jackpot: {EXPANSION.tries}")
        self.message.pack()
        self.tries_message.pack()

        self.slots = tk.Label(frame, text=f"| {EXPANSION.slots[0]} | | {EXPANSION.slots[1]} | | {EXPANSION.slots[2]} |")
        self.slots.pack()

        spin_button = tk.Button(root, text="Spin", command=self.spin, width=5, height=1)
        riichi_button = tk.Button(root, text="Riichi", command=self.riichi, width=5, height=1)
        riichi_button.pack(side="right", padx=100)
        spin_button.pack(side="left", padx=100)

        self.load_images()
        self.create_dance_label()

    #setting images
    def load_images(self):
        images = [Image.open(f"Expansão do Hakari\dance_{i}.png").resize((150, 150)) for i in range(1, 4)]
        self.photo_images = [ImageTk.PhotoImage(img) for img in images]

    def create_dance_label(self):
        self.dance = tk.Label(root, image=self.photo_images[0])
        self.dance.image = self.photo_images[0]
        self.image_index = 0
        self.jackpot_animating = False
    
    #setting messsages
    def message_update(self):
        self.message.config(text=EXPANSION.message)

    def tries_message_update(self):
        self.tries_message.config(text=f"Tentativas desde o último Jackpot: {EXPANSION.tries}")

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
        x2, y2 = 75, 75
        animation_speed = 50

        def move_ball(x, y):
            self.canvas.delete("all")
            self.canvas.create_oval(x, y, x - 50, y + 50, fill=EXPANSION.ball)
            x += 5  # Ajuste a velocidade da animação alterando esse valor
            if x < 80:  # Ajuste a condição de parada para a animação
                self.root.after(animation_speed, lambda: move_ball(x, y))

        move_ball(x1, y1)

    def riichi(self):
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
                        self.animate_images()
                        self.canvas.delete("all")


        if EXPANSION.slots[0] != 0:
            update_last_number(0)
        else:
            self.message.config(text="Você precisa jogar se quiser ganhar!")

    def animate_images(self):
        self.dance.pack()
        def toggle_image():
            if self.jackpot_animating:
                self.image_index = (self.image_index + 1) % len(self.photo_images)
                self.current_image = self.photo_images[self.image_index]
                self.dance.config(image=self.current_image)
                self.root.after(120, toggle_image)

        self.jackpot_animating = True
        toggle_image()

    
if __name__ == "__main__":
    root = tk.Tk()
    app = GameGui(root)
    root.geometry("700x400")
    root.mainloop()