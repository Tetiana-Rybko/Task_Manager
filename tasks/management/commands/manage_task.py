import json
from datetime import datetime, timedelta

tasks = [
    {
        "title": "Prepare presentation",
        "status": "New",
        "deadline": "2025-04-20",
        "description": "",
        "subtasks": [
            {
                "title": "Gather information",
                "status": "Done",
                "deadline": "2025-04-12"
            },
            {
                "title": "Create slides",
                "status": "In progress",
                "deadline": "2025-04-15",
                "description": ""
            }
        ]
    },
    {
        "title": "Write report",
        "status": "New",
        "deadline": "2025-04-25",
        "subtasks": []
    }
]

print("Задачи со статусом 'New':")
for task in tasks:
    if task["status"] == "New":
        print("-", task["title"])

print("\nПодзадачи со статусом 'Done', но с просроченным сроком:")
today = datetime.today().date()
for task in tasks:
    for subtask in task.get("subtasks", []):
        due_date = datetime.strptime(subtask["deadline"], "%Y-%m-%d").date()
        if subtask["status"] == "Done" and due_date < today:
            print("-", subtask["title"])


for task in tasks:
    if task["title"] == "Prepare presentation":
        task["status"] = "In progress"
        for subtask in task["subtasks"]:
            if subtask["title"] == "Gather information":
                subtask["deadline"] = (today - timedelta(days=2)).strftime("%Y-%m-%d")
            elif subtask["title"] == "Create slides":
                subtask["description"] = "Create and format presentation slides"

tasks = [task for task in tasks if task["title"] != "Prepare presentation"]

with open("final_tasks.json", "w", encoding="utf-8") as f:
    json.dump(tasks, f, indent=4, ensure_ascii=False)

print("\nИтоговый список задач сохранён в 'final_tasks.json'.")