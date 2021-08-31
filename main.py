from tkinter.constants import BOTTOM, LEFT, RIGHT, TOP
import pypokedex
import PIL.Image, PIL.ImageTk
import tkinter as tk
import tkinter.ttk as ttk
import urllib3
from io import BytesIO
import random
import pygame
import pyglet
from tkinter.font import Font

class Pokemon(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)

        self.score_font = Font(
            family="Pokemon Solid",
            size=30,
            weight="normal",
            slant="roman",
            underline=0,
            overstrike=0
        )

        self.title_font = Font(
            family="Pokemon Solid",
            size=40,
            weight="bold",
            slant="roman",
            underline=0,
            overstrike=0
        )

        self.cal_font = Font(
            family="Calibri",
            size=20,
            weight="bold",
            slant="roman",
            underline=0,
            overstrike=0
        )

        self.score_text = tk.StringVar()
        self.score_text.set("0")

        self.types = tk.StringVar()

        self.button_style = ttk.Style()
        self.button_style.configure("TButton", font=("Calibri", 20, "bold"), foreground="#000", background="#000")

        self.title = tk.Label(self, text="Who's That Pokemon?")
        self.title.config(font=self.title_font, foreground="#ffd700")
        self.title.pack(padx=10)

        self.score = tk.Label(self, textvariable=self.score_text)
        self.score.config(font=self.score_font)
        self.score.pack(padx=10)

        self.pokemon_image = tk.Label(self)
        self.pokemon_image.pack(padx=10)

        self.pokemon_types = tk.Label(self, textvariable=self.types)
        self.pokemon_types.config(font=self.cal_font)

        self.text_input = tk.Text(self, height=1, bg="#ffffff")
        self.text_input.config(font=self.cal_font)

        self.btn_start = ttk.Button(self, text="Start", style="TButton", command=self.load_random_pokemons)
        self.btn_start.pack(padx=10, pady=10, side=TOP)

        self.btn_check = ttk.Button(self, text="Check", style="TButton", command=self.check_pokemon)
        self.btn_next = ttk.Button(self, text="Next", style="TButton", command=self.load_random_pokemons)
        self.btn_hint = ttk.Button(self, text="Hint", style="TButton", command=self.give_hints)
        
        self.current_pokemon = ""
        self.current_score = 0
    
    def load_random_pokemons(self):
        pygame.mixer.music.load("./sound/whos_that_pokemon.mp3")
        pygame.mixer.music.play()
        pokemon = pypokedex.get(dex=random.randint(1,898))
        # pokemon = pypokedex.get(dex=233)

        self.current_pokemon = pokemon.name

        self.btn_start.pack_forget()
        self.btn_next.pack_forget()
        self.text_input.pack(padx=10, pady=20)
        self.text_input.delete("1.0", "end-1c")
        self.btn_check.pack(padx=10, pady=10, side=LEFT)
        self.btn_hint.pack(padx=10, pady=10, side=LEFT)

        http = urllib3.PoolManager()
        response = http.request('GET', pokemon.sprites.front.get('default'))
        image = PIL.Image.open(BytesIO(response.data))

        img = PIL.ImageTk.PhotoImage(image.resize((250,250)))
        self.pokemon_image.config(image=img)
        self.pokemon_image.image = img

        self.types.set("Type(s): {" + ", ".join([t for t in pokemon.types]) + "}")

        print(pokemon.name)

    def check_pokemon(self):
        correct_answer = self.text_input.get("1.0", "end-1c")
        sec_val = self.current_pokemon.split("-")[1]

        if "-" in self.current_pokemon and (sec_val == "o" or sec_val == "oh" or sec_val == "f" or sec_val == "m" or sec_val == "z"):
            pass
        elif "-" in self.current_pokemon and self.current_pokemon.split("-")[0] == "tapu":
            self.current_pokemon = self.current_pokemon.replace("-", " ")
        elif "-" in self.current_pokemon:
            self.current_pokemon = self.current_pokemon.split("-")[0]

        if correct_answer.lower() == self.current_pokemon.lower():
            print("yay!!")
            self.current_score += 1
            if self.current_score % 100 == 0 and self.current_score > 0:
                pygame.mixer.music.load("./sound/congratulations.mp3")
                pygame.mixer.music.play()
            elif self.current_score % 10 == 0 and self.current_score > 0:
                pygame.mixer.music.load("./sound/10.mp3")
                pygame.mixer.music.play()
            else:
                pygame.mixer.music.load("./sound/correct.wav")
                pygame.mixer.music.play()
            self.score_text.set(str(self.current_score))
            self.btn_next.pack(padx=10, pady=10, side=RIGHT)
            self.btn_check.pack_forget()
            self.btn_hint.pack_forget()
        else:
            pygame.mixer.music.load("./sound/wrong.mp3")
            pygame.mixer.music.play()
            print("nay..")
            self.current_score -= 1
            self.score_text.set(str(self.current_score))

    def give_hints(self):
        pygame.mixer.music.load("./sound/hint.wav")
        pygame.mixer.music.play()
        self.pokemon_types.pack(padx=10, pady=10, side=LEFT)
        self.pokemon_types.after(1000, self.pokemon_types.pack_forget)

def main():
    pyglet.font.add_file("./fonts/Pokemon Solid.ttf")
    pyglet.font.add_file("./fonts/Pokemon Hollow.ttf")
    pygame.mixer.init()
    
    window = tk.Tk()
    window.geometry("1000x800")
    window.title("Pokemon Guessing Game")
    window.config(padx=10, pady=10)

    window_frame = Pokemon(window)
    window_frame.pack(expand='false',fill='both')

    window.mainloop()

if __name__ == "__main__":
    main()