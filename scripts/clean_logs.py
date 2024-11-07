import os
import time

LOG_DIR = "/app/logs/"  # Укажите путь к каталогу с логами
MAX_LOG_AGE_DAYS = 7    # Удалять логи старше 7 дней


def clean_logs():
    current_time = time.time()
    for log_file in os.listdir(LOG_DIR):
        file_path = os.path.join(LOG_DIR, log_file)
        if os.path.isfile(file_path):
            file_age = current_time - os.path.getmtime(file_path)
            if file_age > MAX_LOG_AGE_DAYS * 86400:  # 86400 секунд = 1 день
                os.remove(file_path)
                print(f"Удален старый лог-файл: {file_path}")


if __name__ == "__main__":
    clean_logs()
