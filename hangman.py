import tkinter as tk
from tkinter import *
from tkinter import ttk
import random

class Hangman:
    def __init__(self, window):
        self.window = window
        self.window.title('Виселица')
        self.window.geometry("600x500")
        self.lives = 6
        self.guessed_letters = []
        self.word = ""
        self.display_word = ""

        self.create_widgets()

    def create_widgets(self):
        self.btn = ttk.Button(text = "Начать игру и прочитать правила", command = self.start_program)
        self.btn.pack(pady = 20)

        self.rules_label = tk.Label(self.window, text = "", wraplength = 500, justify = "left", fg = "red")
        self.rules_label.pack(pady = 20)

        self.word_label = tk.Label(self.window, text = "", font = ("Courier", 24, "bold"))
        self.word_label.pack(pady = 20)

        self.lives_label = tk.Label(self.window, text="", font=("Arial", 12), fg="red")
        self.lives_label.pack(pady=5)
        
        self.guessed_label = tk.Label(self.window, text="Использованные буквы: ", font=("Arial", 10))
        self.guessed_label.pack(pady=5)

        self.entry_frame = tk.Frame(self.window)
        self.entry_label = tk.Label(self.entry_frame, text="Введите букву: ", font=("Arial", 12))
        self.entry_label.pack(side="left", padx=5)
        
        self.entry = ttk.Entry(self.entry_frame, width=5, font=("Arial", 12))
        self.entry.pack(side="left", padx=5)
        self.entry.bind("<KeyRelease>", self.on_key_release)

        self.result_label = tk.Label(self.window, text = "", font=("Arial", 12), fg="red")
        self.result_label.pack(pady=5)

    def start_program(self):
        rules_text = "Я загадал слово. Если отгадаешь - плюсик в карму, а нет - снесу твою систему! Играем на русском языке."
        self.rules_label.config(text=rules_text)
        try:
            with open('english.txt', 'r') as file:
                words = file.readlines()
                self.word = random.choice(words).strip().lower()
                self.display_word = ['_' for _ in self.word]
                self.update_word_display()
                self.lives = 6
                self.guessed_letters = []
                self.update_lives_display()
                self.update_guessed_display()
                
                # Показываем поле ввода
                self.entry_frame.pack(pady=20)
                self.entry.focus()
                
                self.result_label.config(text="Игра началась! Вводите буквы.", fg="green")
        except FileNotFoundError:
            self.result_label.config(text="Файл со словами не найден!", fg="red")
        except Exception as e:
            self.result_label.config(text=f"Ошибка: {e}", fg="red")

    def on_key_release(self, event):
        char = event.char.lower()
        if char and char.isalpha() and len(char) == 1:
            self.entry.delete(0, tk.END)  # Очищаем поле
            
            if char in self.guessed_letters:
                self.result_label.config(text=f"Буква '{char}' уже была использована!", fg="orange")
                return
            
            self.guessed_letters.append(char)
            self.update_guessed_display()
            
            if char in self.word:
                # Правильная буква
                self.result_label.config(text=f"Бинго! Буква '{char}' есть в слове!", fg="green")
                for i, letter in enumerate(self.word):
                    if letter == char:
                        self.display_word[i] = char
                self.update_word_display()
                
                # Проверка победы
                if '_' not in self.display_word:
                    self.result_label.config(text="Ура, Винда жива!! Ты выиграл!", fg="green", font=("Arial", 14, "bold"))
                    self.entry_frame.pack_forget()
            else:
                # Неправильная буква
                self.lives -= 1
                self.update_lives_display()
                self.result_label.config(text=f"Минус одна жизнь! Буквы '{char}' нет в слове.", fg="red")
                
                # Проверка поражения
                if self.lives == 0:
                    self.result_label.config(text=f"Неудача! Сношу твою систему! Загаданное слово: {self.word}", 
                                           fg="red", font=("Arial", 14, "bold"))
                    self.entry_frame.pack_forget()
    
    def update_word_display(self):
        self.word_label.config(text=' '.join(self.display_word))
    
    def update_lives_display(self):
        self.lives_label.config(text=f"Жизней осталось: {self.lives}")
    
    def update_guessed_display(self):
        self.guessed_label.config(text=f"Использованные буквы: {', '.join(sorted(self.guessed_letters))}")

# Запуск игры
window = tk.Tk()
game = Hangman(window)
window.mainloop()
