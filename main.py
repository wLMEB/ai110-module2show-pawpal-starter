from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler, HealthInfo, Priority

# --- Setup ---
owner = Owner("Alex")

luna = Pet("Luna", "Golden Retriever", 3, "Dog",
           health=HealthInfo(28.5, "grain-free diet", "rabies, DHPP", "none"))

mochi = Pet("Mochi", "Siamese", 5, "Cat",
            health=HealthInfo(4.2, "wet food only", "FVRCP", "allergy drops"))

owner.add_pet(luna)
owner.add_pet(mochi)

# --- Tasks ---
today = datetime.today()

def at(hour, minute=0):
    return today.replace(hour=hour, minute=minute, second=0, microsecond=0)

scheduler = Scheduler()

scheduler.add_task(Task("Morning walk",        luna,  at(7),     30, Priority.HIGH,   "daily"))
scheduler.add_task(Task("Flea medication",     luna,  at(9),     5,  Priority.HIGH,   "weekly"))
scheduler.add_task(Task("Breakfast feeding",   mochi, at(8),     10, Priority.MEDIUM, "daily"))
scheduler.add_task(Task("Brush coat",          mochi, at(14),    15, Priority.LOW,    "weekly"))
scheduler.add_task(Task("Evening walk",        luna,  at(18, 30), 30, Priority.HIGH,  "daily"))

# --- Print schedule ---
scheduler.print_schedule(date=today.date())
