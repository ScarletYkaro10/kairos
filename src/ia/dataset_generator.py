import pandas as pd
import random
from faker import Faker

fake = Faker("pt_BR")

NUM_SAMPLES = 1000


def generate_task_data():
    data = []
    categories = [
        "Trabalho",
        "Estudo",
        "Saúde",
        "Lazer",
        "Casa",
        "Projetos",
        "Finanças",
    ]
    priorities_list = ["Baixa", "Média", "Alta"]  

    print("Gerando dados com 'Fator Humano' (Ruído)...")

    for _ in range(NUM_SAMPLES):
        days_until_due = random.randint(0, 30)
        estimated_minutes = random.randint(15, 480)
        category = random.choice(categories)
        difficulty = random.randint(1, 5)

        priority = "Baixa"

        if days_until_due <= 5:
            priority = "Alta"
        elif category in ["Saúde", "Finanças"] and difficulty >= 3:
            priority = "Alta"
        elif days_until_due <= 15 and category in ["Trabalho", "Estudo", "Projetos"]:
            priority = "Média"
        elif category in ["Casa", "Lazer"] and (
            estimated_minutes < 60 or difficulty <= 2
        ):
            priority = "Média"

        if random.random() < 0.15:
            priority = random.choice(priorities_list)

        data.append(
            {
                "days_until_due": days_until_due,
                "estimated_minutes": estimated_minutes,
                "category": category,
                "difficulty": difficulty,
                "priority_label": priority,
            }
        )

    return pd.DataFrame(data)


if __name__ == "__main__":
    df = generate_task_data()
    file_path = "src/ia/tasks_dataset.csv"
    df.to_csv(file_path, index=False)

    print(f"\nDataset com ruído gerado: {file_path}")
    print(df["priority_label"].value_counts())
