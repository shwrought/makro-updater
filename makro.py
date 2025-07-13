import customtkinter as ctk
import threading, time, sys, os, urllib.request, win32api, win32con, psutil
from pynput import keyboard
from tkinter import messagebox

# ==== CONFIGURACIÓN GENERAL ====
VERSIÓN_LOCAL = "1.2.0"
PASS_DIARIA = "shmakro"
PASS_MAESTRA = "ashmakroingv1"
ARCHIVO_BYPASS = "bypass.macro"

# Apariencia
ctk.set_appearance_mode("dark")
COLOR_PRIMARY = "#c70039"
COLOR_SECONDARY = "#888888"
COLOR_BG = "#000000"

# ==== SPLASH SCREEN ====
def mostrar_splash():
    splash = ctk.CTk()
    splash.geometry("400x220")
    splash.title("Cargando...")
    splash.configure(fg_color=COLOR_BG)
    splash.overrideredirect(True)

    FONT_TITLE = ctk.CTkFont(family="Impact", size=26)
    ctk.CTkLabel(splash, text="m a k я σ", font=FONT_TITLE, text_color=COLOR_PRIMARY).pack(expand=True)
    ctk.CTkLabel(splash, text="Cargando...", text_color=COLOR_SECONDARY).pack(pady=(0, 20))

    splash.after(3000, splash.destroy)
    splash.mainloop()

mostrar_splash()

# ==== VERIFICACIÓN DE ACTUALIZACIÓN ====
def obtener_versión_remota():
    try:
        url = "https://raw.githubusercontent.com/shwrought/makro-updater/main/version.txt"
        with urllib.request.urlopen(url) as response:
            return response.read().decode().strip()
    except:
        return None

def obtener_link_descarga():
    try:
        url = "https://raw.githubusercontent.com/shwrought/makro-updater/main/mega_link.txt"
        with urllib.request.urlopen(url) as response:
            return response.read().decode().strip()
    except:
        return "https://mega.nz/"

versión_remota = obtener_versión_remota()
if versión_remota and versión_remota != VERSIÓN_LOCAL:
    descarga = obtener_link_descarga()

    aviso = ctk.CTk()
    aviso.title("Actualización Disponible")
    aviso.geometry("460x250")
    aviso.resizable(False, False)
    aviso.configure(fg_color=COLOR_BG)

    FONT_TITLE = ctk.CTkFont(family="Impact", size=23)
    FONT = ctk.CTkFont(family="Consolas", size=13)

    ctk.CTkLabel(aviso, text=" ¡Hay una nueva versión!", font=FONT_TITLE, text_color=COLOR_PRIMARY).pack(pady=(20, 10))
    ctk.CTkLabel(aviso, text=f"Versión actual: {VERSIÓN_LOCAL} | Nueva: {versión_remota}", font=FONT, text_color=COLOR_SECONDARY).pack()

    ctk.CTkLabel(aviso, text="Enlace de descarga:", font=FONT, text_color=COLOR_SECONDARY).pack(pady=(10, 2))
    enlace_entry = ctk.CTkEntry(aviso, font=FONT, width=350)
    enlace_entry.insert(0, descarga)
    enlace_entry.configure(state="readonly")
    enlace_entry.pack(pady=(0, 15))

    ctk.CTkLabel(aviso, text="No podrás usar la macro hasta actualizar.", font=FONT, text_color="#ff5555").pack()

    def cerrar():
        aviso.destroy()
        sys.exit()

    ctk.CTkButton(aviso, text="Cerrar", command=cerrar, font=FONT).pack(pady=10)
    aviso.protocol("WM_DELETE_WINDOW", cerrar)
    aviso.mainloop()

# ==== VERIFICACIÓN DE CONTRASEÑA ====
if not os.path.exists(ARCHIVO_BYPASS):
    acceso = ctk.CTk()
    acceso.title("🔒 Ingreso necesario")
    acceso.geometry("300x160")
    acceso.resizable(False, False)
    acceso.configure(fg_color=COLOR_BG)

    FONT_TITLE = ctk.CTkFont(family="Impact", size=22)
    FONT_TEXT = ctk.CTkFont(family="Consolas", size=13)

    ctk.CTkLabel(acceso, text="m a k я σ", font=FONT_TITLE, text_color=COLOR_PRIMARY).pack(pady=(15, 5))
    ctk.CTkLabel(acceso, text="Ingresa la contraseña:", font=FONT_TEXT, text_color=COLOR_SECONDARY).pack()

    entry = ctk.CTkEntry(acceso, show="*", font=FONT_TEXT, justify="center", width=200)
    entry.pack(pady=10)
    entry.focus_set()

    def verificar():
        valor = entry.get()
        if valor == PASS_MAESTRA:
            with open(ARCHIVO_BYPASS, "w") as f:
                f.write("ok")
            acceso.destroy()
        elif valor == PASS_DIARIA:
            acceso.destroy()
        else:
            messagebox.showerror("Error", "🔒 Contraseña incorrecta.")
            acceso.destroy()
            sys.exit()

    def cerrar_acceso():
        acceso.destroy()
        sys.exit()

    ctk.CTkButton(acceso, text="Entrar", command=verificar, font=FONT_TEXT).pack(pady=5)
    acceso.protocol("WM_DELETE_WINDOW", cerrar_acceso)
    acceso.mainloop()

