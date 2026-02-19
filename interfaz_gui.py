import tkinter as tk
from tkinter import ttk, messagebox
from funciones import obtener_materias, generar_horarios_posibles, info_materias, DIAS_SEMANA

# Función principal que lanza la interfaz gráfica
def mostrar_gui():
    
    # Función que carga las materias del trimestre seleccionado
    def mostrar_materias():
        for widget in frame_materias.winfo_children():
            widget.destroy()
        info_materias.clear()
        opcion = combo.get()
        if opcion:
            trimestre = int(opcion.split()[-1])
            materias_lista = obtener_materias(trimestre)
            if materias_lista:
                for subject in materias_lista:
                    crear_widget_materia(frame_materias, subject)
            else:
                messagebox.showwarning("Advertencia", "No se encontraron materias.")

    # Crea los controles gráficos para una materia específica
    def crear_widget_materia(parent, subject):
        nombre = subject['materia']
        creditos = subject['creditos']

        # Etiqueta con el nombre de la materia y sus créditos
        label = ttk.Label(parent, text=f"{nombre} ({creditos} creditos)", font=("Segoe UI", 10, "bold"))
        label.pack(anchor="w", padx=10, pady=5)

        frame_secciones = ttk.Frame(parent)
        frame_secciones.pack(padx=20, pady=5)

        # Selector para el número de secciones que tendrá esta materia
        spin_var = tk.IntVar(value=1)
        spin = ttk.Spinbox(frame_secciones, from_=1, to=5, textvariable=spin_var, width=5, state="readonly")
        spin.grid(row=0, column=0, padx=5)
        ttk.Label(frame_secciones, text="secciones").grid(row=0, column=1, padx=5)

        secciones_data = []

        # Genera la entrada de horarios para cada sección
        def generar_secciones():
            for widget in frame_dinamico.winfo_children():
                widget.destroy()
            secciones_data.clear()

            for s in range(spin_var.get()):
                ttk.Label(frame_dinamico, text=f"Seccion {s+1}:").pack(anchor="w")
                dia_frames = []
                for dia in DIAS_SEMANA:
                    frame = ttk.Frame(frame_dinamico)
                    frame.pack(anchor="w", pady=2)

                    # Checkbox para seleccionar el día
                    var = tk.BooleanVar()
                    chk = ttk.Checkbutton(frame, text=dia, variable=var)
                    chk.pack(side="left")

                    # ComboBoxes para seleccionar hora de inicio y fin
                    ttk.Label(frame, text="Inicio:").pack(side="left")
                    combo_inicio = ttk.Combobox(frame, width=5, values=[str(h) for h in range(7, 22)], state="disabled")
                    combo_inicio.pack(side="left", padx=2)
                    ttk.Label(frame, text="Fin:").pack(side="left")
                    combo_fin = ttk.Combobox(frame, width=5, values=[str(h) for h in range(8, 23)], state="disabled")
                    combo_fin.pack(side="left", padx=2)

                    # Activa/desactiva los combos según el checkbox
                    def on_toggle(*args, var=var, combo_inicio=combo_inicio, combo_fin=combo_fin):
                        if var.get():
                            combo_inicio.config(state="readonly")
                            combo_fin.config(state="readonly")
                        else:
                            combo_inicio.config(state="disabled")
                            combo_fin.config(state="disabled")
                            combo_inicio.set("")
                            combo_fin.set("")

                    var.trace("w", on_toggle)

                    dia_frames.append({
                        "dia": dia,
                        "var": var,
                        "inicio": combo_inicio,
                        "fin": combo_fin
                    })

                secciones_data.append({
                    "dia_frames": dia_frames,
                    "seccion": str(s+1)
                })

        # Contenedor para los controles dinámicos de secciones
        frame_dinamico = ttk.Frame(parent)
        frame_dinamico.pack(padx=30, pady=5)

        # Botón para crear entradas de secciones
        ttk.Button(frame_secciones, text="Anadir secciones", command=generar_secciones).grid(row=0, column=2, padx=10)

        # Función para guardar la información ingresada de esta materia
        def guardar_info():
            info_materias[nombre] = []
            for datos in secciones_data:
                dias_horas = []
                for dia_info in datos["dia_frames"]:
                    if dia_info["var"].get():
                        try:
                            h_ini = int(dia_info["inicio"].get())
                            h_fin = int(dia_info["fin"].get())
                            if h_ini < h_fin:
                                dias_horas.append({
                                    "dia": dia_info["dia"],
                                    "hora_inicio": h_ini,
                                    "hora_fin": h_fin
                                })
                        except:
                            continue
                if dias_horas:
                    info_materias[nombre].append({
                        "materia": nombre,
                        "creditos": creditos,
                        "seccion": datos["seccion"],
                        "dias_horas": dias_horas
                    })
            messagebox.showinfo("Secciones guardadas", f"Guardadas secciones para {nombre}.")

        # Botón para guardar los datos ingresados para esta materia
        ttk.Button(parent, text=f"Guardar secciones de {nombre}", command=guardar_info).pack(pady=5)

    # ---------- CONFIGURACIÓN GENERAL DE LA INTERFAZ ----------

    root = tk.Tk()
    root.title("Organizador de Horarios")
    root.geometry("1000x750")

    # Combo para seleccionar el trimestre
    ttk.Label(root, text="Selecciona tu trimestre:").pack(pady=10)
    combo = ttk.Combobox(root, values=[f"Trimestre {i}" for i in range(1, 15)], state="readonly")
    combo.pack()

    # Botón que muestra las materias según el trimestre
    ttk.Button(root, text="Mostrar Materias", command=mostrar_materias).pack(pady=10)

    # Frame scrollable para mostrar materias y secciones
    canvas = tk.Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Asignación global del frame de materias para acceder desde otras funciones
    global frame_materias
    frame_materias = scrollable_frame

    # Frame para mostrar los horarios generados
    frame_resultados = ttk.Frame(root)
    frame_resultados.pack(fill="both", expand=True)

    # Botón para generar combinaciones de horarios válidos
    ttk.Button(root, text="Generar Horarios Posibles", command=lambda: generar_horarios_posibles(frame_resultados)).pack(pady=10)

    # Inicia la ventana principal
    root.mainloop()

