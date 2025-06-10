import canvas as cv
from openai import call_gpt
import random
import time

user_input = ""
ai_response = ""
mood = "neutral"
is_blinking = False
is_jumping = False
is_waving = False
typing = False
mood_score = 50

def main():
    cv.make_canvas(500, 500)
    cv.set_background_color("lightblue")
    draw_character()
    cv.set_interval(blink, 3000)  
    cv.on_key_typed(handle_key)
    cv.on_key_press("Enter", handle_enter)

def draw_character():
    cv.clear()
    draw_face()
    cv.draw_text("Say something to your buddy:", 20, 20, size=16, color="black")
    cv.draw_text("You: " + user_input, 20, 400, size=14, color="darkblue")
    if typing:
        cv.draw_text("Buddy is typing...", 20, 430, size=14, color="gray")
    else:
        cv.draw_text("Buddy: " + ai_response, 20, 430, size=14, color="darkgreen")
    draw_mood_meter()

def draw_face():
    x, y = 150, 100
    if is_jumping:
        y -= 30
    # Head
    cv.draw_oval(x, y, 200, 200, color="white")

    # Eyes
    if is_blinking:
        cv.draw_line(200, y+60, 220, y+60, color="black")  # Left eye blink
        cv.draw_line(280, y+60, 300, y+60, color="black")  # Right eye blink
    else:
        cv.draw_oval(200, 150, 20, 20, color="black")  # Left eye
        cv.draw_oval(280, 150, 20, 20, color="black")  # Right eye
    
    # Waving Arms
    if is_waving:
        cv.draw_line(x + 200, y + 100, x + 240, y + 50, color="black", width=3)
    else:
        cv.draw_line(x + 200, y + 100, x + 240, y + 120, color="black", width=3)

    cv.draw_line(x + 0, y + 100, x - 40, y + 120, color="black", width=3)

    # Body & Legs
    cv.draw_line(x + 100, y + 200, x + 100, y + 270, color="black", width=3)
    cv.draw_line(x + 100, y + 270, x + 80, y + 300, color="black", width=3)
    cv.draw_line(x + 100, y + 270, x + 120, y + 300, color="black", width=3)

    # Mouth based on mood
    if mood == "happy":
        cv.draw_arc(220, 220, 60, 40, start=0, extent=-180, color="green")
    elif mood == "sad":
        cv.draw_arc(220, 240, 60, 40, start=0, extent=180, color="blue")
    elif mood == "confused":
        cv.draw_text("?", 245, 230, size=30, color="orange")
    else:
        cv.draw_line(230, 240, 270, 240, color="gray")  # Neutral mouth

def handle_key(key):
    global user_input
    if key == "Backspace":
        user_input = user_input[:-1]
    elif len(key) == 1:
        user_input += key
    draw_character()

def handle_enter():
    global ai_response, user_input, mood
    if user_input.strip() == "":
        return
    ai_response = call_gpt(user_input)
    mood = detect_mood(ai_response)
    user_input = ""
    draw_character()

def detect_mood(text):
    text = text.lower()
    if "happy" in text or "glad" in text or "great" in text:
        return "happy"
    elif "sad" in text or "sorry" in text or "unhappy" in text:
        return "sad"
    elif "?" in text or "confused" in text:
        return "confused"
    else:
        return "neutral"

def blink():
    global is_blinking
    is_blinking = True
    draw_character()
    cv.pause(200)
    is_blinking = False
    draw_character()

def draw_mood_meter():
    cv.draw_text("Mood", 400, 20, size=12)
    cv.draw_rect(390, 40, 100, 10, color="gray")
    color = "green" if mood_score > 70 else "orange" if mood_score > 40 else "red"
    cv.draw_rect(390, 40, mood_score, 10, color=color)

main()