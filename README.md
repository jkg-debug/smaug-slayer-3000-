# Pothole Keyboard Simulator

Turns typing into a hazardous commute. One ordinary key is secretly a
"pothole." Hit it, and:

1. Your active window violently shakes for ~5 seconds (suspension damage).
2. Your cursor drops 3 lines down into your text.
3. A burst of garbage characters gets typed at that spot.
4. The pothole immediately relocates to a new random key.
5. **Every key you press from then on types a random garbage character
   instead of itself** — you're driving on a flat — until you hold
   **Backspace** for a continuous **2 seconds** to "repair the tire."

Hold Backspace for a continuous **8 seconds** at any time to quit the
whole script outright.

## Setup

```
pip install -r requirements.txt
```

(`keyboard` handles the global key hook, `pywin32` handles shaking the
window via the Win32 API.)

## Run

```
python pothole_keyboard.py
```

If key hooking doesn't seem to register (some apps run elevated), try
running your terminal as Administrator.

## Quit

Hold **Backspace** for 8 continuous seconds — no separate hotkey needed,
and it works even mid-pothole.

## Tuning the chaos

All the knobs are at the top of `pothole_keyboard.py`:

- `REPAIR_HOLD_SECONDS` — how long you must hold Backspace to fix a flat tire
- `QUIT_HOLD_SECONDS` — how long you must hold Backspace to quit
- `SHAKE_DURATION` / `SHAKE_AMPLITUDE` — how violent and how long the window shake is
- `GARBAGE_MIN_LEN` / `GARBAGE_MAX_LEN` — length of the initial garbage text burst
- `CANDIDATE_KEYS` — which keys are eligible to become potholes (defaults to
  a–z and space; deliberately excludes Backspace and modifier keys so
  you're never fully locked out)

## Notes

- This is a real global key hook — it affects typing in *every* application
  while it's running, not just a sandboxed demo.
- Once you hit a pothole, EVERY keystroke (except Backspace) becomes a
  random garbage character until you repair the tire — plan on your text
  looking like static during that window.
- The cursor-drop effect (`Down` x3) only does something meaningful in
  multi-line text areas (editors, chat boxes, documents) — in single-line
  fields like a URL bar it's a no-op, which is fine.
- Consider this a "high highway hazard" prank tool for your own machine —
  don't leave it running on anything you (or someone else) needs for real
  work in the near term.
