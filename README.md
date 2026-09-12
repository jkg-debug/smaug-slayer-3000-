<img width="1280" height="640" alt="git (1)" src="https://github.com/user-attachments/assets/8920b256-2ba8-4988-b824-5351134eb4bd" />



# Pothole Keyboard Simulator 🎯


## Basic Details
### Team Name: [chaosBoard]


### Team Members
- Team Lead: Jagath Krishna - College of engineering adoor
- Member 2: Joel shaji mathew - College of engineering adoor


### Project Description
Pothole Keyboard Simulator brings vehicular hazards to your daily typing workflow.

    Hidden Road Hazards: Quietly arms a random key to act as a pothole.

    Window Shake Physics: Uses the Win32 API to violently rattle the active window on impact.

    Flat-Tire Scrambling: Suppresses regular typing and injects erratic bursts of junk characters.

    Side-of-the-Road Repairs: Requires a dedicated, animated Tkinter progress hold on Backspace to patch the tire and return to smooth drivi

### The Problem (that doesn't exist)
Autopilot typing, mindless drafting, and lack of presence at the keyboard.

### The Solution (that nobody asked for)
Physical shock: The window shake and garbage burst jolt your brain out of its muscle-memory trance.

Real consequences: Hitting the hazard sidelines your input, forcing a mandatory, deliberate 1-second pause to "change the tire."

Constant vigilance: Because the pothole moves after every repair, you can never relax into mindless rushing.

## Technical Details
### Technologies/Components Used
For Software:
- Python
- Tkinter (GUI framework included with Python standard library)
- keyboard, pywin32 (win32gui, win32con), Python Standard Library (random, string, threading, time)
- Windows OS (Win32 API environment), Python interpreter, Git / GitHub (for version control and hosting)


### Implementation
For Software:
# Installation
pip install -r requirements.txt


# Run
python pothole_keyboard.py

### Project Documentation
For Software:

# Screenshots (Add at least 3)
![Screenshot1](Add screenshot 1 here with proper name)
*Add caption explaining what this shows*

![Screenshot2](Add screenshot 2 here with proper name)
*Add caption explaining what this shows*

![Screenshot3](Add screenshot 3 here with proper name)
*Add caption explaining what this shows*

# Diagrams
[ Physical Keystroke ]
                                 │
                                 ▼
                     keyboard.hook (Global Hook)
                                 │
         ┌───────────────────────┴───────────────────────┐
         ▼                                               ▼
  [ Key == Backspace ]                          [ Any Other Key ]
         │                                               │
         ├─ Held >= 8s? ──► [ Exit Script ]              ▼
         │                                         Is Tire Flat?
         ├─ Held >= 1s & Flat?                           │
         │       │                               ┌───────┴───────┐
         │      YES ──► [ Repair Complete ]     YES              NO
         │              [ Plant New Key   ]      │               │
         │                                       ▼               ▼
         └─ Flat & Holding?              [ Inject Random  Is Key == Pothole?
                 │                         Gibberish ]           │
                 ▼                                        ┌──────┴──────┐
         [ Spawn Tkinter ]                               YES            NO
         [ Repair HUD    ]                                │             │
                                                  [ Bam! Flat Tire ]    │
                                                  ├─ Win32 Shake Window │
                                                  └─ Cursor Chaos Burst │
                                                                        ▼
                                                                [ Pass Keystroke
                                                                  to Active App ]
For Hardware:

# Schematic & Circuit
[ Built-in Laptop Keyboard ]
             │
             ▼  (Physical Scan Codes)
[ Windows OS Input Subsystem ]
             │
             ▼  (WH_KEYBOARD_LL Low-Level Hook)
[ Python Script (pothole.py) ]
      │               │
      ▼               ▼
[ Win32 API ]   [ Tkinter GUI Engine ]
(Window Shake)  (Topmost Overlay HUD)

+-------------------------------------------------------------------------------+
|                             WINDOWS OS USERLAND                               |
|                                                                               |
|  [ Laptop Keyboard ] ---> [ Windows Raw Input / Event Queue ]                 |
|                                         |                                     |
|                                  WH_KEYBOARD_LL                               |
|                                         v                                     |
|  +-------------------------------------------------------------------------+  |
|  |                        pothole.py Execution Flow                        |  |
|  |                                                                         |  |
|  |   [ global_key_filter() ] <-----------------------+                     |  |
|  |          |                                        |                     |  |
|  |          |-- (Backspace Held >= 1s) --> [ _state_lock: Reset Tire ]     |  |
|  |          |                                        |                     |  |
|  |          |                                        v                     |  |
|  |          |                             [ plant_new_pothole() ]          |  |
|  |          |                                                              |  |
|  |          |-- (Key == Pothole Key) ----> [ trigger_pothole_hit() ]       |  |
|  |          |                                        |                     |  |
|  |          |                      +-----------------+-----------------+   |  |
|  |          |                      v                                   v   |  |
|  |          |            Thread: shake_window()             Thread: chaos_burst() |  |
|  |          |                      |                                   |   |  |
|  |          |-- (Tire is Flat)     |                                   |   |  |
|  |          |   Inject Garbage     v                                   v   |  |
|  +----------|------------------ SetWindowPos() -------------- SendInput() -+  |
|             |                   (Win32 API)                  (Junk Chars)      |
|             v                                                                  |
|   (Suppress or Pass Through)                                                   |
|             v                                                                  |
|   [ Active Foreground App ] <--------------------------------------------------+
+-------------------------------------------------------------------------------+

# Build Photos
<img width="1395" height="242" alt="Screenshot 2026-09-12 202927" src="https://github.com/user-attachments/assets/624bfc5c-0671-475e-99e7-13e77403a23f" />
<img width="1367" height="865" alt="Screenshot 2026-09-12 203431" src="https://github.com/user-attachments/assets/e5856576-4d5b-43f4-ac77-fb72b96caa78" />




### Project Demo
# Video
[Add your demo video link here]
*Explain what the video demonstrates*

# Additional Demos
[Add any extra demo materials/links]

## Team Contributions
- Jagath Krishna: 
- Joel Shaji Mathew:

---
Made with ❤️ at TinkerHub Useless Projects 

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProjects--26-26?link=https%3A%2F%2Ftinkerhub.org%2Fevents%2F1M8ORET9A1%2Fuseless-projects-3.0)
