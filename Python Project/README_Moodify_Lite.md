# 🎵 Moodify Lite – Emotion-Based Music Recommendation System

## 📖 Overview
**Moodify Lite** is a desktop-based emotion detection and music recommendation system that combines artificial intelligence, computer vision, and an elegant user interface. 
By using **OpenCV** and **DeepFace**, the app detects a user's emotions in real time through their webcam and recommends music that matches their mood using curated Spotify playlists.

---

## 🧠 Key Features
- 🎭 Real-time emotion detection using a webcam.
- 💡 Smart classification into emotions such as *Happy, Sad, Angry, Neutral, Fear, Surprise,* and *Disgust*.
- 🎶 Spotify integration for mood-based music recommendations.
- 🎨 Simple, clean, and modern GUI using Tkinter.
- ⚙️ Lightweight, fully offline operation (except for opening Spotify links).
- 🧍 Personalized responses and dynamic emotion-based text prompts.

---

## 🧩 Technologies Used
| Category | Technology |
|-----------|-------------|
| Programming Language | Python 3.10+ |
| GUI Framework | Tkinter |
| AI Library | DeepFace |
| Computer Vision | OpenCV |
| Web Integration | Webbrowser module |
| Miscellaneous | Random, Time |

---

## 🧰 Installation & Setup
### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/Moodify-Lite.git
cd Moodify-Lite
```

### Step 2: Install Dependencies
```bash
pip install opencv-python deepface tk
```

### Step 3: Run the Application
```bash
python moodify_lite.py
```

---

## 🧠 How It Works
1. The webcam captures your live video feed.
2. DeepFace analyzes your facial expressions using pre-trained CNN models.
3. The detected emotion is displayed on the GUI.
4. The system shows a personalized message and recommends a Spotify playlist that matches your mood.

---

## 💻 Emotion Categories & Responses
| Emotion | Description | Music Type |
|----------|--------------|-------------|
| 😊 Happy | Bright smile, joyful face | Upbeat & cheerful tracks |
| 😔 Sad | Downturned lips, soft eyes | Calm & comforting songs |
| 😡 Angry | Tense face, furrowed brows | Relaxing & cooling tracks |
| 😲 Surprise | Raised eyebrows, open mouth | Energetic & fun music |
| 😨 Fear | Wide eyes, tense mouth | Calming tunes |
| 😐 Neutral | Relaxed face | Chill background playlists |

---

## 🧪 Testing
The system was tested under different lighting and facial conditions to ensure reliable performance.

| Test Case | Action | Expected Output |
|------------|---------|----------------|
| 1 | User smiles | Happy emotion + cheerful playlist |
| 2 | User frowns | Sad emotion + soothing playlist |
| 3 | No face visible | Prompt to adjust position |
| 4 | Poor lighting | Detection fallback or prompt |

---

## 🚀 Future Enhancements
- 🎧 Direct Spotify API integration for in-app playback.
- 🗣️ Voice-based emotion feedback.
- ☁️ Cloud-based emotion analytics.
- 📱 Mobile app version using Flutter or Kivy.

---

## 💬 Author
**Developed by:** Sahil Hans  
🎓 MCA – Artificial Intelligence & Machine Learning  
📍 Chandigarh University  

---

## 🪪 License
This project is licensed under the **MIT License**.  
Feel free to use, modify, and distribute with attribution.
