import canvas as cv
from openai import call_gpt
import random

user_input = ""
ai_response = ""
mood = "neutral"
is_blinking = False

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
    cv.draw_text("Buddy: " + ai_response, 20, 430, size=14, color="darkgreen")

def draw_face():
    # Head
    cv.draw_oval(150, 100, 200, 200, color="white")

    # Eyes
    if is_blinking:
        cv.draw_line(200, 160, 220, 160, color="black")  # Left eye blink
        cv.draw_line(280, 160, 300, 160, color="black")  # Right eye blink
    else:
        cv.draw_oval(200, 150, 20, 20, color="black")  # Left eye
        cv.draw_oval(280, 150, 20, 20, color="black")  # Right eye

    # Mouth based on mood
    if mood == "happy":
        cv.draw_arc(220, 220, 60, 40, start=0, extent=-180, color="green")
    elif mood == "sad":
        cv.draw_arc(220, 240, 60, 40, start=0, extent=180, color="blue")
    elif mood == "confused":
        cv.draw_text("?", 245, 230, size=30, color="orange")
    else:
        cv.draw_line(230, 240, 270, 240, color="gray")  # Neutral mouth