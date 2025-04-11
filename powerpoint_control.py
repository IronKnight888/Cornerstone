import win32com.client
import time
import os

import pygetwindow as gw
import win32gui
import win32con

PPTX_PATH = r"C:\Users\vedic\Documentos\VSCODE\cornerstone.pptx"

ppt = win32com.client.Dispatch("PowerPoint.Application")
ppt.Visible = True

if not os.path.exists(PPTX_PATH):
    raise FileNotFoundError(f"❌ Could not find PowerPoint file at: {PPTX_PATH}")

presentation = ppt.Presentations.Open(PPTX_PATH, WithWindow=True)

last_slide = None

def focus_powerpoint():
    try:
        window = gw.getWindowsWithTitle("PowerPoint Slide Show")[0]
        hwnd = window._hWnd
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        win32gui.SetForegroundWindow(hwnd)
        print("🎯 Focused PowerPoint window")
        time.sleep(0.5)
    except Exception as e:
        print(f"⚠️ Could not focus PowerPoint: {e}")

def wait_for_slideshow_ready():
    if ppt.SlideShowWindows.Count == 0:
        print("▶️ Starting slideshow...")
        presentation.SlideShowSettings.Run()

    for _ in range(20):
        if ppt.SlideShowWindows.Count > 0:
            print("✅ Slideshow is running.")
            time.sleep(1)
            return

    raise RuntimeError("❌ PowerPoint slideshow never started.")

def go_to_slide(slide_number):
    global last_slide
    try:
        if ppt.SlideShowWindows.Count == 0:
            presentation.SlideShowSettings.Run()
            time.sleep(0.5)

        view = ppt.SlideShowWindows(1).View
        view.GotoSlide(slide_number)
        time.sleep(0.5)

        if slide_number != last_slide:
            focus_powerpoint()
            print(f"📽️ Slide {slide_number}")
            last_slide = slide_number
        time.sleep(0.5)
    except Exception as e:
        print(f"⚠️ Failed to go to slide {slide_number}: {e}")