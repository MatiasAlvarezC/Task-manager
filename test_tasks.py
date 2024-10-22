import datetime
from main import get_tasks_near_deadline, tasks

def test_get_tasks_near_deadline():
    # Configurar datos de prueba
    tasks.clear()  # Limpiamos las tareas para el test
    today = datetime.datetime.now().date()
    tomorrow = today + datetime.timedelta(days=1)

    print(f"Fecha actual: {today}")
    print(f"Fecha de mañana: {tomorrow}")

    tasks['Tarea 1'] = {
        'due_date': today.strftime("%d/%m/%Y"),
        'status': 'Nueva',
        'priority': 'Alta',
        'description': 'Descripción de tarea 1'
    }
    print(f"Tarea 1 añadida: {tasks['Tarea 1']}")

    tasks['Tarea 2'] = {
        'due_date': tomorrow.strftime("%d/%m/%Y"),
        'status': 'En progreso',
        'priority': 'Media',
        'description': 'Descripción de tarea 2'
    }
    print(f"Tarea 2 añadida: {tasks['Tarea 2']}")

    tasks['Tarea 3'] = {
        'due_date': (today + datetime.timedelta(days=3)).strftime("%d/%m/%Y"),
        'status': 'Finalizada',
        'priority': 'Baja',
        'description': 'Descripción de tarea 3'
    }
    print(f"Tarea 3 añadida: {tasks['Tarea 3']}")

    # Llamar a la función
    near_deadline_tasks = get_tasks_near_deadline()

    print(f"Tareas cercanas a la fecha de vencimiento: {near_deadline_tasks}")

    # Comprobar que las tareas que vencen hoy o mañana están en la lista
    assert 'Tarea 1' in near_deadline_tasks, f"Tarea 1 no encontrada en {near_deadline_tasks}"
    assert 'Tarea 2' in near_deadline_tasks, f"Tarea 2 no encontrada en {near_deadline_tasks}"
    assert 'Tarea 3' not in near_deadline_tasks, f"Tarea 3 encontrada en {near_deadline_tasks}"

    print("Prueba completada con éxito")
