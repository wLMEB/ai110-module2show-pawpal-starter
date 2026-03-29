from enum import Enum


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class HealthInfo:
    """Stores and manages a pet's health details."""

    _EDITABLE = {"weight", "dietary_notes", "vaccinations", "medications"}

    def __init__(self, weight, dietary_notes, vaccinations, medications):
        """Initialize health info with weight, diet notes, vaccinations, and medications."""
        self._weight = weight
        self._dietary_notes = dietary_notes
        self._vaccinations = vaccinations
        self._medications = medications

    def edit_health(self, attribute, value):
        """Update a health attribute by name; raises ValueError for unknown fields."""
        if attribute not in self._EDITABLE:
            raise ValueError(f"'{attribute}' is not an editable health field")
        setattr(self, f"_{attribute}", value)

    def get_weight(self):
        """Return the pet's weight."""
        return self._weight

    def get_dietary_notes(self):
        """Return dietary notes for the pet."""
        return self._dietary_notes

    def get_vaccinations(self):
        """Return the pet's vaccination records."""
        return self._vaccinations

    def get_medications(self):
        """Return current medications for the pet."""
        return self._medications


class Task:
    """Represents a single care activity assigned to a pet."""

    _EDITABLE = {"description", "scheduled_time", "frequency", "duration_minutes", "priority", "owner"}

    def __init__(self, description, pet, scheduled_time, duration_minutes,
                 priority, frequency="once", owner=None):
        """Initialize a task with description, pet, time, duration, priority, and optional frequency."""
        self._description = description
        self._pet = pet
        self._scheduled_time = scheduled_time
        self._duration_minutes = duration_minutes
        self._priority = Priority(priority) if isinstance(priority, str) else priority
        self._frequency = frequency  # e.g. "once", "daily", "weekly"
        self._completed = False
        self._owner = owner

    def mark_complete(self):
        """Mark this task as completed."""
        self._completed = True

    def is_complete(self):
        """Return True if the task has been completed."""
        return self._completed

    def edit_task(self, attribute, value):
        """Update a task attribute by name; raises ValueError for unknown fields."""
        if attribute not in self._EDITABLE:
            raise ValueError(f"'{attribute}' is not an editable task field")
        if attribute == "priority" and isinstance(value, str):
            value = Priority(value)
        setattr(self, f"_{attribute}", value)

    def get_description(self):
        """Return the task description."""
        return self._description

    def get_pet(self):
        """Return the pet this task is assigned to."""
        return self._pet

    def get_scheduled_time(self):
        """Return the scheduled datetime for this task."""
        return self._scheduled_time

    def get_duration(self):
        """Return the task duration in minutes."""
        return self._duration_minutes

    def get_priority(self):
        """Return the task priority as a Priority enum value."""
        return self._priority

    def get_frequency(self):
        """Return how often this task recurs (e.g. 'once', 'daily', 'weekly')."""
        return self._frequency

    def get_owner(self):
        """Return the owner responsible for this task."""
        return self._owner

    def __str__(self):
        """Return a human-readable summary of the task."""
        status = "[x]" if self._completed else "[ ]"
        time_str = self._scheduled_time.strftime("%I:%M %p")
        return (f"{status} {time_str} | {self._description} "
                f"({self._pet.get_name()}, {self._duration_minutes} min, "
                f"{self._priority.value} priority)")


class Pet:
    """Stores pet details and its associated care tasks."""

    _EDITABLE = {"name", "breed", "age", "species", "health"}

    def __init__(self, name, breed, age, species, health=None):
        """Initialize a pet with name, breed, age, species, and optional health info."""
        self._name = name
        self._breed = breed
        self._age = age
        self._species = species
        self._health = health
        self._tasks = []
        self._owner = None  # set by Owner.add_pet

    def add_task(self, task):
        """Add a care task to this pet's task list."""
        self._tasks.append(task)

    def get_tasks(self):
        """Return all tasks assigned to this pet."""
        return list(self._tasks)

    def edit_pet(self, attribute, value):
        """Update a pet attribute by name; raises ValueError for unknown fields."""
        if attribute not in self._EDITABLE:
            raise ValueError(f"'{attribute}' is not an editable pet field")
        setattr(self, f"_{attribute}", value)

    def get_name(self):
        """Return the pet's name."""
        return self._name

    def get_breed(self):
        """Return the pet's breed."""
        return self._breed

    def get_age(self):
        """Return the pet's age."""
        return self._age

    def get_species(self):
        """Return the pet's species."""
        return self._species

    def get_health(self):
        """Return the pet's HealthInfo object."""
        return self._health

    def get_owner(self):
        """Return the owner this pet belongs to."""
        return self._owner


