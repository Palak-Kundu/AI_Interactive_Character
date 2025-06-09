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
    cv.draw_face()
    cv.draw_text("Say something to your buddy:", 20, 20, size=16, color="black")
    cv.draw_text("You: " + user_input, 20, 400, size=14, color="darkblue")
    cv.draw_text("Buddy: " + ai_response, 20, 430, size=14, color="darkgreen")