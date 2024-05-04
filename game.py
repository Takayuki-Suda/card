import random
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class CardGameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("世界一かっこいいカードゲーム")
        self.master.attributes('-fullscreen', True)
        self.master.configure(bg="#333333")  # ウィンドウの背景色を設定
        width = self.master.winfo_screenwidth()
        height = self.master.winfo_screenheight()
        font_size = min(width, height) // 30  # フォントサイズを設定

        # ウィジェットのスタイルを定義
        style = ttk.Style()
        style.configure("Cool.TButton", background="#007bff", foreground="white", font=("Helvetica", font_size))

        # ウィジェットを配置
        self.label = tk.Label(master, text="世界一かっこいいカードゲーム！", font=("Helvetica", font_size), bg="#333333", fg="white")
        self.label.pack(pady=50)

        self.play_button = ttk.Button(master, text="プレイ", command=self.play_game, style="Cool.TButton")
        self.play_button.pack()

    def play_game(self):
        self.master.withdraw()
        game_window = tk.Toplevel(self.master)
        GameWindow(game_window)

class GameWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("ゲーム")
        self.master.attributes('-fullscreen', True)
        self.master.configure(bg="#333333")
        font_size = 16

        self.player1_score = 0
        self.player2_score = 0
        self.player1_card = None
        self.player2_card = None
        self.round_count = 0
        self.player1_hand = [str(i) for i in range(1, 6)]  # プレイヤーの初期手札は1から5までの全ての数字
        self.player2_hand = [str(i) for i in range(1, 6)]  # AIの初期手札は1から5までの全ての数字

        self.label = tk.Label(master, text="各プレイヤーは交互にカードをプレイします。\nカードの最も高い数字を持ったプレイヤーがラウンドに勝ちます。",
                              font=("Helvetica", font_size), bg="#333333", fg="white")
        self.label.pack(pady=20)

        self.player2_hand_label = tk.Label(master, text="AIの手札:", font=("Helvetica", font_size), bg="#333333", fg="white")
        self.player2_hand_label.pack()

        self.player2_hand_display = tk.Label(master, font=("Helvetica", font_size), bg="#333333", fg="white")
        self.player2_hand_display.pack()

        self.button_frame = tk.Frame(self.master, bg="#333333")
        self.button_frame.pack()

        self.result_label = tk.Label(master, text="", font=("Helvetica", 14), bg="#333333", fg="white")
        self.result_label.pack(pady=20)

        self.show_card_buttons()

        # 「次のラウンド」ボタンの上に画像を表示するラベルを作成
        img_hand = Image.open("img/hand_dia.png")
        img_hand = img_hand.resize((200, 200))  # 必要に応じてサイズを調整
        img_hand = img_hand.convert("RGBA")
        img_hand = ImageTk.PhotoImage(img_hand)

        self.hand_label = tk.Label(master, image=img_hand, bg="#333333")
        self.hand_label.image = img_hand
        self.hand_label.pack()

        # 「次のラウンド」ボタンを作成
        self.next_round_button = ttk.Button(self.master, text="次のラウンド", command=self.reset_round, style="Cool.TButton")
        self.next_round_button.pack()

    def show_card_buttons(self):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        card_labels = ["1", "2", "3", "4", "5"]
        for card_label in card_labels:
            if card_label in self.player1_hand:
                # 画像の読み込み
                img = Image.open(f"img/card{card_label}.png")
                # 画像のサイズを変更
                img = img.resize((240, 350))  # 例: 幅150ピクセル、高さ250ピクセルに変更
                # 画像の背景色を透明に設定
                img = img.convert("RGBA")
                img = ImageTk.PhotoImage(img)

                label = tk.Label(self.button_frame, image=img, bg="#333333")
                label.image = img
                label.bind("<Button-1>", lambda event, card=card_label: self.choose_card(card))
                label.pack(side=tk.LEFT, padx=5)


    def choose_card(self, card_label):
        if self.player1_card is None:
            self.player1_card = card_label
            self.player1_hand.remove(card_label)  # 選択したカードをプレイヤーの手札から削除
            self.show_card_buttons()  # カードを選択した後にボタンを再描画
            self.play_round()

    def play_round(self):
        self.round_count += 1
        self.player2_card = random.choice(self.player2_hand)

        result = "引き分けです！"
        if int(self.player1_card) > int(self.player2_card):
            self.player1_score += 1
            result = "プレイヤー1がこのラウンドを勝ちました！"
        elif int(self.player2_card) > int(self.player1_card):
            self.player2_score += 1
            result = "AIがこのラウンドを勝ちました！"

        self.result_label.config(text=f"プレイヤー1のカード: {self.player1_card}\nAIのカード: {self.player2_card}\n{result}")

        if self.round_count == 5:
            self.end_game()  # ラウンドが5回に達したらゲーム終了

    def reset_round(self):
        self.result_label.config(text="")
        self.player1_card = None
        if self.round_count < 5:
            self.update_ai_hand()

    def end_game(self):
        winner = "プレイヤー1" if self.player1_score > self.player2_score else "AI" if self.player2_score > self.player1_score else "引き分け"
        messagebox.showinfo("ゲーム終了", f"プレイヤー1の得点: {self.player1_score}\nAIの得点: {self.player2_score}\n{winner}の勝利！")
        self.master.destroy()

    def update_ai_hand(self):
        if self.player2_card in self.player2_hand:
            self.player2_hand.remove(self.player2_card)
        self.player2_hand_display.config(text=", ".join(self.player2_hand))

def main():
    root = tk.Tk()
    app = CardGameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
