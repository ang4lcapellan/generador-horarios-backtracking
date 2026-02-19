# Generador de Horarios con Backtracking (Python + Tkinter)

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Algorithm](https://img.shields.io/badge/Algorithm-Backtracking-orange)
![GUI](https://img.shields.io/badge/GUI-Tkinter-green)
![Status](https://img.shields.io/badge/Status-Acad%C3%A9mico-lightgrey)

> Generador de horarios universitarios que utiliza backtracking en Python con interfaz Tkinter para producir combinaciones sin choques de horario.

---

## 📋 Descripción del Proyecto

Este proyecto implementa un **generador automático de horarios universitarios** capaz de producir todas las combinaciones válidas de materias sin conflictos de tiempo.

El sistema permite al usuario seleccionar un trimestre, configurar secciones por materia y generar horarios posibles utilizando un **algoritmo de backtracking**, técnica clásica de exploración exhaustiva en problemas de combinatoria.

El proyecto fue desarrollado para la asignatura **Estructuras de Datos y Algoritmos II**.

---

## ✨ Características Principales

- 📚 Lectura automática del pensum desde `PESUM.txt`
- 🖥️ Interfaz gráfica con Tkinter
- ⚙️ Configuración dinámica de secciones por materia
- 🔍 Detección automática de choques de horario
- 🧠 Generación de combinaciones válidas mediante backtracking
- 💾 Exportación de horarios válidos a archivos `.txt`
- 📊 Visualización tabular de los horarios generados

---

## 🧠 Algoritmo Utilizado

El núcleo del sistema utiliza **backtracking recursivo**, que:

1. Ordena materias por cantidad de créditos  
2. Explora combinaciones posibles de secciones  
3. Verifica conflictos de horario  
4. Retrocede cuando encuentra incompatibilidades  
5. Guarda únicamente horarios válidos  

Este enfoque garantiza encontrar **todas las combinaciones sin solapamientos**.

---

## 🏗️ Arquitectura del Proyecto

main.py → Punto de entrada
interfaz_gui.py → Interfaz gráfica (Tkinter)
funciones.py → Lógica del algoritmo y procesamiento
PESUM.txt → Datos del pensum académico


---

## 🧪 Tecnologías Utilizadas

- Python 3  
- Tkinter  
- Algoritmo Backtracking  
- Estructuras de datos (listas, diccionarios)  
- Programación modular  

---

## 🚀 Cómo Ejecutar el Proyecto

### 1️⃣ Requisitos

- Python 3 instalado  
- VS Code o cualquier IDE  

---

### 2️⃣ Clonar repositorio

```bash
git clone https://github.com/TU-USUARIO/generador-horarios-backtracking.git
cd generador-horarios-backtracking
3️⃣ Ejecutar el programa
python main.py
🧭 Uso del Sistema
Seleccionar trimestre

Presionar Mostrar Materias

Configurar secciones por materia

Guardar secciones

Presionar Generar Horarios Posibles

Exportar horarios válidos si se desea

🎯 Aprendizajes Clave
Implementación práctica de backtracking

Detección de conflictos de intervalos

Diseño de GUI con Tkinter

Manejo de estructuras de datos complejas

Programación modular en Python

Resolución de problemas combinatorios

🔮 Mejoras Futuras
Versión web del generador

Optimización heurística del backtracking

Exportación a Excel

Filtros por horario preferido

Visualización tipo calendario

👤 Autor
Angel E. Concepción Capellán
Proyecto académico – INTEC