# ==== AUTOCLICKER ====
p = psutil.Process(os.getpid())
p.nice(psutil.HIGH_PRIORITY_CLASS)

app = ctk.CTk()
app.title("м a k я σ")
app.geometry("600x400")
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

    def click_loop(self):
        while self.running:
            for _ in range(self.clicks_per_action):
                self.click_mouse()
                time.sleep(0.00001)
            time.sleep(self.delay)

    def burst_click(self):
        while self.burst_active:
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

    def set_key_object(self, key_obj):
        self.activation_key = key_obj

clicker = AutoClicker()

# ==== UI ====
left_frame = ctk.CTkFrame(app, fg_color="transparent")
left_frame.pack(side="left", fill="both", expand=True, padx=15, pady=15)

right_frame = ctk.CTkFrame(app, fg_color="#111111", width=170, height=300, corner_radius=10)
right_frame.pack(side="right", fill="y", pady=15, padx=(0, 15))

ctk.CTkLabel(left_frame, text="мakяσ", font=FONT_TITLE, text_color=COLOR_PRIMARY).pack(pady=10)

ctk.CTkLabel(left_frame, text="tıklama modo", font=FONT_TEXT, text_color=COLOR_SECONDARY).pack()
click_mode = ctk.CTkOptionMenu(left_frame, values=[str(i) for i in range(1, 10)], command=lambda val: clicker.set_clicks(val), font=FONT_TEXT)
click_mode.set("1")
click_mode.pack(pady=9)

ctk.CTkLabel(left_frame, text="Modo de Activación", font=FONT_TEXT, text_color=COLOR_SECONDARY).pack()
toggle_switch = ctk.CTkSwitch(left_frame, text="Toggle / Hold ", command=lambda: clicker.set_mode(toggle_switch.get()), font=FONT_TEXT)
toggle_switch.select()
toggle_switch.pack(pady=5)

ctk.CTkLabel(left_frame, text="Presiona una tecla para asignarla", font=FONT_TEXT, text_color=COLOR_SECONDARY).pack()
def escuchar_tecla():
    def capturar(key):
        clicker.set_key_object(key)
        listener.stop()

    listener = keyboard.Listener(on_press=capturar)
    listener.start()

ctk.CTkButton(left_frame, text="Cambiar Tecla", command=escuchar_tecla, font=FONT_TEXT).pack(pady=5)

status_label = ctk.CTkLabel(left_frame, text="Presiona la tecla para iniciar/detener", text_color=COLOR_SECONDARY, font=FONT_STATUS)
status_label.pack(pady=10)

def mostrar_autor():
    messagebox.showinfo("Información", "Autor: ashwrought\nEsta macro es potente, úsala con responsabilidad.\n\nDiscord: 01_j4ck")

ctk.CTkButton(app, text="ⓘ Info", font=FONT_TEXT, width=70, height=25, fg_color="#111", hover_color="#222", text_color=COLOR_SECONDARY, corner_radius=12, command=mostrar_autor).place(relx=0.87, rely=0.92, anchor="center")

# ==== CHANGELOG DESDE EL SCRIPT ====
def obtener_changelog():
    return """
-Fixes errors

-wait screen

-password changed

"""

ctk.CTkLabel(right_frame, text=" CHANGELOGS", text_color=COLOR_PRIMARY, font=FONT_TEXT).pack(pady=(10, 5))
changelog_box = ctk.CTkTextbox(right_frame, font=FONT_TEXT, width=170, height=280, fg_color="#111111", text_color=COLOR_SECONDARY, corner_radius=8)
changelog_box.insert("0.0", obtener_changelog())
changelog_box.configure(state="disabled")
changelog_box.pack()

# ==== STATUS DINÁMICO ====
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

app.protocol("WM_DELETE_WINDOW", lambda: app.destroy() if messagebox.askokcancel("Salir", "¿Quieres cerrar MACRO sh?") else None)
update_status()
app.mainloop()
