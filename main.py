#configuración de la ventana principal y la interacción del usuario con la lista de tareas.
#GESTIONA Y MUESTRA LAS TAREAS OBTENIDAS DE TASK_DIALOG
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox #submodulos simpledialog: inputs, messsagebok: msj informativos
from dialogs.task_dialog import TaskDialog
import csv
import datetime   #fechas y horas
import threading

task_list = None #se inicializa vacio
tasks = {}   #se iniciliza un dicc 


def main():   #se encarga de ejecutar la aplicacion principal
    global tree, status_vars, search_var, search_by_name, search_by_description  #globales para poder acceder fuera de la funcion
    
    #ventana principal (raiz):
    root = tk.Tk()    
    root.title("Gestor de Tareas")
    root.geometry("800x600")
    main_frame = ttk.Frame(root)  #se crea el contenedor para acomodar los elementos (frame)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)
    
    #Filtrar tareas por estado
    status_vars = {
        "Nueva": tk.BooleanVar(value=True),   #cuando se crean todas inicializan en true para que salgan cuando se filtre
        "En progreso": tk.BooleanVar(value=True),
        "Finalizada": tk.BooleanVar(value=True)
    }
    for idx, (status, var) in enumerate(status_vars.items()):   #itera: idx es el indice que comienza en 0. Enumerate obtiene inidice y valor booleando
        chk = ttk.Checkbutton(main_frame, text=status, variable=var, command=update_treeview) #crea checkbox para filtrar tareas segun estado
        chk.grid(row=idx+2, column=0, sticky="w", pady=2)


    #Busqueda:
    search_frame = ttk.Frame(main_frame)
    search_frame.grid(row=5, column=0, sticky="ew", pady=5)
    
    search_label = ttk.Label(search_frame, text="Buscar:") 
    search_label.grid(row=0, column=0, sticky=tk.E)
    
    search_var = tk.StringVar() #crea una varibale de tipo StringVar para almacenar el texto que el usuario ingresara
    search_entry = ttk.Entry(search_frame, textvariable=search_var) #el texto ingresado lo compara con las tareas almacenadas
    search_entry.grid(row=0, column=1, sticky="ew", padx=10)
    
    search_button = ttk.Button(search_frame, text="Buscar tareas", command=search_tasks, width=20)
    search_button.grid(row=0, column=2, padx=10)
    
    search_by_name = tk.BooleanVar(value=True)  #se crea variable booleana inicializada en True
    search_by_description = tk.BooleanVar(value=False) #se crea variable booleana inicializada en #False (desactivado al principio)
    
    chk_search_by_name = ttk.Checkbutton(search_frame, text="Buscar por nombre", variable=search_by_name)
    chk_search_by_name.grid(row=1, column=0, sticky=tk.W, padx=10)
    
    chk_search_by_description = ttk.Checkbutton(search_frame, text="Buscar por descripción", variable=search_by_description)
    chk_search_by_description.grid(row=1, column=1, sticky=tk.W, padx=10)
    
    reset_search_button = ttk.Button(search_frame, text="Limpiar", command=reset_search, width=20)    #reiniciar busqueda
    reset_search_button.grid(row=1, column=2, padx=10, pady=10)
    
    search_frame.grid_columnconfigure(1, weight=1)   #la ventana se adpata automaticamente
    
    
    #Lista de tareas
    task_frame = ttk.Frame(main_frame) #crea un marco denro del contenedor princial
    task_frame.grid(row=0, column=0, sticky="nsew")   #nsew el marco se estira en todas las direcciones
    tree = ttk.Treeview(task_frame, columns=('Priority', 'Task'), show='headings')  #creacion de columnas
    tree.bind("<Double-1>", display_task_details)  #cuando hacemos doble click se abre una ventana con los detalles
    tree.heading('Priority', text='Prioridad')
    tree.column('Priority', width=100, stretch=tk.NO)
    tree.heading('Task', text='Tarea')
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) #pack: adiministrador de geometria
    scrollbar = ttk.Scrollbar(task_frame, command=tree.yview) #crea bara de desplazamiento vertical
    tree.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    #Conf de colores de fondo
    tree.tag_configure("Alta", background="#FFCCCC")  #rojo
    tree.tag_configure("Media", background="#FFFFCC") #amarillo 
    tree.tag_configure("Baja", background="#CCFFCC")  #verde 
    
    #Contenedor para botones de prioridad
    buttons_frame = ttk.Frame(main_frame)
    buttons_frame.grid(row=1, column=0, pady=10, sticky="ew")
    
    #Boton Añadir tarea
    add_task_button = ttk.Button(buttons_frame, text="Añadir tarea", command=lambda:add_task(root))
    add_task_button.pack(side=tk.LEFT, padx=20)
    #Boton Editar Tarea
    edit_task_button = ttk.Button(buttons_frame, text="Editar tarea", command=lambda:edit_task(root))
    edit_task_button.pack(side=tk.LEFT, padx=20)
    #Boton eliminar tarea
    delete_task_button = ttk.Button(buttons_frame, text="Eliminar tarea", command=delete_task)
    delete_task_button.pack(side=tk.LEFT, padx=20)
    
    update_treeview()  #actualizan tareas
    show_notifications() #muestra si hay tareas por vencer
    #threading.Thread(target=check_alarms, args=(tasks,), daemon=True).start()
    
    #Main loop:
    root.mainloop()   #bucle que espera si se ejecuta alguno de los eventos anteriores, finaliza cuando se cierra la apliacion

