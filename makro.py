import customtkinter as ctk
import threading, time, sys, os, urllib.request, win32api, win32con, win32gui, psutil
from pynput import keyboard
from tkinter import messagebox

# ==== CONFIGURACIÓN GENERAL ====
VERSIÓN_LOCAL = "1.0.0"
PASS_DIARIA = "shmakro"
PASS_MAESTRA = "ashmakroingv1"
ARCHIVO_BYPASS = "bypass.macro"

ctk.set_appearance_mode("dark")
COLOR_PRIMARY = "#c70039"
COLOR_SECONDARY = "#888888"
COLOR_BG = "#000000"

# ==== 1. VERIFICACIÓN DE ACTUALIZACIÓN ====
def obtener_versión_remota():
    try:
        url = "https://raw.githubusercontent.com/shwrought/makro-updater/main/version.txt"
        with urllib.request.urlopen(url) as response:
            return response.read().decode().strip()
    except:
        return None

temp = ctk.CTk()
temp.withdraw()
versión_remota = obtener_versión_remota()
if versión_remota and versión_remota != VERSIÓN_LOCAL:
    messagebox.showwarning("🔄 Actualización requerida", f"Hay una nueva versión ({versión_remota}) disponible.\n\nDescárgala desde:\nhttps://github.com/shwrought/makro-updater\n\nEl programa se cerrará.")
    sys.exit()

# ==== 2. VERIFICACIÓN DE CONTRASEÑA ====
if not os.path.exists(ARCHIVO_BYPASS):
    root = ctk.CTk()
    root.geometry("300x160")
    root.title("🔒 Ingreso necesario")
    root.resizable(False, False)
    root.configure(fg_color=COLOR_BG)

    FONT_TITLE = ctk.CTkFont(family="Impact", size=22)
    FONT_TEXT = ctk.CTkFont(family="Consolas", size=13)

    ctk.CTkLabel(root, text="m a k я σ", font=FONT_TITLE, text_color=COLOR_PRIMARY).pack(pady=(15, 5))
    ctk.CTkLabel(root, text="Ingresa la contraseña:", font=FONT_TEXT, text_color=COLOR_SECONDARY).pack()

    entry = ctk.CTkEntry(root, show="*", font=FONT_TEXT, justify="center", width=200)
    entry.pack(pady=10)
    entry.focus_set()

    def verificar():
        valor = entry.get()
        if valor == PASS_MAESTRA:
            with open(ARCHIVO_BYPASS, "w") as f:
                f.write("ok")
            root.quit()
        elif valor == PASS_DIARIA:
            root.quit()
        else:
            messagebox.showerror("Error", "🔒 Contraseña incorrecta.")
            root.destroy()
            sys.exit()

    ctk.CTkButton(root, text="Entrar", command=verificar, font=FONT_TEXT).pack(pady=5)
    root.mainloop()
    root.destroy()

# ==== 3. AUTOCLICKER ====
p = psutil.Process(os.getpid())
p.nice(psutil.HIGH_PRIORITY_CLASS)

app = ctk.CTk()
app.title("м a k я σ")
app.geometry("400x390")
app.resizable(False, False)
app.configure(fg_color=COLOR_BG)

FONT_TITLE = ctk.CTkFont(family="Impact", size=26, weight="bold")
FONT_TEXT = ctk.CTkFont(family="Consolas", size=13)
FONT_STATUS = ctk.CTkFont(family="Consolas", size=12, weight="bold")

