import customtkinter as ctk
from PIL import Image
import os
import sys

if getattr(sys, 'frozen', False):
    script_dir = os.path.dirname(sys.executable)
else:
    script_dir = os.path.dirname(os.path.abspath(__file__))

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("MCU Personality Test")
root.geometry("700x650")


characters = ["Iron Man", "Captain America", "Thor",
               "Black Widow", "Hawkeye", "Spider-Man", "Doctor Strange", "Wanda"]

char_images = ["ironman.png", "captainamerica.png", "thor.png", "blackwidow.png", "hawkeye.png", "spider-man.png", "doctor strange.png", "wanda.png"]
descriptions = [
    "You are a technological genius. You solve problems with your mind and innovations.",
    "You are a moral compass. Honor and duty are more important than anything else.",
    "You are the soul of the team and a powerful force. You love your friends.",
    "You are a strategy master. You prefer to act subtly and effectively.",
    "You are an example of self-discipline. You value focus and family.",
    "You are a kind heart. You are always ready to help, even in small things.",
    "You are a seeker of knowledge. You see the world deeper than others.",
    "You are the embodiment of emotions. Your strength lies in your feelings.",
]

questions = [
    {"text": "1. What is your primary weapon of choice?", "options": [("Advanced Technology", 0), ("My Willpower", 1), ("Divine Artifact", 2), ("Magic and Spells", 6)]},
    {"text": "2. How do you handle a crisis?", "options": [("Analyze and invent", 0), ("Follow the plan", 1), ("Improvise and adapt", 5), ("Use intuition", 7)]},
    {"text": "3. What do you value most in a friend?", "options": [("Brilliance", 0), ("Loyalty", 2), ("Reliability", 4), ("Kindness", 5)]},
    {"text": "4. What is your ideal environment?", "options": [("High-tech lab", 0), ("Quiet countryside", 4), ("Ancient library", 6), ("The battlefield", 2)]},
    {"text": "5. What is your biggest weakness?", "options": [("Ego", 0), ("Self-sacrifice", 1), ("Short temper", 2), ("Over-thinking", 6)]},
    {"text": "6. How do you fight?", "options": [("Tactical strikes", 3), ("Long-range precision", 4), ("Close combat", 1), ("Psychological pressure", 7)]},
    {"text": "7. What's your attitude towards teamwork?", "options": [("I work best alone", 6), ("I'm the leader", 1), ("I'm the heart of the team", 2), ("I support from shadows", 3)]},
    {"text": "8. Pick a word that describes you:", "options": [("Unstoppable", 2), ("Disciplined", 4), ("Curious", 5), ("Resilient", 3)]},
    {"text": "9. How do you react to a loss?", "options": [("Blame myself and work harder", 0), ("Keep moving forward", 1), ("Fall into deep grief", 7), ("Seek revenge", 2)]},
    {"text": "10. What is your favorite type of mission?", "options": [("Rescue operation", 5), ("Stealth & Spy work", 3), ("Diplomacy", 1), ("Cosmic adventure", 2)]},
    {"text": "11. What defines a hero?", "options": [("Their inventions", 0), ("Their character", 1), ("Their sacrifice", 5), ("Their control", 6)]},
    {"text": "12. How do you view your enemies?", "options": [("A problem to solve", 0), ("Threat to peace", 1), ("Worthy opponents", 2), ("Tools of chaos", 6)]},
]

points = [0] * len(characters)
history = []
current_q = 0

def show_start_screen():
    question_label.pack_forget()
    back_button.pack_forget()
    for b in buttons: b.pack_forget()
    result_name.pack_forget()
    image_label.pack_forget()
    result_desc.pack_forget()
    retry_button.pack_forget()
   
    start_title.pack(pady=(150, 30))
    start_button.pack(pady=20)

def start_quiz():
    global current_q, points, history
    current_q = 0
    points = [0] * len(characters)
    history = []
   
    start_title.pack_forget()
    start_button.pack_forget()
    update_question()

def handle_answer(char_idx):
    global current_q
   
    points[char_idx] += 1
    history.append(char_idx)
    current_q += 1

    if current_q < len(questions):
        update_question()
    else:
        show_results()

def go_back():
    global current_q
    if current_q > 0:
        current_q -= 1
        last_idx = history.pop()
        points[last_idx] -= 1
        update_question()

def update_question():
    q_data = questions[current_q]
    question_label.pack(pady=(40, 20))
    question_label.configure(text=q_data["text"])
    if current_q > 0:
        back_button.pack(pady=(0, 10))
    else:
        back_button.pack_forget()

    for i in range(4):
        btn_text, char_link = q_data["options"][i]
        buttons[i].pack(pady=10)
        buttons[i].configure(
            text=btn_text,
            command=lambda idx=char_link: handle_answer(idx)
        )

def show_results():
    question_label.pack_forget()
    back_button.pack_forget()
    for b in buttons: b.pack_forget()

    best_index = points.index(max(points))
    result_name.configure(text=characters[best_index].upper())
    result_desc.configure(text=descriptions[best_index])

    img_path = os.path.join(script_dir, "characters", char_images[best_index])
    if os.path.exists(img_path):
        try:
            pil_image = Image.open(img_path)
            my_image = ctk.CTkImage(light_image=pil_image, size=(300, 400))
            image_label.configure(image=my_image, text="")
        except Exception as e:
            image_label.configure(text=f"Error: {e}")
    else:
        image_label.configure(text=f"Image not found:\n{char_images[best_index]}")

    result_name.pack(pady=20)
    image_label.pack(pady=10)
    result_desc.pack(pady=20, padx=40)
    retry_button.pack(pady=20)


start_title = ctk.CTkLabel(root, text="AVENGERS PERSONALITY QUIZ", font=("Helvetica", 34, "bold"), text_color="#8E1717")
start_button = ctk.CTkButton(root, text="START TEST", width=250, height=60, font=("Helvetica", 20, "bold"), fg_color="#8E1717", hover_color="#631010", command=start_quiz)

question_label = ctk.CTkLabel(root, text="", font=("Helvetica", 22, "bold"))
back_button = ctk.CTkButton(root, text="← Back to previous question", width=200, height=30, fg_color="transparent", text_color="gray", hover_color="#EEE", command=go_back )
buttons = []
for i in range(4):
    btn = ctk.CTkButton(root, text="", width=450, height=55, fg_color="#8E1717", hover_color="#631010", font=("Helvetica", 16))
    buttons.append(btn)

result_name = ctk.CTkLabel(root, text="", font=("Helvetica", 40, "bold"), text_color="#8E1717")
image_label = ctk.CTkLabel(root, text="")
result_desc = ctk.CTkLabel(root, text="", font=("Helvetica", 18), wraplength=500)
retry_button = ctk.CTkButton(root, text="Try Again", command=show_start_screen, fg_color="#333", height=45, width=200)

show_start_screen()
root.mainloop()