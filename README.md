# RetroArch Savestates Manager

A lightweight, modern desktop application built with Python and PySide6 designed to inspect, manage, and clean up your RetroArch save states. Easily browse through your save state library across different cores and games, preview screenshot thumbnails, switch save slots, and safely delete unwanted states from a clean graphical interface.

<img width="2326" height="1097" alt="image" src="https://github.com/user-attachments/assets/585dde12-3b40-44cc-a409-fc39335cf137" />

---

## 🌟 Features

- **Automated Game & Core Organization:** Parses and groups your save state files by game title and associated RetroArch core (e.g., Genesis Plus GX, Mesen-S, Nestopia).
- **Save Slot Navigation:** Inspect and switch between different save state slots (`Savestate: 0`, `1`, etc.) for any selected title.
- **Screenshot Preview Support:** Displays save state screenshot thumbnails directly in the UI to easily identify specific game saves.
- **Safe State Deletion:** Fast state deletion with an optional confirmation toggle (*"Ask confirmation before delete"*) to prevent accidental data loss.
- **Modern Dark UI:** A sleek, clean, responsive dark-themed graphical interface crafted with PySide6.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- [PySide6](https://pypi.org/project/PySide6/)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/silverlays/RetroArch-Savestates-Manager.git
   cd retroarch-savestates-manager
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application:**
   ```bash
   python app.py
   ```

## 📜 Credits & Acknowledgments
### 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
