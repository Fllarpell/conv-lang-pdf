import subprocess

def run_migrations():
    print("Выполняем миграции базы данных...")
    subprocess.run(["python", "manage.py", "migrate"], check=True)

def collect_static():
    print("Собираем статические файлы...")
    subprocess.run(["python", "manage.py", "collectstatic", "--noinput"], check=True)

if __name__ == "__main__":
    run_migrations()
    collect_static()
