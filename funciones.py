import re
from tkinter import ttk, messagebox

# Lista de los días de la semana usados para los horarios
DIAS_SEMANA = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado"]

# Diccionario global donde se almacenará la información de materias y secciones
info_materias = {}

# Contador para asignar nombres únicos a los archivos de salida
contador_archivos = 1

# Función que lee el archivo PESUM.txt y retorna las materias del trimestre seleccionado
def obtener_materias(trimestre):
    nombre_archivo = "PESUM.txt"
    materias = []
    buscando = False
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                # Buscar el trimestre solicitado
                if linea.startswith(f"Trimestre {trimestre}"):
                    buscando = True
                    continue
                if buscando:
                    if linea.startswith("Trimestre"):
                        break  # Termina cuando empieza un nuevo trimestre
                    if linea:
                        # Extrae materia y créditos si tiene el formato esperado
                        match = re.match(r"(.+)\s+\((\d+)\s+creditos\)", linea)
                        if match:
                            subject = match.group(1).strip()
                            creditos = int(match.group(2))
                            materias.append({'materia': subject, 'creditos': creditos})
                        else:
                            materias.append({'materia': linea, 'creditos': 0})
        return materias
    except FileNotFoundError:
        messagebox.showerror("Error", f"No se encontro el archivo {nombre_archivo}.")
        return []

# Función que muestra en pantalla una tabla con un horario válido (sin choques)
def mostrar_horario_tabla(parent, combinacion):
    global contador_archivos
        
    # Crear un frame con título y añadirlo al contenedor
    frame = ttk.LabelFrame(parent, text=f"Horario valido #{contador_archivos}")
    frame.pack(fill="x", padx=10, pady=10)

    # Diccionario que almacena qué materia hay en cada hora de cada día
    horario = {dia: {} for dia in DIAS_SEMANA}
    for seccion in combinacion:
        for dia_hora in seccion["dias_horas"]:
            for h in range(dia_hora["hora_inicio"], dia_hora["hora_fin"]):
                horario[dia_hora["dia"]][h] = seccion["materia"]

    # Rango de horas visualizadas (de 7 a.m. a 10 p.m.)
    horas = list(range(7, 23))
    tree = ttk.Treeview(frame, columns=["Hora"] + DIAS_SEMANA, show="headings")
    tree.heading("Hora", text="Hora")
    tree.column("Hora", width=60)
    for dia in DIAS_SEMANA:
        tree.heading(dia, text=dia)
        tree.column(dia, width=100)

    # Llenar cada fila de la tabla con las materias por hora
    for hora in horas:
        row = []
        for dia in DIAS_SEMANA:
            row.append(horario[dia].get(hora, ""))
        tree.insert("", "end", values=[f"{hora}:00"] + row)
    tree.pack()

    # Función interna para guardar el horario mostrado en un archivo .txt
    def guardar_txt():
        nombre = f"Horario_Valido_{contador_archivos}.txt"
        with open(nombre, "w", encoding="utf-8") as f:
            f.write(f"Horario valido #{contador_archivos}\n")
            f.write("="*30 + "\n")
            for seccion in combinacion:
                for dia_hora in seccion["dias_horas"]:
                    f.write(f"{seccion['materia']} - Seccion {seccion['seccion']} - {dia_hora['dia']} {dia_hora['hora_inicio']}:00-{dia_hora['hora_fin']}:00\n")
        messagebox.showinfo("Guardado", f"Archivo '{nombre}' creado.")

    # Botón para guardar
    ttk.Button(frame, text="Guardar como .txt", command=guardar_txt).pack(pady=5)
    contador_archivos += 1

# Función principal que genera todas las combinaciones de horarios válidos usando backtracking
def generar_horarios_posibles(container):
    # Limpia el contenedor antes de mostrar nuevos resultados
    for widget in container.winfo_children():
        widget.destroy()

    materias = list(info_materias.keys())
    valid_schedules = []
    creditos_por_materia = {}

    # Obtener los créditos por materia
    for subject in materias:
        if info_materias[subject]:
            creditos_por_materia[subject] = info_materias[subject][0].get("creditos", 0)
        else:
            creditos_por_materia[subject] = 0

    # Ordenar materias por cantidad de créditos (mayor a menor)
    materias.sort(key=lambda s: creditos_por_materia[s], reverse=True)

    # Función auxiliar que verifica si una nueva sección choca con las ya asignadas
    def conflicto(current_schedule, nueva_seccion):
        for seccion in current_schedule:
            for dh in seccion["dias_horas"]:
                for ndh in nueva_seccion["dias_horas"]:
                    if dh["dia"] == ndh["dia"]:
                        if not (ndh["hora_fin"] <= dh["hora_inicio"] or ndh["hora_inicio"] >= dh["hora_fin"]):
                            return True
        return False

    # Algoritmo recursivo de backtracking que explora todas las combinaciones posibles
    def backtracking(index, current_schedule, total_creditos):
        # Si ya se asignaron todas las materias, guardar esta combinación
        if index == len(materias):
            valid_schedules.append(current_schedule.copy())
            return

        subject = materias[index]
        creditos = creditos_por_materia.get(subject, 0)

        # Si se pasa del máximo de créditos permitidos, no seguir
        if total_creditos + creditos > 22:
            return

        # Probar cada sección de la materia actual
        for seccion in info_materias[subject]:
            if not conflicto(current_schedule, seccion):
                current_schedule.append(seccion)
                backtracking(index + 1, current_schedule, total_creditos + creditos)
                current_schedule.pop()  # Retrocede para probar otra opción

    # Llamada inicial al backtracking
    backtracking(0, [], 0)

    # Mostrar resultados si se encontraron combinaciones
    if valid_schedules:
        for schedule in valid_schedules:
            mostrar_horario_tabla(container, schedule)
    else:
        messagebox.showwarning("Sin horarios validos", "No se pudieron generar horarios válidos.")
