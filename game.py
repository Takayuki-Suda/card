import random
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from time import strftime

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

        # ゲーム終了ボタンを追加
        self.quit_button = ttk.Button(master, text="ゲームを終了", command=self.quit_game, style="Cool.TButton")
        self.quit_button.pack()

    def play_game(self):
        self.master.withdraw()
        game_window = tk.Toplevel(self.master)
        game_window.focus_force()  # ゲームウィンドウにフォーカスを当てる
        GameWindow(game_window)

    def quit_game(self):
        self.master.destroy()

class GameWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("ゲーム")
        self.master.attributes('-fullscreen', True)
        self.master.configure(bg="#333333")
        font_size = 16

        self.total_coins = 100
        self.coin_gain = 0

        self.player1_coins = 0
        self.player2_coins = 0

        self.player1_card = None
        self.player2_card = None
        self.round_count = 0
        self.player1_hand = [str(i) for i in range(1, 6)]  # プレイヤーの初期手札は1から5までの全ての数字
        self.player2_hand = [str(i) for i in range(1, 6)]  # AIの初期手札は1から5までの全ての数字

        self.label = tk.Label(master, text="各プレイヤーは交互にカードをプレイします。\nカードの最も高い数字を持ったプレイヤーがラウンドに勝ちます。",
                              font=("Helvetica", font_size), bg="#333333", fg="white")
        self.label.pack(pady=20)

        # 時計を表示するためのラベルを作成
        self.clock_label = tk.Label(master, font=("Helvetica", font_size), bg="#333333", fg="white")
        self.clock_label.pack(pady=0, side="left")
        # 時計を更新するためにupdate_timeメソッドを呼び出す
        self.update_time()

        self.backGround_img = tk.Label(master, bg="#333333")
        self.backGround_img.place(x=0, y=0)

        backGround_img = Image.open("img/back.png")
        backGround_img = backGround_img.resize((1920, 1080))
        backGround_img = backGround_img.convert("RGBA")
        photo_bk_image = ImageTk.PhotoImage(backGround_img)
        self.backGround_img.configure(image=photo_bk_image)
        self.backGround_img.image = photo_bk_image

        self.coins_frame = tk.Frame(master, bg="#333333")
        self.coins_frame.pack()

        self.player1_coins_label = tk.Label(self.coins_frame, text=f"プレイヤーの金貨: {self.player1_coins}枚", font=("Helvetica", font_size), bg="#333333", fg="white", anchor="w")
        self.player1_coins_label.pack(padx=20, pady=5, side="left")

        self.total_coins_label = tk.Label(self.coins_frame, text=f"総金貨: {self.total_coins}枚", font=("Helvetica", font_size), bg="#333333", fg="white", anchor="w")
        self.total_coins_label.pack(padx=20, pady=5, side="left")

        self.player2_coins_label = tk.Label(self.coins_frame, text=f"AIの金貨: {self.player2_coins}枚", font=("Helvetica", font_size), bg="#333333", fg="white", anchor="w")
        self.player2_coins_label.pack(padx=20, pady=5, side="left")

        self.coin_gain = random.randint(1, 5)
        self.coin_gain_label = tk.Label(master, text=f"今回獲得できる金貨: {self.coin_gain}枚", font=("Helvetica", font_size), bg="#333333", fg="white")
        self.coin_gain_label.pack()

        self.player2_hand_label = tk.Label(master, text="AIの手札:", font=("Helvetica", font_size), bg="#333333", fg="white")
        self.player2_hand_label.pack()

        self.player2_hand_display = tk.Label(master, font=("Helvetica", font_size), bg="#333333", fg="white")
        self.player2_hand_display.pack()

        self.button_frame = tk.Frame(self.master, bg="#333333")
        self.button_frame.pack()

        self.result_label = tk.Label(master, text="", font=("Helvetica", 14), bg="#333333", fg="white")
        self.result_label.pack(pady=20)

        self.card_images = [Image.open(f"img/card{i}.png") for i in range(1, 6)]
        self.show_card_buttons()

        # プレイヤーとAIのコイン画像の表示
        self.player1_coins_img_label = tk.Label(master, bg="#333333")
        self.player1_coins_img_label.place(x=1260, y=950)
        self.player2_coins_img_label = tk.Label(master, bg="#333333")
        self.player2_coins_img_label.place(x=350, y=0)
        
        # プレイヤーとAIのカード表示用のラベルを作成
        self.player1_card_label = tk.Label(master, bg="#333333")
        self.player1_card_label.pack(side=tk.LEFT, padx=100, pady=20)
        self.player2_card_label = tk.Label(master, bg="#333333")
        self.player2_card_label.pack(side=tk.RIGHT, padx=100, pady=20)

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
        self.next_round_button.pack_forget()

        self.update_ai_hand()

        self.master.bind("<Escape>", self.create_modal_window)
        
        # Label上で<Motion>イベント発生時、
        # show_positionを実行するように設定
        self.mouse_pos = tk.Label(self.master, text=f"", font=("Helvetica", font_size), bg="#333333", fg="white")
        self.mouse_pos.place(x=0, y=0)
        self.master.bind("<Motion>", self.show_position)

    def show_card_buttons(self):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        card_labels = ["1", "2", "3", "4", "5"]
        for card_label in card_labels:
            if card_label in self.player1_hand:
                # 画像の読み込み
                img = Image.open(f"img/card{card_label}.png")
                # 画像のサイズを変更
                img = img.resize((140, 210))  # 例: 幅150ピクセル、高さ250ピクセルに変更
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
            self.play_round()
            if self.round_count == 5:
                self.end_game()  # ラウンドが5回に達したらゲーム終了

    def play_round(self):
        self.round_count += 1
        self.player2_card = random.choice(self.player2_hand)

        result = "引き分けです！"
        if int(self.player1_card) > int(self.player2_card):
            result = "プレイヤー1がこのラウンドを勝ちました！"
            self.player1_coins += self.coin_gain
            self.total_coins -= self.coin_gain
        elif int(self.player2_card) > int(self.player1_card):
            result = "AIがこのラウンドを勝ちました！"
            self.player2_coins += self.coin_gain
            self.total_coins -= self.coin_gain

        # カードの表示
        self.show_cards()

        self.result_label.config(text=result)
        self.update_coins_display()
        self.next_round_button.pack()

    def show_cards(self):
        # プレイヤーのカードの画像を読み込み、透明度を変更可能な形式に変換
        player1_card_img = Image.open(f"img/card{self.player1_card}.png")
        player1_card_img = player1_card_img.resize((140, 210))
        player1_card_img = player1_card_img.convert("RGBA")

        # AIのカードの画像を読み込み、透明度を変更可能な形式に変換
        player2_card_img = Image.open(f"img/card{self.player2_card}.png")
        player2_card_img = player2_card_img.resize((140, 210))
        player2_card_img = player2_card_img.convert("RGBA")

        # カードの勝敗を判定
        if int(self.player1_card) > int(self.player2_card):
            # フェードアウトのアニメーションを実行
            self.shatter_card(player1_card_img, player2_card_img, 1)
        elif int(self.player2_card) > int(self.player1_card):
            # フェードアウトのアニメーションを実行
            self.shatter_card(player1_card_img, player2_card_img, 2)

    def shatter_card(self, image1, image2, flg):
        # カードが割れるアニメーションを追加
        # 今回は割れるアニメーションは省略しています
        if flg == 1:
            player1_card_img = ImageTk.PhotoImage(image1)
            self.player1_card_label.configure(image=player1_card_img)
            self.player1_card_label.image = player1_card_img
            for alpha in range(255, -1, -5):
                image2.putalpha(alpha)  # 透明度を設定
                photo_image = ImageTk.PhotoImage(image2)
                self.player2_card_label.configure(image=photo_image)
                self.player2_card_label.image = photo_image
                self.player2_card_label.update_idletasks()  # 更新された画像を表示
                self.player2_card_label.after(50)  # 50ミリ秒待ってから次の透明度に更新
            # 透明度が0になったら画像を削除
            self.player2_card_label.configure(image="")
            self.player2_card_label.image = None

        elif flg == 2:
            player2_card_img = ImageTk.PhotoImage(image2)
            self.player2_card_label.configure(image=player2_card_img)
            self.player2_card_label.image = player2_card_img
            for alpha in range(255, -1, -5):
                image1.putalpha(alpha)  # 透明度を設定
                photo_image = ImageTk.PhotoImage(image1)
                self.player1_card_label.configure(image=photo_image)
                self.player1_card_label.image = photo_image
                self.player1_card_label.update_idletasks()  # 更新された画像を表示
                self.player1_card_label.after(50)  # 50ミリ秒待ってから次の透明度に更新
            # 透明度が0になったら画像を削除
            self.player1_card_label.configure(image="")
            self.player1_card_label.image = None

    def reset_round(self, event=None):
        self.result_label.config(text="")
        self.coin_gain_label.config(text="")
        self.player1_card = None
        if self.round_count < 5:
            self.show_card_buttons()  # カードを選択した後にボタンを再描画
            self.update_ai_hand()
            self.update_coin_gain()
            self.update_coin_img_display()
            self.next_round_button.pack_forget()
            self.player1_card_label.configure(image="")
            self.player1_card_label.image = None
            self.player2_card_label.configure(image="")
            self.player2_card_label.image = None

    def end_game(self):
        if self.player1_coins > self.player2_coins:
            winner = "プレイヤー1の勝利！"
        elif self.player1_coins < self.player2_coins:
            winner = "AIの勝利！"
        else :
            winner = "引き分け"
        messagebox.showinfo("ゲーム終了", 
                            "金貨枚数で判定します。\n\n"
                            f"{winner}\n\n"
                            f"プレイヤー1の総金貨: {self.player1_coins}/100枚\n"
                            f"AIの総金貨: {self.player2_coins}/100枚")
        self.master.destroy()

    def update_coins_display(self):
        self.player1_coins_label.config(text=f"プレイヤー1の金貨: {self.player1_coins}枚")
        self.total_coins_label.config(text=f"総金貨: {self.total_coins}枚")
        self.player2_coins_label.config(text=f"AIの金貨: {self.player2_coins}枚")

    def update_ai_hand(self):
        if self.player2_card in self.player2_hand:
            self.player2_hand.remove(self.player2_card)
        self.player2_hand_display.config(text=", ".join(self.player2_hand))

    def update_coin_img_display(self):

        # プレイヤー1のコイン
        if(self.player1_coins >=1):
            if self.player1_coins >= 1 and self.player1_coins < 5:
                player1_img = Image.open("img/coin_back.png")
                player1_img = player1_img.resize((100, 100))
                player1_img = player1_img.convert("RGBA")     
            elif self.player1_coins >= 5 and self.player1_coins < 10 :
                player1_img = Image.open("img/coin_5piece.png")
                player1_img = player1_img.resize((100, 100))
                player1_img = player1_img.convert("RGBA")
            else :
                player1_img = Image.open("img/coin_10piece.png")
                player1_img = player1_img.resize((100, 100))
                player1_img = player1_img.convert("RGBA")
            photo_image1 = ImageTk.PhotoImage(player1_img)
            self.player1_coins_img_label.configure(image=photo_image1)
            self.player1_coins_img_label.image = photo_image1
            self.player1_coins_img_label.update_idletasks()  # 更新された画像を表示

        # AIのコイン
        if(self.player2_coins >=1):
            if self.player2_coins >= 1 and self.player2_coins < 5:
                player2_img = Image.open("img/coin_back.png")
                player2_img = player2_img.resize((100, 100))
                player2_img = player2_img.convert("RGBA")     
            elif self.player2_coins >= 5 and self.player2_coins < 10 :
                player2_img = Image.open("img/coin_5piece.png")
                player2_img = player2_img.resize((100, 100))
                player2_img = player2_img.convert("RGBA")
            else :
                player2_img = Image.open("img/coin_10piece.png")
                player2_img = player2_img.resize((100, 100))
                player2_img = player2_img.convert("RGBA")
            photo_image2 = ImageTk.PhotoImage(player2_img)
            self.player2_coins_img_label.configure(image=photo_image2)
            self.player2_coins_img_label.image = photo_image2
            self.player2_coins_img_label.update_idletasks()  # 更新された画像を表示
        

    def update_coin_gain(self):
        self.coin_gain = random.randint(1, 5)
        self.coin_gain_label.config(text=f"今回獲得できる金貨: {self.coin_gain}枚")        

    def create_modal_window(self, event=None):
        modal_window = tk.Toplevel(self.master)
        modal_window.title("ゲーム終了")
        modal_window.attributes('-topmost', True)
        modal_window.geometry("200x100")
        modal_window.grab_set()

        end_game_button = tk.Button(modal_window, text="ゲームを終了", command=self.end_game)
        end_game_button.pack(pady=10)

    def show_position(self, event):
        x, y = event.x, event.y     # x,y座標取得
        self.mouse_pos.config(text= str(x) + ", " + str(y))   # 座標表示

    def update_time(self):
        current_time = strftime('%H:%M:%S %p')  # 現在時刻を取得
        self.clock_label.config(text=current_time)  # ラベルに時刻を表示
        self.clock_label.after(1000, self.update_time)  # 1秒ごとに時刻を更新


def main():
    root = tk.Tk()
    app = CardGameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
