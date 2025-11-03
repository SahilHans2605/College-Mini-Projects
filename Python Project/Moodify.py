import cv2
from deepface import DeepFace
import tkinter as tk
from tkinter import messagebox
import webbrowser
import time
import random

# ====================================
# Function to detect emotion using webcam
# ====================================
def detect_emotion():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        messagebox.showerror("Error", "Could not access webcam.")
        return "neutral"

    detected_emotion = "neutral"
    print("Detecting emotion... (Press 'q' to stop)")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            emotion = result[0]['dominant_emotion']
            detected_emotion = emotion
            cv2.putText(frame, f"Emotion: {emotion}", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        except:
            cv2.putText(frame, "No face detected", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Moodify Lite - Emotion Detection (Press 'q' to stop)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return detected_emotion


# ====================================
# Splash Screen
# ====================================
def splash_screen():
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.geometry("400x250+550+250")
    splash.configure(bg="#F8EDEB")

    label = tk.Label(splash, text="✨ Made by Sahil Hans ✨",
                     font=("Comic Sans MS", 22, "bold"),
                     fg="#2C3E50", bg="#F8EDEB")
    label.pack(expand=True)

    splash.after(3000, splash.destroy)  # Display for 3 seconds
    splash.mainloop()


# ====================================
# Main App GUI Setup
# ====================================
def main_app():
    root = tk.Tk()
    root.title("Moodify Lite - Emotion Based Music Player")
    root.geometry("550x500")
    root.configure(bg="#EAF6F6")

    # 🎵 Title
    title = tk.Label(root, text="🎵 Moodify Lite 🎵",
                     font=("Comic Sans MS", 26, "bold"),
                     fg="#34495E", bg="#EAF6F6")
    title.pack(pady=25)

    # ✨ Dynamic Tagline
    quotes = [
        "✨ Let your face tell the rhythm of your soul ✨",
        "🎧 Feel the beat that matches your heart 🎶",
        "😊 Every emotion deserves its own melody 🎵",
        "💫 Turn your mood into music magic 🌈"
    ]
    tagline = tk.Label(root, text=random.choice(quotes),
                       font=("Comic Sans MS", 14, "italic"),
                       fg="#555", bg="#EAF6F6")
    tagline.pack(pady=5)

    # 🧠 Instructions
    instruction_frame = tk.Frame(root, bg="#dfe7ec", bd=2, relief="groove")
    instruction_frame.pack(pady=10, padx=20, fill="x")

    instruction_text = (
        "📸 How to Use:\n"
        "1️⃣ Sit in good lighting and face the camera clearly.\n"
        "2️⃣ Keep a natural expression — smile or frown normally.\n"
        "3️⃣ Press 'q' to stop detection once emotion is displayed.\n"
        "4️⃣ Enjoy your personalized Spotify vibe 🎧"
    )
    tk.Label(instruction_frame, text=instruction_text, font=("Arial", 10),
             bg="#dfe7ec", justify="left", wraplength=400).pack(padx=10, pady=8)

    # 🎶 Now Playing Section
    now_playing_label = tk.Label(root,
                                 text="🎵 Now Playing: It's too quiet out here 🎧",
                                 font=("Helvetica", 12, "italic"),
                                 fg="#333", bg="#EAF6F6")
    now_playing_label.pack(pady=15)

    # --- Spotify Suggestion Section ---
    spotify_frame = tk.Frame(root, bg="#EAF6F6")
    spotify_label = tk.Label(spotify_frame, text="",
                             font=("Comic Sans MS", 14, "bold"),
                             fg="#333", bg="#EAF6F6", wraplength=400, justify="center")
    spotify_label.pack(pady=10)

    spotify_button = tk.Button(spotify_frame, text="Open Spotify 🎶",
                               font=("Helvetica", 12, "bold"),
                               bg="#1DB954", fg="white",
                               activebackground="#1ed760",
                               relief="flat", padx=15, pady=8)
    spotify_button.pack(pady=5)

    # 💚 Hover animation for button
    def on_enter(e): e.widget.config(bg="#58D68D")
    def on_leave(e): e.widget.config(bg="#45B39D")

    # 🧠 Start detection logic
    def start_detection():
        emotion = detect_emotion()

        # Hide panel first
        spotify_frame.pack_forget()

        # Spotify message + playlist mapping
        messages = {
            "happy": ("😄 Feeling joyful? Let’s amplify the vibe — hit play!", "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC"),
            "sad": ("😔 Feeling low? Let’s lift the mood with some music therapy 💙", "https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1"),
            "angry": ("😤 Cool off with calm beats — wanna play something chill?", "https://open.spotify.com/playlist/37i9dQZF1DX7EfmlBlBKdm"),
            "surprise": ("😲 That’s a surprise! Let’s match your spark with upbeat tunes!", "https://open.spotify.com/playlist/37i9dQZF1DWTx0xog3gN3q"),
            "fear": ("😨 Time for comfort tunes — ready to feel safe in sound?", "https://open.spotify.com/playlist/37i9dQZF1DWZqd5JICZI0u"),
            "neutral": ("😎 Just vibing? Here’s something mellow to keep it flowing.", "https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0")
        }

        message, link = messages.get(emotion, messages["neutral"])

        now_playing_label.config(text=f"🎧 Now Playing: {emotion.capitalize()} Vibes")

        # Update Spotify section
        spotify_label.config(text=message)
        spotify_button.config(command=lambda: webbrowser.open(link))
        spotify_frame.pack(pady=10)

    # 🎛️ Start button
    btn = tk.Button(root, text="Start Emotion Detection", command=start_detection,
                    font=("Helvetica", 14, "bold"),
                    bg="#45B39D", fg="white",
                    activebackground="#58D68D",
                    relief="flat", padx=25, pady=12)
    btn.pack(pady=25)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

    # Footer
    footer = tk.Label(root, text="Made with ❤️ by Sahil Hans",
                      font=("Helvetica", 10, "italic"),
                      fg="#888", bg="#EAF6F6")
    footer.pack(side="bottom", pady=10)

    root.mainloop()


# ====================================
# Run splash first, then main app
# ====================================
if __name__ == "__main__":
    splash_screen()
    main_app()
