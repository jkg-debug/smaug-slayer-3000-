"""
Pothole Keyboard Simulator (Windows)
=====================================
Turns typing into a hazardous commute.

One ordinary key on your keyboard is secretly declared a "pothole." Every
single time you hit it:
  1. Your active window is violently shaken (like hitting suspension damage)
  2. Your cursor drops 3 lines down into your text
  3. A burst of garbage characters gets typed at that spot

From that point on, EVERY key you press produces a random garbage
character instead of what you actually typed — the "flat tire" state —
until you hold BACKSPACE for 1 straight second to "repair the tire."
A loading-bar overlay tracks the hold in real time and flips to
"TIRE REPAIRED" the moment you clear the threshold. Only once repaired
does a brand-new pothole get planted on a different key.

Requirements:
    pip install keyboard pywin32

Run:
    python pothole_keyboard.py
    (Run as Administrator if key hooking doesn't seem to register)

Quit any time:
    Hold BACKSPACE for 8 straight seconds (longer than a repair hold)
"""

import random
import string
import threading
import time
import tkinter as tk

import keyboard
import win32con
import win32gui

# ---------------------------------------------------------------------------
# CONFIG — tune the chaos here
# ---------------------------------------------------------------------------
CANDIDATE_KEYS = list(string.ascii_lowercase) + ["space"]
REPAIR_HOLD_SECONDS = 1.0       # how long to hold Backspace to fix the tire
SHAKE_DURATION = 3.0            # seconds the window shakes for
SHAKE_AMPLITUDE = 15            # pixels of shake wobble
GARBAGE_MIN_LEN = 5
GARBAGE_MAX_LEN = 15
CURSOR_DROP_LINES = 3
QUIT_HOLD_SECONDS = 8.0         # hold Backspace this long (from any state) to quit
GARBAGE_ALPHABET = string.ascii_letters + string.digits + "!@#$%^&*"

REPAIR_BAR_WIDTH = 400
REPAIR_BAR_HEIGHT = 28
REPAIR_DONE_TEXT = "🔧 TIRE REPAIRED 🔧"
REPAIR_HOLD_MS = 700            # how long the "repaired" state stays fully visible
REPAIR_STEP_MS = 20             # animation frame interval

# ---------------------------------------------------------------------------
# STATE
# ---------------------------------------------------------------------------
_state_lock = threading.Lock()
_pothole_key = None
_tire_flat = False
_backspace_down_since = None
_stop_event = threading.Event()


def _log(msg: str) -> None:
    print(f"[pothole] {msg}")


# ---------------------------------------------------------------------------
# WINDOW SHAKE
# ---------------------------------------------------------------------------
def shake_window() -> None:
    hwnd = win32gui.GetForegroundWindow()
    if not hwnd:
        return
    try:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        end_time = time.time() + SHAKE_DURATION
        while time.time() < end_time:
            dx = random.randint(-SHAKE_AMPLITUDE, SHAKE_AMPLITUDE)
            dy = random.randint(-SHAKE_AMPLITUDE, SHAKE_AMPLITUDE)
            win32gui.SetWindowPos(
                hwnd, None, left + dx, top + dy, 0, 0,
                win32con.SWP_NOSIZE | win32con.SWP_NOZORDER
            )
            time.sleep(0.02)
        # snap back to original position
        win32gui.SetWindowPos(
            hwnd, None, left, top, 0, 0,
            win32con.SWP_NOSIZE | win32con.SWP_NOZORDER
        )
    except Exception as exc:  # some windows (elevated apps, etc.) may refuse
        _log(f"couldn't shake window ({exc})")


# ---------------------------------------------------------------------------
# CHAOS TYPING
# ---------------------------------------------------------------------------
def chaos_burst() -> None:
    """Initial hit: drop the cursor a few lines and spray a burst of garbage."""
    time.sleep(0.05)
    for _ in range(CURSOR_DROP_LINES):
        keyboard.send("down")
        time.sleep(0.02)
    length = random.randint(GARBAGE_MIN_LEN, GARBAGE_MAX_LEN)
    garbage = "".join(random.choices(GARBAGE_ALPHABET, k=length))
    keyboard.write(garbage, delay=0.01)


def inject_garbage_char() -> None:
    """Ongoing flat-tire effect: replace one keystroke with one garbage char."""
    time.sleep(0.005)
    keyboard.write(random.choice(GARBAGE_ALPHABET))


