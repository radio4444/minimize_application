# Idle Application Minimizer

A robust Python utility designed to improve desktop privacy and workspace organization by automatically minimizing specific application windows after a period of system inactivity.

## 🚀 Overview
The **Idle Application Minimizer** monitors system-wide inactivity (mouse and keyboard input) and automatically hides targeted applications once a predefined idle threshold is reached. 

This project was built and optimized with the assistance of **Google AI Studio** to solve the specific challenge of targeting "Electron" apps like **Notion** and **Visual Studio Code**, which often use dynamic window titles and multiple background "ghost" processes.

## ✨ Features
- **Dual-Layer Detection Strategy**:
    - **Process-Level Targeting**: Identifies applications by their executable name (e.g., `Notion.exe`), ensuring the script works even when window titles change.
    - **Title-Level Targeting**: A lightweight alternative for apps with consistent titles (e.g., "Chrome").
- **Smart Filtering**: Built-in logic to distinguish between the main user interface and "ghost" utility windows (like *Default IME* or background renderers).
- **Windows API Integration**: Leverages `ctypes` for high-performance idle detection with minimal CPU usage.
- **State Awareness**: The script intelligently minimizes windows once per idle session and resets only after user activity is detected.

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/radio4444/minimize_application.git
   cd idle-app-minimizer
   ```

2. **Install dependencies**:
This project uses pygetwindow, pywinauto, and psutil. You can install them all at once using the provided requirements file:

## 🚀 Usage
The project is split into two specialized scripts depending on your needs:
### Option A: Advanced Minimization (Recommended for Notion, VS Code, Discord)
This script targets the application's process directly.
```bash
python minimize_by_process.py
```
### Option B: Basic Minimization (Recommended for Browsers/Simple Apps)
This script targets specific text found in the window title bar.
```bash
python minimize_by_title.py
```

## ⚙️ Configuration
You can customize the idle time and the target apps by editing the CONFIG section at the top of either script:
```bash
# --- CONFIG ---
TARGET_PROCESSES = ["Notion.exe", "Code.exe", "Discord.exe"]
IDLE_THRESHOLD_MINUTES = 5
CHECK_INTERVAL = 10 
# --------------
```

## 🧠 Development & Attribution
This project was developed using logic and optimization provided by Google AI Studio. The AI assisted in creating the multi-stage filtering logic required to handle the complex window hierarchies of modern productivity software, ensuring that background system tasks are not accidentally affected.