#agregar nueva tarea
def add_task(parent):  #parent representa la ventana principal
    dialog = TaskDialog(parent, "Crear nueva tarea") #ventana para crear nueva tarea
    if dialog.result:  #cuando el usuario confirma la accion
        task_name, task_status, task_priority, task_description, task_creation_date, task_due_date, task_completion_date, alarm_date, alarm_hour = dialog.result #muestra en pantalla estos campos
        if task_name:
            if task_name in tasks:  #verifica que la tarea no este duplicada, en caso de estar duplicada se aplica return
                messagebox.showinfo("Error", "Ya existe una tarea con ese nombre")
                return
            tree.insert("", "end", text=f'{task_priority} - {task_name}', values=(task_priority, task_name), tags=(task_priority,)) #si no hay errores se agrega al treeview (tabla)
            tasks[task_name] = {  #agrega tarea al diccionario
                "status": task_status,
                "priority": task_priority,
                "description": task_description,
                "creation_date": task_creation_date,
                "due_date": task_due_date,
                "completion_date": task_completion_date,
                "alarm_date": alarm_date,
                "alarm_hour": alarm_hour
            }
        else:
            messagebox.showinfo("Error", "El nombre de la tarea no puede estar vacío")
    update_treeview()  #actualiza vista
    save_tasks_to_csv()  #almacena en db

#editar tarea
def edit_task(parent): #parent: ventana principal
    try:
        selected_task = tree.selection()   #asegurarnos de que se selecciono una tarea
        if not selected_task:
            messagebox.showinfo("Error", "No hay ninguna tarea seleccionada!")
            return
        
        task_priority, task_name = tree.item(selected_task, "values")   #desempaqueta todos los campos
        task_data = tasks[task_name]
        task_status = task_data['status']
        task_description = task_data['description']
        task_creation_date = task_data['creation_date']
        task_due_date = task_data['due_date']
        task_completion_date = task_data['completion_date']
        task_alarm_date = task_data.get('alarm_date', '')  # .get permite un valor predeterminado si la clave no existe.
        task_alarm_hour = task_data.get('alarm_hour', '')
        #crea un instancia para editar los datos
        dialog = TaskDialog(parent, "Editar tarea", task_name, task_status, task_priority, task_description, task_creation_date, task_due_date, task_completion_date, task_alarm_date, task_alarm_hour)
        
        if dialog.result:
            updated_task_name, updated_task_status, updated_task_priority, updated_task_description, updated_task_creation_date, updated_task_due_date, updated_task_completion_date, updated_alarm_date, updated_alarm_hour = dialog.result
            if updated_task_name != task_name and updated_task_name in tasks:
                messagebox.showerror("Error", "Ya existe una tarea con ese nombre!")
                return
            if updated_task_name != task_name:
                del tasks[task_name]
            tasks[updated_task_name] = {   #se alamcenan los datos
                'status': updated_task_status,
                'priority': updated_task_priority,
                'description': updated_task_description,
                'creation_date': updated_task_creation_date,
                'due_date': updated_task_due_date,
                'completion_date': updated_task_completion_date,
                'alarm_date': updated_alarm_date,
                'alarm_hour': updated_alarm_hour
            }
            
            tree.delete(selected_task)  #elimina tarea antgua
            tree.insert("", "end", values=(updated_task_priority, updated_task_name), tags=(updated_task_priority,)) 
        update_treeview()
        save_tasks_to_csv()
    except KeyError:  #manejo de excepciones
        messagebox.showerror("Error", "La tarea seleccionada no fue encontrada!")
        
#eliminar tarea
def delete_task():
    try:
        selected_task = tree.selection()
        if not selected_task:
            messagebox.showinfo("Error", "No hay ninguna tarea seleccionada!")
            return
        task_priority, task_name = tree.item(selected_task, "values")
        confirm = messagebox.askyesno("Confirmar", f"¿Estás seguro de que vas a eliminar la tarea '{task_name}'?")
        if confirm:
            del tasks[task_name]
            tree.delete(selected_task)
    except KeyError:
        messagebox.showerror("Error", "La tarea seleccionada no fue encontrada!")
    update_treeview()
    save_tasks_to_csv()

