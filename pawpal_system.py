from enum import Enum


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class HealthInfo:
    _EDITABLE = {"weight", "dietary_notes", "vaccinations", "medications"}

    def __init__(self, weight, dietary_notes, vaccinations, medications):
        self._weight = weight
        self._dietary_notes = dietary_notes
        self._vaccinations = vaccinations
        self._medications = medications

    def edit_health(self, attribute, value):
        if attribute not in self._EDITABLE:
            raise ValueError(f"'{attribute}' is not an editable health field")
        setattr(self, f"_{attribute}", value)

    def get_weight(self):
        return self._weight

    def get_dietary_notes(self):
        return self._dietary_notes

    def get_vaccinations(self):
        return self._vaccinations

    def get_medications(self):
        return self._medications


class Pet:
    _EDITABLE = {"name", "breed", "age", "species", "health"}

    def __init__(self, name, breed, age, species, health=None):
        self._name = name
        self._breed = breed
        self._age = age
        self._species = species
        self._health = health
        self._owner = None  # set by Owner.add_pet

    def edit_pet(self, attribute, value):
        if attribute not in self._EDITABLE:
            raise ValueError(f"'{attribute}' is not an editable pet field")
        setattr(self, f"_{attribute}", value)

    def get_name(self):
        return self._name

    def get_breed(self):
        return self._breed

    def get_age(self):
        return self._age

    def get_species(self):
        return self._species

    def get_health(self):
        return self._health

    def get_owner(self):
        return self._owner


class Task:
    _EDITABLE = {"task_name", "pet", "scheduled_time", "duration_minutes", "priority", "owner"}

    def __init__(self, task_name, pet, scheduled_time, duration_minutes, priority, owner=None):
        self._task_name = task_name
        self._pet = pet
        self._scheduled_time = scheduled_time
        self._duration_minutes = duration_minutes
        self._priority = Priority(priority) if isinstance(priority, str) else priority
        self._owner = owner

    def edit_task(self, attribute, value):
        if attribute not in self._EDITABLE:
            raise ValueError(f"'{attribute}' is not an editable task field")
        if attribute == "priority" and isinstance(value, str):
            value = Priority(value)
        setattr(self, f"_{attribute}", value)

    def get_task_name(self):
        return self._task_name

    def get_pet(self):
        return self._pet

    def get_scheduled_time(self):
        return self._scheduled_time

    def get_duration(self):
        return self._duration_minutes

    def get_priority(self):
        return self._priority

    def get_owner(self):
        return self._owner


class Owner:
    def __init__(self, name):
        self._name = name
        self._pets = []
        self._tasks = []

    def add_pet(self, pet):
        if pet in self._pets:
            raise ValueError(f"{pet.get_name()} is already registered to this owner")
        pet._owner = self
        self._pets.append(pet)

    def add_task(self, task):
        task._owner = self
        self._tasks.append(task)

    def get_name(self):
        return self._name

    def get_pets(self):
        return self._pets

    def get_tasks(self):
        return self._tasks


class Scheduler:
    def __init__(self):
        self._tasks = []

    def add_task(self, task):
        self._tasks.append(task)

    def remove_task(self, task):
        if task not in self._tasks:
            raise ValueError("Task not found in scheduler")
        self._tasks.remove(task)

    def get_all_tasks(self):
        return list(self._tasks)

    def get_tasks_by_pet(self, pet):
        return [t for t in self._tasks if t.get_pet() is pet]

    def get_tasks_by_owner(self, owner):
        return [t for t in self._tasks if t.get_owner() is owner]

    def get_tasks_by_priority(self, priority):
        p = Priority(priority) if isinstance(priority, str) else priority
        return [t for t in self._tasks if t.get_priority() == p]

    def get_tasks_sorted_by_time(self):
        return sorted(self._tasks, key=lambda t: t.get_scheduled_time())

    def get_tasks_sorted_by_priority(self):
        order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        return sorted(self._tasks, key=lambda t: order[t.get_priority()])

    def get_upcoming_tasks(self, from_time, to_time):
        return [
            t for t in self._tasks
            if from_time <= t.get_scheduled_time() <= to_time
        ]
