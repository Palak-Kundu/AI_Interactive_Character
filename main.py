import canvas as cv
from openai import call_gpt
import random
import time
from playsound import playsound  
import os

user_input = ""
ai_response = ""
mood = "neutral"
is_blinking = False
is_jumping = False
is_waving = False
typing = False
mood_score = 50
conversation_log = []
wearing_hat = False

def main():
    load_mood()
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
    draw_face()
    cv.draw_text("Chat Log:", 20, 310, size=14, color="black")
    y = 330
    for speaker, msg in conversation_log:
        cv.draw_text(f"{speaker}: {msg}", 20, y, size=12, color="black")
        y += 20

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

    # Body & Legs
    cv.draw_line(x + 0, y + 100, x - 40, y + 120, color="black", width=3)
    cv.draw_line(x + 100, y + 200, x + 100, y + 270, color="black", width=3)
    cv.draw_line(x + 100, y + 270, x + 80, y + 300, color="black", width=3)
    cv.draw_line(x + 100, y + 270, x + 120, y + 300, color="black", width=3)

    # Mouth based on mood
    if mood == "happy":
        cv.draw_arc(220, y+120, 60, 40, start=0, extent=-180, color="green")
    elif mood == "sad":
        cv.draw_arc(220, y+140, 60, 40, start=0, extent=180, color="blue")
    elif mood == "confused":
        cv.draw_text("?", 245, y+120, size=30, color="orange")
    else:
        cv.draw_line(230, y+140, 270, y+140, color="gray")  # Neutral mouth

    if wearing_hat:
        cv.draw_rect(180, y - 30, 140, 20, color="black")
        cv.draw_rect(170, y - 10, 160, 10, color="black")


def handle_key(key):
    global user_input
    if key == "Backspace":
        user_input = user_input[:-1]
    elif len(key) == 1:
        user_input += key
    draw_character()

def handle_enter():
    global ai_response, user_input, mood, typing, is_jumping, is_waving, mood_score
    if user_input.strip() == "":
        return
    conversation_log.append(("You", user_input))
    draw_character()
    typing = True
    draw_character()
    playsound("typing-sound-effect-337681.mp3") 
    cv.wait(0.5)
    ai_response = call_gpt(user_input)
    conversation_log.append(("Buddy", ai_response))
    typing = False
    conversation_log = conversation_log[-6:]  # Keep last 6 lines
    mood = detect_mood(ai_response)
    mood_score = update_mood_score(mood)
    if mood == "sad":
        playsound("e-oh-91678.mp3")
    # Animation Triggers
    if "dance" in user_input.lower() or "jump" in user_input.lower():
        jump()
    elif "hi" in user_input.lower() or "hello" in user_input.lower():
        wave()
    elif "wear hat" in user_input.lower():
        wearing_hat = True
    elif "remove hat" in user_input.lower():
        wearing_hat = False
        
    user_input = ""
    save_mood()
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

def update_mood_score(mood):
    if mood == "happy":
        return min(mood_score + 10, 100)
    elif mood == "sad":
        return max(mood_score - 15, 0)
    elif mood == "confused":
        return max(mood_score - 5, 0)
    else:
        return mood_score
    
def jump():
    global is_jumping
    is_jumping = True
    playsound("cartoon-jump-6462.mp3")
    draw_character()
    cv.pause(300)
    is_jumping = False
    draw_character()

def wave():
    global is_waving
    is_waving = True
    draw_character()
    cv.pause(500)
    is_waving = False
    draw_character()

def save_mood():
    with open("mood.txt", "w") as f:
        f.write(str(mood_score))

def load_mood():
    global mood_score
    if os.path.exists("mood.txt"):
        with open("mood.txt", "r") as f:
            mood_score = int(f.read())

main()