class Owner:
    """Manages multiple pets and provides access to all their tasks."""

    def __init__(self, name):
        """Initialize an owner with a name."""
        self._name = name
        self._pets = []

    def add_pet(self, pet):
        """Register a pet under this owner; raises ValueError if already registered."""
        if pet in self._pets:
            raise ValueError(f"{pet.get_name()} is already registered to this owner")
        pet._owner = self
        self._pets.append(pet)

    def get_all_tasks(self):
        """Return a flat list of all tasks across every pet owned."""
        tasks = []
        for pet in self._pets:
            tasks.extend(pet.get_tasks())
        return tasks

    def get_name(self):
        """Return the owner's name."""
        return self._name

    def get_pets(self):
        """Return the list of pets owned."""
        return list(self._pets)


class Scheduler:
    """The brain of PawPal — retrieves, organizes, and manages tasks across all pets."""

    def __init__(self):
        """Initialize the scheduler with an empty task registry."""
        self._tasks = []

    def register_owner(self, owner):
        """Pull in all existing tasks from an owner's pets into the scheduler."""
        for task in owner.get_all_tasks():
            if task not in self._tasks:
                self._tasks.append(task)

    def add_task(self, task):
        """Add a task to the scheduler and attach it to the pet's task list."""
        task.get_pet().add_task(task)
        self._tasks.append(task)

    def remove_task(self, task):
        """Remove a task from the scheduler; raises ValueError if not found."""
        if task not in self._tasks:
            raise ValueError("Task not found in scheduler")
        self._tasks.remove(task)

    def get_all_tasks(self):
        """Return all tasks tracked by the scheduler."""
        return list(self._tasks)

    def get_tasks_by_pet(self, pet):
        """Return all tasks assigned to a specific pet."""
        return [t for t in self._tasks if t.get_pet() is pet]

    def get_tasks_by_owner(self, owner):
        """Return all tasks belonging to any pet of a given owner."""
        owner_pets = set(owner.get_pets())
        return [t for t in self._tasks if t.get_pet() in owner_pets]

    def get_tasks_by_priority(self, priority):
        """Return tasks matching a given priority (string or Priority enum)."""
        p = Priority(priority) if isinstance(priority, str) else priority
        return [t for t in self._tasks if t.get_priority() == p]

    def get_tasks_sorted_by_time(self):
        """Return all tasks sorted by scheduled time ascending."""
        return sorted(self._tasks, key=lambda t: t.get_scheduled_time())

    def get_tasks_sorted_by_priority(self):
        """Return all tasks sorted from HIGH to LOW priority."""
        order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        return sorted(self._tasks, key=lambda t: order[t.get_priority()])

    def get_upcoming_tasks(self, from_time, to_time):
        """Return tasks scheduled within the given datetime window."""
        return [
            t for t in self._tasks
            if from_time <= t.get_scheduled_time() <= to_time
        ]

    def print_schedule(self, date=None):
        """Print a formatted daily schedule, optionally filtered to a specific date."""
        tasks = self.get_tasks_sorted_by_time()
        if date:
            tasks = [t for t in tasks if t.get_scheduled_time().date() == date]

        label = date.strftime("%A, %B %d %Y") if date else "All Tasks"
        print(f"\n{'=' * 45}")
        print(f"  PawPal Schedule — {label}")
        print(f"{'=' * 45}")
        if not tasks:
            print("  No tasks scheduled.")
        for task in tasks:
            print(f"  {task}")
        print(f"{'=' * 45}\n")
