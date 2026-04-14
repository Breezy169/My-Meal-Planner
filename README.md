# MyMealPlanner 🥗💪

A lightweight, local desktop application built with Python and Tkinter to manage your daily nutrition, track fitness progress, and organize your weekly meal prep.

## ✨ Features

- **Profile Management:** Track your weight (Current vs. Starting), body fat, and fitness milestones (Deadlift, Squat, Running).
- **Progress Tracking:** Automatically calculates your "Achievement" (weight loss or gain) based on your chosen plan (Cut/Bulk).
- **Meal Database:** Create and save your favorite meals including macros (Calories, Proteins, Carbs, Fats) and even recipes.
- **Weekly Planner:** Drag-and-drop style organization for your week with total calorie and cost calculation.
- **Single Instance Protection:** Smart socket-based protection to ensure the app only opens once.
- **Local Privacy:** All data is stored locally in SQLite databases. No cloud, no tracking.

## 🚀 Getting Started

### Prerequisites

- Python 3.x installed on your system.

### Installation

1. **Clone the repository:**

2. Run the application:

    Directly start the app using Python:

    python App.py

    Note: On the first start, the app will automatically create the necessary database files in a /db folder.

### 🛠️ Built With

* **Python** - Core logic
* **Tkinter** - Graphical User Interface
* **SQLite3** - Local database management
    

### 📦 Creating an Executable (.exe)
* **If you want to create a standalone application for Windows:**
* **1. Install PyInstaller: pip install pyinstaller**
* **2. Build the app:**
        pyinstaller --noconsole --onefile App.py
* **3. Copy your db/ folder into the dist/ directory next to the App.exe.**

### 🔒 Privacy & Data
This is the Vanilla Version. The repository includes the source code and the database structure, but none of my personal data. When you run the app, a fresh profile is generated for you.

📝 License

This project is open-source and free to use.
