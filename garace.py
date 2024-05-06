import tkinter as tk
from PIL import ImageTk, Image

def fade_out(image_path):
    root = tk.Tk()
    root.title("Fading Image")
    image = Image.open(image_path).convert("RGBA")
    canvas = tk.Canvas(root, width=image.width, height=image.height)
    canvas.pack()
    photo_image = ImageTk.PhotoImage(image)
    image_id = canvas.create_image(0, 0, anchor=tk.NW, image=photo_image)

    for alpha in range(255, -1, -5):
        image.putalpha(alpha)
        photo_image = ImageTk.PhotoImage(image)
        canvas.itemconfig(image_id, image=photo_image)
        root.update()
        root.after(50)

    root.mainloop()

fade_out("img/card1.png")
