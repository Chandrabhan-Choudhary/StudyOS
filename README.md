# 💻 StudyOS: The Placement Operating System

> **Turn placement preparation into a data-driven streak.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Excel](https://img.shields.io/badge/Data-Local%20Excel-217346?style=flat&logo=microsoft-excel&logoColor=white)
![Architecture](https://img.shields.io/badge/Architecture-Modular%20MVC-purple?style=flat)

![App Interface](assets/screenshot.png)

## 📖 Overview

**StudyOS** is a modular productivity dashboard designed specifically for engineering students targeting high-stakes placement exams. Unlike standard to-do apps, StudyOS visualizes effort using a **"GitHub-style" Contribution Graph**, gamifying the grind of Data Structures, System Design, and Aptitude prep.

Built with **Streamlit** and **Python**, it operates on a **Zero-Database Architecture**, using local Excel files for portability while delivering a high-performance, neon-themed UI.

---

## 💡 The Story: Why I Rebuilt My Own Tool

It started as a simple need: I needed to track my placement preparation for **Data Structures** and **React**. I didn't want a bloated Notion template; I wanted a raw, high-speed dashboard that looked like code.

I wrote a quick Python script. It worked for three days. **Then it broke.**

### The "Works on My Machine" Trap
As I used the tool daily, real-world friction appeared that I hadn't anticipated during the initial build:

1.  **The OneDrive Deadlock:** Every time I saved my progress, OneDrive would try to sync the Excel file to the cloud. If I clicked "Save" again too quickly, the entire app would crash with a `PermissionError`. I was losing data because my code couldn't handle file locking.
2.  **The Sprawl:** By day 15, the data table was so wide I had to scroll horizontally for 10 seconds just to find "Today." The UX was fighting me.
3.  **The Monolith:** My code was one giant 300-line file. Adding a simple feature like a "Streak Counter" required scrolling through hundreds of lines of spaghetti code.

### The Refactor (v13.0)
I realized I wasn't building a script anymore; I was maintaining a product. I tore the code down and rebuilt it with a **Modular Architecture**:

* **Resilience:** I engineered a custom **Retry-Backoff Loop** that detects when Excel is locked, waits for the "Ghost Process" to clear, and retries the save automatically. The crashes stopped instantly.
* **Intelligence:** I built a **"Smart Focus" algorithm** that calculates the current date and dynamically renders only the relevant 3-day window. No more scrolling.
* **Structure:** I separated the app into a strict **MVC pattern** (Data Engine, Renderer, Config), making the codebase clean enough to be open-sourced.

**StudyOS is the result of that evolution: A tool that started as a script and graduated into an Operating System.**
---

## ⚙️ Architecture

The system follows a strict **Model-View-Controller (MVC)** pattern adaptation:

1.  **Frontend (View):** Streamlit with custom CSS injection for the "Neon/Dark" aesthetic.
2.  **Logic (Controller):** `modules/data_engine.py` handles input sanitization, date logic, and auto-retry saving.
3.  **Storage (Model):** Local `.xlsx` files via **OpenPyXL**. No complex SQL setup required; data is portable and user-owned.
4.  **Rendering:** A custom **HTML/CSS Engine** (`modules/renderer.py`) draws the heatmaps, bypassing the limitations of standard charting libraries.

### **Key Technical Masteries**

| Mastery | Implementation Detail | Outcome |
| :--- | :--- | :--- |
| **Concurrency Handling** | Implemented a `try/except` loop with `time.sleep()` backoff for file I/O. | **100% reduction** in "Permission Denied" crashes caused by OneDrive sync locks. |
| **Custom Visualization** | Built a raw HTML/CSS rendering engine instead of using pre-built Plotly charts. | Achieved pixel-perfect **GitHub-style Heatmaps** with precise rounded corners and gradient control. |
| **UX Optimization** | Created a "Smart Focus" toggle and split-screen layout (80/20). | Reduced cognitive load by auto-hiding past data while keeping historical context one click away. |

---

## 🚀 Features

* **Yearly Consistency Heatmap:** Visualizes your study volume over the entire year (similar to GitHub).
* **Smart Focus Mode:** The data table automatically focuses on the current 3-day window, preventing "scroll fatigue."
* **Modular Tech Stack:** Clean separation of concerns (`app.py` → `modules/`).
* **One-Click Launcher:** Includes a custom `StartStudyOS.bat` for instant deployment without touching the terminal.
* **Dark/Neon UI:** Custom CSS theming for a modern, developer-centric look.

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Excel](https://img.shields.io/badge/Excel-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)

---

## 📦 Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/Chandrabhan-Choudhary/StudyOS.git](https://github.com/Chandrabhan-Choudhary/StudyOS.git)
    cd StudyOS
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application**
    * **Method A (Windows):** Double-click `StartStudyOS.bat` (Recommended).
    * **Method B (Terminal):**
        ```bash
        python -m streamlit run app.py
        ```

4.  **Access the Dashboard**
    Open your browser to `http://localhost:8501`

---

## 📂 File Structure

```text
StudyOS/
├── app.py                  # Main Application Entry Point
├── StartStudyOS.bat        # One-Click Launcher
├── modules/                # Core Logic
│   ├── data_engine.py      # Excel I/O & Math Logic
│   ├── renderer.py         # HTML Heatmap Generator
│   └── config.py           # CSS Styling & Constants
├── requirements.txt        # Dependency List
└── studyProgress2025.xlsx  # (Auto-Generated - Not in Git)

🔮 Future Roadmap
To transition StudyOS from a personal tool to a general-purpose student planner:

📊 Predictive Analytics: Use linear regression to predict "Day of Completion" for specific subjects based on current velocity.

☁️ Cloud Sync (Optional): Add a toggle to sync specifically to Google Sheets for cross-device access without file conflicts.

🏆 Gamification: Add "Badges" (e.g., "7-Day Streak", "Weekend Warrior") to the sidebar to boost motivation.

Built by Chandrabhan Choudhary