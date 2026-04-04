import tkinter as tk
import random
import string
import pygame
import time


#XXXXX-XXXX-XXXX

HEIGHT = 150
WIDTH = 400

pygame.mixer.init()

pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

weights = {char: i for i, char in enumerate(string.ascii_uppercase, 1)}

def create_frames(root):
    frame_main = tk.Frame(root)
    frame_main.pack(fill=tk.BOTH, expand=False)

    frame_top = tk.Frame(frame_main, width=WIDTH, height=3*HEIGHT/5, bg="lightblue")
    frame_top.pack(fill=tk.X, side=tk.TOP)
    frame_top.pack_propagate(False) #no shrinking to contents tipa

    frame_bottom = tk.Frame(frame_main, width=WIDTH, height=2*HEIGHT/5, bg="lightgreen")
    frame_bottom.pack(fill=tk.X, side=tk.BOTTOM)
    frame_bottom.pack_propagate(False)

    return frame_main, frame_top, frame_bottom

def generate_code():
    code_blocks = []
    for i in range(3):
        k_num = i == 0 and 5 or 4

        while True:
            block = ''.join(random.choices(string.ascii_uppercase, k=k_num))
            
            total = sum(weights[char] for char in block)
            average = total / k_num
            
            if 10 <= average <= 15:
                code_blocks.append(block)
                break
    
    return "-".join(code_blocks)


def start_generation(top_label, button, root):
    button.config(text="Generating...", command=None)

    for _ in range(15):
        temp_code = "-".join([
            ''.join(random.choices(string.ascii_uppercase, k=4)),
            ''.join(random.choices(string.ascii_uppercase, k=4)),
            ''.join(random.choices(string.ascii_uppercase, k=4))
        ])
        top_label.config(text=temp_code)
        top_label.update()
        time.sleep(0.1)

    top_label.config(text=generate_code())
    button.config(text="Exit generator", command=root.destroy)

def init_gui():
    root = tk.Tk()
    root.title("Free robux generator (no scam fr fr)")
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.img = tk.PhotoImage(file='./robux.png') 
    
    frames = create_frames(root)
    frame_main, frame_top, frame_bottom = frames
    
    top_label = tk.Label(frame_top, text="XXXXX-XXXX-XXXX")
    top_label.pack(pady=5)

    button = tk.Button(frame_bottom, 
                       text="Generate robux", 
                       command=lambda: start_generation(top_label, 
                                                        button,
                                                        root))
    button.pack(pady=10)

    image_label = tk.Label(frame_top, image=root.img, width=50, height=54, bg="lightblue")
    image_label.pack()
    
    root.mainloop()

if __name__ == "__main__":
    init_gui()

    #ВВести константы вместо непонятных чисел