import csv
import os
import datetime
from main import save_tasks_to_csv, tasks  # Importa la función y el diccionario de tareas desde main

def test_save_tasks_to_csv():
    # Configurar datos de prueba
    tasks.clear()  # Limpiamos las tareas para el test
    today = datetime.datetime.now().date()
    tomorrow = today + datetime.timedelta(days=1)

    tasks['Tarea 1'] = {
        'status': 'Nueva',
        'priority': 'Alta',
        'description': 'Descripción de tarea 1',
        'creation_date': today.strftime("%d/%m/%Y"),
        'due_date': today.strftime("%d/%m/%Y"),
        'completion_date': '',
        'alarm_date': '',
        'alarm_hour': ''
    }

    tasks['Tarea 2'] = {
        'status': 'En progreso',
        'priority': 'Media',
        'description': 'Descripción de tarea 2',
        'creation_date': today.strftime("%d/%m/%Y"),
        'due_date': tomorrow.strftime("%d/%m/%Y"),
        'completion_date': '',
        'alarm_date': '',
        'alarm_hour': ''
    }

    # Guardar las tareas en el archivo CSV
    print("Guardando tareas en el archivo CSV...")
    save_tasks_to_csv()

    # Verificamos que el archivo CSV se haya creado
    if os.path.exists('tasks.csv'):
        print("Archivo CSV creado exitosamente.")
    else:
        print("Error: El archivo CSV no fue creado.")

    # Leemos el archivo CSV y verificamos su contenido
    with open('tasks.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        tasks_from_csv = list(reader)

    # Verificamos que el número de tareas guardadas coincida con las tareas que agregamos
    print(f"Número de tareas guardadas: {len(tasks_from_csv)}")
    print(f"Número de tareas agregadas: {len(tasks)}")
    assert len(tasks_from_csv) == len(tasks), "El número de tareas guardadas no coincide."

    # Verificamos que las tareas en el archivo CSV coincidan con las que agregamos
    for task_name, task_data in tasks.items():
        print(f"Verificando tarea: {task_name}")
        task_in_csv = next((task for task in tasks_from_csv if task['task_name'] == task_name), None)
        assert task_in_csv is not None, f"La tarea '{task_name}' no se encontró en el archivo CSV."
        print(f"Tarea '{task_name}' encontrada en el archivo CSV. Verificando campos...")
        for field, value in task_data.items():
            if field != 'task_name':  # No necesitamos verificar 'task_name' ya que está en la cabecera
                assert task_in_csv[field] == value, f"El valor del campo '{field}' para la tarea '{task_name}' es incorrecto."
                print(f"El campo '{field}' es correcto para la tarea '{task_name}'.")

    print("Prueba completada con éxito.")

# Ejecutamos la prueba
test_save_tasks_to_csv()
