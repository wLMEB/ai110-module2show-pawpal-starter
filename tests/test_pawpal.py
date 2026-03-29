from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler, Priority


def make_task(description="Feed", priority=Priority.LOW):
    pet = Pet("Buddy", "Labrador", 2, "Dog")
    return Task(description, pet, datetime(2026, 3, 28, 9, 0), 10, priority)


def test_mark_complete_changes_status():
    task = make_task("Bath time")
    assert task.is_complete() is False
    task.mark_complete()
    assert task.is_complete() is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Nala", "Persian", 4, "Cat")
    scheduler = Scheduler()
    assert len(pet.get_tasks()) == 0

    task = Task("Vet checkup", pet, datetime(2026, 3, 28, 11, 0), 20, Priority.HIGH)
    scheduler.add_task(task)

    assert len(pet.get_tasks()) == 1
