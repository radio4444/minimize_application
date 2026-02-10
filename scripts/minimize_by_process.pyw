import time
import ctypes
import psutil
from pywinauto import Desktop

# --- CONFIG ---
# TARGET_PROCESSES = ["Notion.exe", "Code.exe", "Discord.exe"]
TARGET_PROCESSES = ["Notion.exe"]
IDLE_THRESHOLD_MINUTES = 0.5
CHECK_INTERVAL = 1
# --------------


class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]


def get_idle_duration():
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = ctypes.sizeof(LASTINPUTINFO)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lastInputInfo))
    millis = ctypes.windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return millis / 1000.0


def minimize_by_process():
    print("Idle threshold reached. Searching for active windows...")

    # 1. Get all running process IDs for our target apps
    target_pids = []
    for proc in psutil.process_iter(["pid", "name"]):
        if proc.info["name"] in TARGET_PROCESSES:
            target_pids.append(proc.info["pid"])

    # 2. Find windows and apply filters
    windows = Desktop(backend="win32").windows()
    for win in windows:
        if win.process_id() in target_pids:
            title = win.window_text()

            # FILTERS:
            # - Must have a title
            # - Must be visible
            # - Must not be a known system utility window
            # - Must have a real size (not 0x0)
            if (
                title
                and win.is_visible()
                and title not in ["Default IME", "MSCTFIME UI"]
                and win.rectangle().width() > 10
            ):
                try:
                    if win.get_show_state() != 6:  # 6 is code for Minimized
                        print(f"Minimizing: {title}")
                        win.minimize()
                except Exception:
                    continue


def main():
    threshold_seconds = IDLE_THRESHOLD_MINUTES * 60
    already_minimized = False
    print(f"Monitoring Processes: {TARGET_PROCESSES}")

    while True:
        idle_sec = get_idle_duration()
        if idle_sec >= threshold_seconds:
            if not already_minimized:
                minimize_by_process()
                already_minimized = True
        else:
            if already_minimized:
                print("User active. Resetting.")
                already_minimized = False
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
