#La clase se encarga de crear una ventana emergente donde se puedan ingresar los datos
#se centra en la creación y edición de tareas a través de un diálogo
#SE U TILIZA PARA OBTENER INFORMACION DE UNA TAREA
from tkinter import simpledialog, messagebox, ttk
import tkinter as tk
from datetime import datetime
from tkcalendar import DateEntry

class TaskDialog(simpledialog.Dialog):  # la clase hereda simpledialog            constructor se lleama cuando se instancia taskDialog
    def __init__(self, parent, title, task_name="",task_status="Nueva", task_priority="Baja", task_description="", task_creation_date="", task_due_date="", task_completion_date="", alarm_date="", alarm_hour=""):
        self.default_task_name = task_name   #almacena nombre y asi sucesivamente
        self.default_task_status = task_status
        self.default_task_priority = task_priority
        self.default_task_description = task_description
        self.default_task_creation_date = task_creation_date
        self.default_task_due_date = task_due_date
        self.default_task_completion_date = task_completion_date
        self.default_alarm_date = alarm_date
        self.default_alarm_hour = alarm_hour
        super().__init__(parent, title) # llama al constructor para que tinter se inicialice correctamente, y se le pasan parent y title
    
    def body(self, parent): #se define el cuerpo del dialogo    parent(se coloca en la ventana principal)
        ttk.Label(parent, text="Tarea:").grid(column=0, row=0, sticky="w")
        ttk.Label(parent, text="Estado:").grid(column=0, row=1, sticky="w")
        ttk.Label(parent, text="Prioridad:").grid(column=0, row=2, sticky="w")
        ttk.Label(parent, text="Descripción:").grid(column=0, row=3, sticky="w")
        ttk.Label(parent, text="Fecha de creación:").grid(column=0, row=4, sticky="w")
        ttk.Label(parent, text="Fecha límite:").grid(column=0, row=5, sticky="w")
        ttk.Label(parent, text="Fecha de finalización:").grid(column=0, row=6, sticky="w")
        
        self.e1 = ttk.Entry(parent)  #campo para que usuario ingrese nombre de tarea
        self.status_options = ["Nueva", "En progreso", "Finalizada"]    #lista de opciones para estado de tarea
        self.status_combobox = ttk.Combobox(parent, values=self.status_options, state="readonly")
        self.priority_options = ["Alta", "Media", "Baja"]
        self.priority_combobox = ttk.Combobox(parent, values=self.priority_options, state="readonly")
        self.e2 = ttk.Entry(parent)
        self.e3 = ttk.Entry(parent)
        self.e4 = DateEntry(parent, date_pattern="dd/mm/Y")
        self.e4.delete(0, 'end') #Esta línea borra cualquier texto que pueda estar presente en el campo de entrada de fecha
        self.completion_date = ttk.Entry(parent)  #ventana ememrgente cuando se pone la fecha de finalizacion
        
        #ubicacion de tareas
        self.e1.grid(column=1, row=0, sticky="ew")
        self.status_combobox.grid(column=1, row=1, sticky="ew")
        self.priority_combobox.grid(column=1, row=2, sticky="ew")
        self.e2.grid(column=1, row=3, sticky="ew")
        self.e3.grid(column=1, row=4, sticky="ew")
        self.e4.grid(column=1, row=5, sticky="ew")
        self.completion_date.grid(column=1, row=6, sticky="ew")
        
        self.due_date_var = tk.BooleanVar(value=bool(self.default_task_due_date)) #se crea variable booleana para gestionar estado de casilla de verifiacaion
        self.due_date_checkbox = ttk.Checkbutton(parent, text="Establecer fecha límite", variable=self.due_date_var, command=self.toggle_due_date)
        self.due_date_checkbox.grid(column=0, row=5, sticky="w")
        
        self.e1.insert(0, self.default_task_name) #0 el texto se debe insertar al principio del campo
        self.status_combobox.set(self.default_task_status) #combobox para estado de tareas
        self.priority_combobox.set(self.default_task_priority)
        self.e2.insert(0, self.default_task_description)
        self.e3.insert(0, self.default_task_creation_date or datetime.today().strftime("%d/%m/%Y"))
        self.e4.insert(0, self.default_task_due_date or "")
        self.completion_date.insert(0, self.default_task_completion_date or "")
        
        #alarma no utilizada en esta version
        ttk.Label(parent, text="Establecer alarma:").grid(column=0, row=7, sticky="w")
        self.alarm_var = tk.BooleanVar(value=False)
        self.alarm_checkbox = ttk.Checkbutton(parent, text="Activar", variable=self.alarm_var, command=self.toggle_alarm)
        self.alarm_checkbox.grid(column=1, row=7, sticky="w")

        self.alarm_date = DateEntry(parent, date_pattern="dd/mm/Y")
        self.alarm_date.grid(column=0, row=8, sticky="w")
        self.alarm_date.grid_remove() 

        self.alarm_hour = ttk.Combobox(parent, values=[f"{i:02d}:00" for i in range(24)], state="readonly") 
        self.alarm_hour.grid(column=1, row=8, sticky="w")
        self.alarm_hour.grid_remove() 
        
        if self.default_alarm_date and self.default_alarm_hour:
            self.alarm_var.set(True)
            self.alarm_date.insert(0, self.default_alarm_date)
            self.alarm_hour.set(self.default_alarm_hour)
            self.alarm_date.grid()
            self.alarm_hour.grid()
        
        # Si la fecha de vencimiento predeterminada no está establecida, oculta el widget DateEntry
        if not self.default_task_due_date:
            self.e4.grid_remove()
            
        if self.default_task_status != "Finalizada":
            self.completion_date.grid_remove()
            
        self.status_combobox.bind("<<ComboboxSelected>>", self.update_completion_date)
        
        return self.e1
    

    def toggle_due_date(self): #toggle=palanca
        if self.due_date_var.get(): #si se marca la casilla de finalizacion
            self.e4.grid()
        else:
            self.e4.grid_remove()

    #actualiza el campo de finalizado   
    def update_completion_date(self, event=None):  #permite que el método sea llamado como respuesta a un evento
        if self.status_combobox.get() == "Finalizada":
            self.completion_date.delete(0, tk.END)
            self.completion_date.insert(0, datetime.today().strftime("%d/%m/%Y")) #strftime  formatea en el estilo "día/mes/año" 
            self.completion_date.grid()
        else:
            self.completion_date.delete(0, tk.END)
            self.completion_date.grid_remove()
    #recopilar datos ingresados
    def apply(self):
        task_name = self.e1.get()
        task_status = self.status_combobox.get()
        task_priority = self.priority_combobox.get()
        task_description = self.e2.get()
        task_creation_date = self.e3.get()
        task_due_date = self.e4.get() if self.due_date_var.get() else None   # los que contienen None son los campos opcionales
        task_completion_date = self.completion_date.get() or None
        alarm_date = self.alarm_date.get() if self.alarm_var.get() else None
        alarm_hour = self.alarm_hour.get() if self.alarm_var.get() else None

        # tupla que contiene todos los datos recopilados en apply
        self.result = (task_name, task_status, task_priority, task_description, task_creation_date, task_due_date, task_completion_date, alarm_date, alarm_hour)


    #no disponible en esta version
    def toggle_alarm(self):
        if self.alarm_var.get():
            self.alarm_date.grid()
            self.alarm_hour.grid()
        else:
            self.alarm_date.grid_remove()
            self.alarm_hour.grid_remove()