# evento para cuando se haga click en un a tarea y asi ver sus detalles
def display_task_details(event):
        item = tree.selection()[0]
        task_name = tree.item(item, "values")[1]
        if task_name in tasks:
            details_window = tk.Toplevel()
            details_window.title(f"Detalles de la tarea '{task_name}'")
            ttk.Label(details_window, text=f"Nombre: {task_name}").pack(pady=10)
            ttk.Label(details_window, text=f"Estado: {tasks[task_name]['status']}").pack(pady=10)
            ttk.Label(details_window, text=f"Prioridad: {tasks[task_name]['priority']}").pack(pady=10)
            ttk.Label(details_window, text=f"Descripción: {tasks[task_name]['description']}").pack(pady=10)
            ttk.Label(details_window, text=f"Fecha de creación: {tasks[task_name]['creation_date']}").pack(pady=10)
            ttk.Label(details_window, text=f"Fecha límite: {tasks[task_name]['due_date']}").pack(pady=10)
            ttk.Label(details_window, text=f"Fecha de finalización: {tasks[task_name]['completion_date']}").pack(pady=10)

# se asegura de econtrar las tareas segun su estado
def update_treeview():
    tree.delete(*tree.get_children()) #elimina los elementos actuales
    active_statuses = [status for status, var in status_vars.items() if var.get()]
    for task_name, task_data in tasks.items():
        if task_data["status"] in active_statuses:  # Esta línea verifica que el estado de la tarea esté en los estados activos
            tree.insert("", "end", text=f'{task_data["priority"]} - {task_name}', values=(task_data["priority"], task_name), tags=(task_data["priority"], task_name))

#buscar tareas
def search_tasks():
    search_term = search_var.get().lower()  #la busqueda se pasa a minusculas para que no sea sensible a mayusculas
    tree.delete(*tree.get_children()) #elimina las del  arvbol
    
    for task_name, task_data in tasks.items():   #buclea para encontrar coincidencia
        if not status_vars[task_data["status"]].get():
            continue
                
        match_name = search_by_name.get() and search_term in task_name.lower()
        match_description = search_by_description.get() and search_term in task_data["description"].lower()
        if match_name or match_description:
            tree.insert("", "end", text=f'{task_data["priority"]} - {task_name}', values=(task_data["priority"], task_name), tags=(task_data["priority"], task_name)) #si coincide se agrega

#reiniciar busqueda
def reset_search():
    search_var.set("")
    search_by_name.set(True)
    search_by_description.set(False)
    update_treeview()

#guardar tarea en db
def save_tasks_to_csv():
    with open('tasks.csv', 'w', newline='') as csvfile:  #w: modo de escritura, newlune, evitar lineas en blanco adicionales
        fieldnames = ['task_name', 'status', 'priority', 'description', 'creation_date', 'due_date', 'completion_date', 'alarm_date', 'alarm_hour']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)  #permite escribir campos en las campos definidiso anterioirmente
        
        writer.writeheader()  #metodo para escribir las filas 
        for task_name, task_data in tasks.items():
            task_data['task_name'] = task_name
            writer.writerow(task_data)  #escribe el nombre tarea 

#cargar tareas y devolverlas como un diccionario
def load_tasks_from_csv(filename="tasks.csv"):  #argumento predeterminado
    tasks = {}  #inicializa el diccionario
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:   # r: modo lectura utf-8: lee correctamente caracteres especiales
            reader = csv.DictReader(file)  #lector de diccioarios
            for row in reader:  #bucle para encontrar tarea
                task_name = row["task_name"]
                tasks[task_name] = {
                    'status': row['status'],
                    'priority': row['priority'],
                    'description': row['description'],
                    'creation_date': row['creation_date'],
                    'due_date': row['due_date'],
                    'completion_date': row['completion_date'],
                    'alarm_date': row['alarm_date'],
                    'alarm_hour': row['alarm_hour']
                }
    except FileNotFoundError:
        # If the file doesn't exist, just return an empty dictionary.
        pass
    return tasks

#obtener tareas proximas a vencer
def get_tasks_near_deadline():
    near_deadline_tasks = [] #inicializa lista
    today = datetime.datetime.now().date()  #obtener fecha hoy
    tomorrow = today + datetime.timedelta(days=1) #obtener fecha mañana
    for task_name, task_data in tasks.items():  #bucle para ver si se cumple la condicion
        if not task_data["due_date"]:
            continue
        due_date = datetime.datetime.strptime(task_data["due_date"], "%d/%m/%Y").date()
        if today <= due_date <= tomorrow:
            near_deadline_tasks.append(task_name)
    return near_deadline_tasks

#muestra si hay tareas a putnos de vencer
def show_notifications():
    tasks_to_notify = get_tasks_near_deadline()
    if tasks_to_notify:
        tasks_str = "\n".join(tasks_to_notify)    #una tarea por cada linea
        messagebox.showwarning("Atención", f"Las siguientes tareas se vencen hoy o mañana:\n{tasks_str}")


if __name__ == "__main__":   #solo se ejecute el modulo principal
    tasks = load_tasks_from_csv()  #crga tarea desde db
    main()   #inicio ventana principal
    