import tkinter as tk
from PIL import ImageTk, Image

def fade_out(image_path):
    root = tk.Tk()
    root.title("Fading Image")

    # 画像を読み込む
    image = Image.open(image_path)
    image = image.convert("RGBA")
    image_with_alpha = add_alpha_channel(image)  # 透明度を追加

    # 画像を表示するキャンバスを作成
    canvas = tk.Canvas(root, width=image.width, height=image.height)
    canvas.pack()

    # 画像をキャンバスに描画
    photo_image = ImageTk.PhotoImage(image_with_alpha)
    image_id = canvas.create_image(0, 0, anchor=tk.NW, image=photo_image)

    # 画像を徐々に消していく
    for alpha in range(255, -1, -5):  # 255から0まで5ずつ減少
        image_with_alpha.putalpha(alpha)
        photo_image = ImageTk.PhotoImage(image_with_alpha)
        canvas.itemconfig(image_id, image=photo_image)
        root.update()  # ウィンドウを更新
        root.after(50)  # ウィンドウを50ミリ秒後に更新

    root.mainloop()

def add_alpha_channel(image):
    """
    画像に透明度チャンネルを追加する
    """
    image_with_alpha = Image.new("RGBA", image.size, (255, 255, 255, 0))
    image_with_alpha.paste(image, (0, 0), image)
    return image_with_alpha

# 画像ファイル名を指定して関数を呼び出す
image_file_name = "img/card1.png"
fade_out(image_file_name)
