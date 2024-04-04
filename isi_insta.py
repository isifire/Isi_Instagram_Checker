import tkinter as tk
from tkinter import messagebox, Scrollbar
import instaloader
import webbrowser
from tkinter.ttk import Progressbar
import threading

def encontrar_no_seguidores(usuario, contraseña):
    L = instaloader.Instaloader()
    L.login(usuario, contraseña)
    profile = instaloader.Profile.from_username(L.context, usuario)
    seguidores = set(profile.get_followers())
    seguidos = set(profile.get_followees())
    no_seguidores = seguidos - seguidores
    return [usuario.username for usuario in no_seguidores]

def encontrar_no_seguidos(usuario, contraseña):
    L = instaloader.Instaloader()
    L.login(usuario, contraseña)
    profile = instaloader.Profile.from_username(L.context, usuario)
    seguidores = set(profile.get_followers())
    seguidos = set(profile.get_followees())
    no_seguidos = seguidores - seguidos
    return [usuario.username for usuario in no_seguidos]

def abrir_perfil(nombre):
    url = f"https://www.instagram.com/{nombre}/"
    webbrowser.open_new_tab(url)

def buscar_no_seguidores(usuario, contraseña, progress_bar):
    try:
        no_seguidores = encontrar_no_seguidores(usuario, contraseña)
        if no_seguidores:
            mostrar_lista(usuario, "No Seguidores", no_seguidores)
        else:
            messagebox.showinfo("No Seguidores", "¡Genial! Todos te siguen de vuelta.")
    except instaloader.exceptions.BadCredentialsException:
        messagebox.showerror("Error", "Credenciales incorrectas. Inténtalo de nuevo.")
    finally:
        progress_bar.stop()
        progress_bar.config(value=100, mode='determinate', style='green.Horizontal.TProgressbar')

def buscar_no_seguidos(usuario, contraseña, progress_bar):
    try:
        no_seguidos = encontrar_no_seguidos(usuario, contraseña)
        if no_seguidos:
            mostrar_lista(usuario, "No Seguidos", no_seguidos)
        else:
            messagebox.showinfo("No Seguidos", "¡Genial! Sigues a todos tus seguidores.")
    except instaloader.exceptions.BadCredentialsException:
        messagebox.showerror("Error", "Credenciales incorrectas. Inténtalo de nuevo.")
    finally:
        progress_bar.stop()
        progress_bar.config(value=100, mode='determinate', style='green.Horizontal.TProgressbar')

def mostrar_lista(usuario, titulo, lista):
    ventana_no_seguidores = tk.Toplevel(root)
    ventana_no_seguidores.title(titulo)
    ventana_no_seguidores.geometry("400x300")

    scrollbar = Scrollbar(ventana_no_seguidores, orient="vertical")
    lista_no_seguidores = tk.Listbox(ventana_no_seguidores, yscrollcommand=scrollbar.set)
    scrollbar.config(command=lista_no_seguidores.yview)

    for nombre in lista:
        lista_no_seguidores.insert(tk.END, nombre)
    lista_no_seguidores.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    lista_no_seguidores.bind("<Double-Button-1>", lambda event: abrir_perfil(lista_no_seguidores.get(tk.ACTIVE)))

def restablecer_barra_de_progreso():
    progress_bar.config(value=0, mode='determinate')

def verificar_no_seguidores():
    usuario = username_entry.get()
    contraseña = password_entry.get()
    restablecer_barra_de_progreso()
    progress_bar.start()
    threading.Thread(target=lambda: buscar_no_seguidores(usuario, contraseña, progress_bar)).start()

def verificar_no_seguidos():
    usuario = username_entry.get()
    contraseña = password_entry.get()
    restablecer_barra_de_progreso()
    progress_bar.start()
    threading.Thread(target=lambda: buscar_no_seguidos(usuario, contraseña, progress_bar)).start()

root = tk.Tk()
root.title("Isi Insta Tool")

window_width = 400
window_height = 250
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width / 2) - (window_width / 2)
y_coordinate = (screen_height / 2) - (window_height / 2)
root.geometry(f"{window_width}x{window_height}+{int(x_coordinate)}+{int(y_coordinate)}")

username_label = tk.Label(root, text="Usuario de Instagram:")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

password_label = tk.Label(root, text="Contraseña de Instagram:")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

verificar_no_seguidores_button = tk.Button(root, text="Verificar No Seguidores", command=verificar_no_seguidores, width=20)
verificar_no_seguidores_button.pack(pady=(10, 5))

verificar_no_seguidos_button = tk.Button(root, text="Verificar No Seguidos", command=verificar_no_seguidos, width=20)
verificar_no_seguidos_button.pack(pady=5)

progress_bar = Progressbar(root, orient=tk.HORIZONTAL, length=300, mode='determinate', style='blue.Horizontal.TProgressbar')
progress_bar.pack(pady=20)

root.mainloop()