class AutoClicker:
    def __init__(self):
        self.running = False
        self.toggle_mode = True
        self.clicks_per_action = 1
        self.delay = 0.00001
        self.activation_key = keyboard.Key.f1
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        self.holding = False
        self.burst_active = False

    def click_mouse(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def is_roblox_active(self):
        try:
            hwnd = win32gui.GetForegroundWindow()
            return "roblox" in win32gui.GetWindowText(hwnd).lower()
        except:
            return False

    def click_loop(self):
        while self.running:
            if self.is_roblox_active():
                for _ in range(self.clicks_per_action):
                    self.click_mouse()
                    time.sleep(0.00001)
            time.sleep(self.delay)

    def burst_click(self):
        while self.burst_active and self.is_roblox_active():
            for _ in range(10):
                self.click_mouse()
                time.sleep(0.0001)
            time.sleep(0.0001)

    def on_press(self, key):
        if key == self.activation_key:
            if self.toggle_mode:
                self.running = not self.running
                if self.running:
                    threading.Thread(target=self.click_loop, daemon=True).start()
            else:
                if not self.running:
                    self.running = True
                    self.holding = True
                    threading.Thread(target=self.click_loop, daemon=True).start()
        elif hasattr(key, "char") and key.char.lower() == "c":
            if not self.burst_active:
                self.burst_active = True
                threading.Thread(target=self.burst_click, daemon=True).start()

    def on_release(self, key):
        if key == self.activation_key and not self.toggle_mode:
            self.running = False
            self.holding = False
        elif hasattr(key, "char") and key.char.lower() == "c":
            self.burst_active = False

    def set_clicks(self, val):
        self.clicks_per_action = int(val)

    def set_mode(self, toggle):
        self.toggle_mode = toggle

    def set_key(self, key_str):
        try:
            if len(key_str) == 1:
                self.activation_key = keyboard.KeyCode.from_char(key_str.lower())
            else:
                self.activation_key = getattr(keyboard.Key, key_str.lower())
        except:
            messagebox.showerror("Error", f"Tecla '{key_str}' no válida.")

clicker = AutoClicker()

# UI
ctk.CTkLabel(app, text="мakяσ", font=FONT_TITLE, text_color=COLOR_PRIMARY).pack(pady=10)

ctk.CTkLabel(app, text="tıklama modo", font=FONT_TEXT, text_color=COLOR_SECONDARY).pack()
click_mode = ctk.CTkOptionMenu(app, values=[str(i) for i in range(1, 10)], command=lambda val: clicker.set_clicks(val), font=FONT_TEXT)
click_mode.set("1")
click_mode.pack(pady=9)

ctk.CTkLabel(app, text="Modo de Activación", font=FONT_TEXT, text_color=COLOR_SECONDARY).pack()
toggle_switch = ctk.CTkSwitch(app, text="Toggle (ON) / Hold (OFF)", command=lambda: clicker.set_mode(toggle_switch.get()), font=FONT_TEXT)
toggle_switch.select()
toggle_switch.pack(pady=5)

ctk.CTkLabel(app, text="Tecla Activadora (Ej: F1, a, b...)", font=FONT_TEXT, text_color=COLOR_SECONDARY).pack()
key_entry = ctk.CTkEntry(app, placeholder_text="F1", font=FONT_TEXT)
key_entry.pack(pady=5)

def apply_key():
    new_key = key_entry.get()
    if new_key:
        clicker.set_key(new_key)

ctk.CTkButton(app, text="Aplicar Tecla", command=apply_key, font=FONT_TEXT).pack(pady=5)

status_label = ctk.CTkLabel(app, text="Presiona la tecla para iniciar/detener", text_color=COLOR_SECONDARY, font=FONT_STATUS)
status_label.pack(pady=10)

def update_status():
    if clicker.running:
        status_label.configure(text="makro ACTIVO", text_color="green")
    elif clicker.burst_active:
        status_label.configure(text="Modo BURST activo (C)", text_color=COLOR_PRIMARY)
    elif clicker.holding:
        status_label.configure(text="Manteniendo tecla...", text_color="orange")
    else:
        status_label.configure(text="makro INACTIVO", text_color=COLOR_SECONDARY)
    app.after(200, update_status)

def mostrar_autor():
    messagebox.showinfo("Información", "Autor: ashwrought\nEsta macro es potente, úsala con responsabilidad.\n\nDiscord: 01_j4ck")

ctk.CTkButton(app, text="ⓘ Info", font=FONT_TEXT, width=70, height=25, fg_color="#111", hover_color="#222", text_color=COLOR_SECONDARY, corner_radius=12, command=mostrar_autor).place(relx=0.87, rely=0.92, anchor="center")

app.protocol("WM_DELETE_WINDOW", lambda: app.destroy() if messagebox.askokcancel("Salir", "¿Cerrar MACRO UI?") else None)
update_status()
app.mainloop()