# ---------------------------------------------------------------------------
# REPAIR PROGRESS OVERLAY — a loading bar that fills as you hold Backspace,
# then flips to "TIRE REPAIRED" and fades out once you clear the threshold.
# If you let go early, it aborts and fades out instead.
# ---------------------------------------------------------------------------
def show_repair_progress(hold_start: float) -> None:
    def run() -> None:
        root = tk.Tk()
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        root.attributes("-alpha", 0.95)

        width, height = 480, 140
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 3
        root.geometry(f"{width}x{height}+{x}+{y}")
        root.configure(bg="#1b1b1b")

        title = tk.Label(
            root, text="🔧 Repairing tire...", font=("Segoe UI", 16, "bold"),
            fg="white", bg="#1b1b1b",
        )
        title.pack(pady=(18, 10))

        bar_bg = tk.Canvas(
            root, width=REPAIR_BAR_WIDTH, height=REPAIR_BAR_HEIGHT,
            bg="#3a3a3a", highlightthickness=0,
        )
        bar_bg.pack()
        bar_fill = bar_bg.create_rectangle(0, 0, 0, REPAIR_BAR_HEIGHT, width=0, fill="#43a047")

        def fade_out(alpha: float) -> None:
            alpha = max(0.0, alpha - 0.1)
            try:
                root.attributes("-alpha", alpha)
            except tk.TclError:
                return
            if alpha > 0.0:
                root.after(REPAIR_STEP_MS, fade_out, alpha)
            else:
                root.destroy()

        def tick() -> None:
            with _state_lock:
                still_holding = _backspace_down_since is not None
                still_flat = _tire_flat

            elapsed = time.time() - hold_start
            progress = min(1.0, elapsed / REPAIR_HOLD_SECONDS)
            bar_bg.coords(bar_fill, 0, 0, REPAIR_BAR_WIDTH * progress, REPAIR_BAR_HEIGHT)

            if not still_flat or progress >= 1.0:
                # Repaired! Fill the bar completely and announce it.
                bar_bg.coords(bar_fill, 0, 0, REPAIR_BAR_WIDTH, REPAIR_BAR_HEIGHT)
                bar_bg.itemconfig(bar_fill, fill="#2e7d32")
                title.config(text=REPAIR_DONE_TEXT)
                root.after(REPAIR_HOLD_MS, lambda: fade_out(0.95))
                return

            if not still_holding:
                # Released early — abort.
                bar_bg.itemconfig(bar_fill, fill="#c62828")
                title.config(text="Repair aborted")
                root.after(300, lambda: fade_out(0.95))
                return

            root.after(REPAIR_STEP_MS, tick)

        root.after(REPAIR_STEP_MS, tick)
        root.mainloop()

    threading.Thread(target=run, daemon=True).start()


# ---------------------------------------------------------------------------
# POTHOLE PLACEMENT (event-driven — only moves once the tire is repaired)
# ---------------------------------------------------------------------------
def plant_new_pothole() -> None:
    global _pothole_key
    with _state_lock:
        choices = [k for k in CANDIDATE_KEYS if k != _pothole_key]
        _pothole_key = random.choice(choices)
    _log(f"New pothole quietly planted on key: '{_pothole_key}'")


def trigger_pothole_hit() -> None:
    global _tire_flat
    hit_key = _pothole_key
    with _state_lock:
        _tire_flat = True
    _log(f"BAM! Hit the '{hit_key}' pothole. Tire is flat — every key now "
         f"types gibberish. Hold Backspace for {REPAIR_HOLD_SECONDS:.0f}s to repair.")
    threading.Thread(target=shake_window, daemon=True).start()
    threading.Thread(target=chaos_burst, daemon=True).start()


# ---------------------------------------------------------------------------
# GLOBAL KEY FILTER — one hook decides what every keystroke does
# ---------------------------------------------------------------------------
def global_key_filter(event: keyboard.KeyboardEvent) -> bool:
    """Return True to let the real keystroke through, False to swallow it."""
    global _backspace_down_since, _tire_flat

    if event.event_type == keyboard.KEY_UP:
        if event.name == "backspace":
            _backspace_down_since = None
        return True

    # --- KEY_DOWN from here ---
    if event.name == "backspace":
        with _state_lock:
            flat = _tire_flat

        if _backspace_down_since is None:
            _backspace_down_since = time.time()
            if flat:
                threading.Thread(
                    target=show_repair_progress, args=(_backspace_down_since,), daemon=True
                ).start()

        held_for = time.time() - _backspace_down_since

        if held_for >= QUIT_HOLD_SECONDS:
            _log(f"Backspace held {QUIT_HOLD_SECONDS:.0f}s — pulling over for good.")
            _stop_event.set()
            return True

        if flat and held_for >= REPAIR_HOLD_SECONDS:
            with _state_lock:
                _tire_flat = False
            _log("Tire repaired! Keyboard is smooth again.")
            plant_new_pothole()
            _backspace_down_since = None
        return True  # always let real Backspace through so you can clean up

    with _state_lock:
        flat = _tire_flat

    if not flat:
        if event.name == _pothole_key:
            threading.Thread(target=trigger_pothole_hit, daemon=True).start()
            return False  # swallow the real pothole character
        return True  # ordinary typing, ordinary road

    # Flat tire: every other key produces gibberish instead of itself.
    threading.Thread(target=inject_garbage_char, daemon=True).start()
    return False


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main() -> None:
    print("=== Pothole Keyboard Simulator ===")
    print(f"Hold Backspace for {REPAIR_HOLD_SECONDS:.0f}s to repair a flat tire, "
          f"or {QUIT_HOLD_SECONDS:.0f}s to quit.")
    print("Driving...\n")

    plant_new_pothole()
    keyboard.hook(global_key_filter, suppress=True)

    try:
        while not _stop_event.is_set():
            time.sleep(0.25)
    except KeyboardInterrupt:
        pass
    finally:
        keyboard.unhook_all()
        print("\n[pothole] Ride complete. Keyboard restored to full safety.")


if __name__ == "__main__":
    main()
