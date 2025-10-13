# 🕹️ Real-Time Ping Pong Game  
![Banner](https://img.shields.io/badge/Game%20Project-Python%20%7C%20Pygame-blue?style=for-the-badge&logo=python&logoColor=white)

[![Python](https://img.shields.io/badge/Python-3.10%2B-yellow?style=flat-square&logo=python)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-Game%20Engine-green?style=flat-square&logo=pygame)]
[![Object-Oriented](https://img.shields.io/badge/Design-OOP%20Principles-orange?style=flat-square)]
[![License](https://img.shields.io/badge/License-Academic-blue?style=flat-square)]
[![Status](https://img.shields.io/badge/Status-Completed-success?style=flat-square)]

---

## 🧩 Project Overview

A **real-time Ping Pong game** built using **Python** and **Pygame**, designed as part of the **VibeCoding Lab 4** project.  
This project focuses on **object-oriented design**, **game physics**, and **interactive user experience** — combining creativity and technical accuracy.

---

## ⚙️ Tech Stack

| Component | Technology |
|------------|-------------|
| Programming Language | Python 3.10+ |
| Game Framework | Pygame |
| Design Pattern | Object-Oriented Programming (OOP) |
| Rendering | Real-time 2D Rendering |
| Sound System | Pygame Mixer |
| AI Mechanism | Auto Paddle Tracking |

---

## ✨ Features

🎮 **Player vs AI Gameplay** – Enjoy competitive gameplay with an adaptive AI opponent.  
⚡ **Smooth Real-Time Physics** – Natural ball motion and realistic paddle collision.  
🔊 **Sound Effects** – Paddle hits, wall bounces, and scoring sounds.  
🔥 **Gradual Difficulty Increase** – Ball speed increases over time for more challenge.  
🏆 **Score & Game Over System** – Displays winner and allows replay (Best of 3, 5, 7).  
🧠 **Modular Codebase** – Clean, extensible OOP architecture for future features.  

---

## 🕹️ Controls

| Action | Key |
|--------|-----|
| Move Up | `W` or `↑` |
| Move Down | `S` or `↓` |
| Quit Game | `ESC` |
| Select Replay Option | `3`, `5`, or `7` |

---

## 📊 Game Flow

1️⃣ **Start the Game** – Run `main.py` and begin the match.  
2️⃣ **Control Paddle** – Player uses `W/S` or arrow keys.  
3️⃣ **AI Paddle** – Automatically tracks the ball position.  
4️⃣ **Score System** – When a player misses, the opponent scores.  
5️⃣ **Game Over** – Winner displayed when target score is reached.  
6️⃣ **Replay Menu** – Option to play Best of 3, 5, or 7.  

---

## 🧾 Folder Structure

```bash
ping-pong/
│
├── main.py                   # Main game entry point
├── requirements.txt           # Dependencies
├── game/
│   ├── game_engine.py         # Core logic and game loop
│   ├── ball.py                # Ball physics and collisions
│   ├── paddle.py              # Player and AI paddle logic
│
└── assets/
    └── sounds/                # Sound effects
        ├── paddle_hit.wav
        ├── wall_bounce.wav
        └── score.wav
```
## 🛠️ Setup Instructions
1️⃣ Clone Repository
```bash
git clone https://github.com/yourusername/ping-pong.git
cd ping-pong
```
2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
3️⃣ Run the Game
```bash
python main.py
```
4️⃣ Ensure Sound Files Exist
Place valid .wav files inside assets/sounds/:
```bash
paddle_hit.wav, wall_bounce.wav, score.wav
```

---


## 🧪 Task Completion Checklist
✅  Accurate ball-paddle collision

✅  Game over and winner display

✅  Replay (Best of 3/5/7)

✅  Sound feedback implemented

✅  Gradual speed increase

✅  Code modular and error-free


---

## 🎵 Sound System

🎵 Paddle hit → ```bash paddle_hit.wav```

🎵 Wall bounce → ```bash wall_bounce.wav```

🎵 Scoring → ```bash score.wav```






