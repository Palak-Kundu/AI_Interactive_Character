
import tkinter as tk
import threading
import time
from playsound import playsound
import os
from dotenv import load_dotenv
import openai
from openai import OpenAI

# Load API key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def call_gpt(prompt):
    try:
        client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "Hello"},
            ],
            stream=False
        )
        print(response.choices[0].message.content)
    except Exception as e:
        return f"Error: {e}"

# Mood file handling
def load_mood():
    try:
        with open("mood.txt", "r") as f:
            return int(f.read().strip())
    except:
        return 50

def save_mood(mood):
    with open("mood.txt", "w") as f:
        f.write(str(mood))

class AIBuddyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Buddy")
        self.mood = load_mood()

        self.canvas = tk.Canvas(root, width=400, height=300, bg="white")
        self.canvas.pack()

        self.face = self.canvas.create_oval(150, 100, 250, 200, fill="lightblue")
        self.eye1 = self.canvas.create_oval(170, 130, 180, 140, fill="black")
        self.eye2 = self.canvas.create_oval(220, 130, 230, 140, fill="black")
        self.mouth = self.canvas.create_arc(175, 150, 225, 180, start=0, extent=-180, style=tk.ARC)

        self.entry = tk.Entry(root, width=40)
        self.entry.pack()
        self.entry.bind("<Return>", self.respond)

        self.response_label = tk.Label(root, text="", wraplength=380, justify="left")
        self.response_label.pack()

        self.typing_label = tk.Label(root, text="", fg="gray")
        self.typing_label.pack()

        self.mood_bar = tk.Canvas(root, width=100, height=10, bg="gray")
        self.mood_bar.pack()
        self.mood_fill = self.mood_bar.create_rectangle(0, 0, self.mood, 10, fill="green")

        threading.Thread(target=self.blinking, daemon=True).start()

    def blinking(self):
        while True:
            time.sleep(1)
            self.canvas.itemconfig(self.eye1, fill="white")
            self.canvas.itemconfig(self.eye2, fill="white")
            time.sleep(0.2)
            self.canvas.itemconfig(self.eye1, fill="black")
            self.canvas.itemconfig(self.eye2, fill="black")

    def respond(self, event=None):
        user_input = self.entry.get()
        self.entry.delete(0, tk.END)

        if "dance" in user_input.lower():
            self.jump()
            playsound("dance.wav", block=False)
            return
        if "wave" in user_input.lower():
            self.wave()
            playsound("wave.wav", block=False)
            return
        if "hello" in user_input.lower():
            playsound("hello.wav", block=False)

        self.typing_label.config(text="Typing...")
        threading.Thread(target=self.generate_response, args=(user_input,), daemon=True).start()

    def generate_response(self, user_input):
        response = call_gpt(user_input)
        self.typing_label.config(text="")
        self.response_label.config(text=response)
        self.mood = min(100, self.mood + 5)
        save_mood(self.mood)
        self.mood_bar.coords(self.mood_fill, 0, 0, self.mood, 10)

    def jump(self):
        for _ in range(5):
            self.canvas.move(self.face, 0, -5)
            self.canvas.move(self.eye1, 0, -5)
            self.canvas.move(self.eye2, 0, -5)
            self.canvas.move(self.mouth, 0, -5)
            self.root.update()
            time.sleep(0.05)
        for _ in range(5):
            self.canvas.move(self.face, 0, 5)
            self.canvas.move(self.eye1, 0, 5)
            self.canvas.move(self.eye2, 0, 5)
            self.canvas.move(self.mouth, 0, 5)
            self.root.update()
            time.sleep(0.05)

    def wave(self):
        self.canvas.itemconfig(self.mouth, start=0, extent=180)
        self.root.update()
        time.sleep(0.5)
        self.canvas.itemconfig(self.mouth, start=0, extent=-180)
        self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = AIBuddyApp(root)
    root.mainloop()
