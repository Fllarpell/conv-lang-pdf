import os
import pandas as pd

DATA_DIR = "/app/data/"
TEMP_FILES = ["temp.csv", "temp_data.json"]
RAW_DATA = "rus.txt"


def prepare_data():
    data = {
        "source_data": [],
        "target_data": [],
    }

    with open(RAW_DATA, 'r') as f:
        for line in f.readlines():
            data["source_data"].append(line.split("\t")[0])
            data["target_data"].append(line.split("\t")[1])

    df = pd.DataFrame(data)

    df.to_csv("training_data.csv", index=False)
    print("CSV-файл успешно создан и сохранен.")

    #
    #
    # for temp_file in TEMP_FILES:
    #     file_path = os.path.join(DATA_DIR, temp_file)
    #     if os.path.exists(file_path):
    #         os.remove(file_path)
    #         print(f"Удален временный файл: {file_path}")


if __name__ == "__main__":
    prepare_data()
