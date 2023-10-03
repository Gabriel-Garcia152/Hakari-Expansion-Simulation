import tkinter as tk
from PIL import Image, ImageTk
from lógica_da_expansão import Simular_expansao

expansion = Simular_expansao()

class GameGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Hakari's expansion")
        self.current_image = None

        frame = tk.Frame(root)
        frame.pack()

        self.canvas = tk.Canvas(frame, width=100, height=100)
        self.canvas.pack()

        self.message = tk.Label(frame, text=expansion.message)
        self.tries_message = tk.Label(frame, text=f"Tentativas desde o último Jackpot: {expansion.tries}")
        self.message.pack()
        self.tries_message.pack()

        self.slots = tk.Label(frame, text=f"| {expansion.slots[0]} | | {expansion.slots[1]} | | {expansion.slots[2]} |")
        self.slots.pack()

        spin_button = tk.Button(root, text="Spin", command=self.spin, width=5, height=1)
        riichi_button = tk.Button(root, text="Riichi", command=self.riichi, width=5, height=1)
        riichi_button.pack(side="right", padx=100)
        spin_button.pack(side="left", padx=100)

        image1 = Image.open("dance_1.png")
        image2 = Image.open("dance_2.png")
        image3 = Image.open("dance_3.png")

        image1 = image1.resize((image1.width // 3, image1.height // 3))
        image2 = image2.resize((image2.width // 3, image2.height // 3))
        image3 = image3.resize((image3.width // 3, image3.height // 3))

        self.photo1 = ImageTk.PhotoImage(image1)
        self.photo2 = ImageTk.PhotoImage(image2)
        self.photo3 = ImageTk.PhotoImage(image3)

        self.dance = tk.Label(root, image=self.photo1)
        self.dance.image = self.photo1

        self.image_index = 0
        self.images = [self.photo1, self.photo2, self.photo3]

    def message_update(self):
        self.message.config(text=expansion.message)

    def tries_message_update(self):
        self.tries_message.config(text=f"Tentativas desde o último Jackpot: {expansion.tries}")

    def spin(self):
        expansion.play()
        self.slots.config(text=f"| {expansion.slots[0]} | | {expansion.slots[1]} | | ? |")
        self.message_update()
        self.tries_message_update()

        self.canvas.delete("all")

        x1, y1 = 25, 25
        x2, y2 = 75, 75
        self.canvas.create_oval(x1, y1, x2, y2, fill=expansion.ball)

    def riichi(self):
        self.slots.config(text=f"| {expansion.slots[0]} | | {expansion.slots[1]} | | {expansion.slots[2]} |")
        expansion.riichi()
        self.message_update()

        if expansion.jackpot == True:
            self.canvas.delete("all")
            self.animate_images()

    def animate_images(self, iterations=20):
        self.dance.pack()

        def toggle_image():
            self.image_index = (self.image_index + 1) % len(self.images)
            self.current_image = self.images[self.image_index]
            self.dance.config(image=self.current_image)
            iterations_left[0] -= 1
            if iterations_left[0] > 0:
                self.root.after(120, toggle_image)
            if iterations_left[0] == 0:
                self.dance.forget()

        iterations_left = [iterations]
        toggle_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = GameGui(root)
    root.geometry("700x400")
    root.mainloop()
