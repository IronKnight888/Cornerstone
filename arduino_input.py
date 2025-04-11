import time
import pygame

def connect_arduino():
    try:
        import serial
        ser = serial.Serial("COM12", 9600, timeout=1)
        time.sleep(2)
        print("✅ Arduino connected.")
        return ser
    except Exception:
        print("⚠️ Arduino not connected. Press 'Z' to simulate button.")
        return None

def wait_for_button(ser):
    if ser is None:
        pygame.event.pump()  # Allow key state update
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            print("🧪 Simulated Z key press.")
            time.sleep(0.3)  # prevent multiple triggers
            return True
        return False

    if ser.in_waiting > 0:
        line = ser.readline().decode().strip()
        if "Left button pressed" in line:
            return True

    return False
