import requests
import psutil
import socket
import subprocess
import mysql.connector


class HealthCheckerService:
    def __init__(self, hostname: str = None,
                 test_file_path: str = None,
                 logs_file_path: str = None,
                 services: list = None,
                 db_config: dict = None):
        self.hostname = hostname if hostname else "google.com"
        self.test_file_path = test_file_path if test_file_path else "text.txt"
        self.logs_file_path = logs_file_path if logs_file_path else "text.txt"
        self.services = services if services else ['httpd', 'ssh', 'mysql']
        self.db_config = db_config if db_config else {'host': 'localhost',
                                                      'user': 'root',
                                                      'password': 'admin',
                                                      'database': 'mysql'}
        

    def check_internet(self) -> str:
        output = "\n--- Проверка доступности интернета ---\n"
        output += f"Проверка {self.hostname}\n"
        try:
            result = requests.get(self.hostname)
            if result.status_code == 200:
                output += "[+] Интернет доступен"
            else:
                output += "[-] Интернет недоступен"
        except requests.RequestException:
            output += "[!] Проблемы с подключением, проверьте хост"
        return output
    
    def check_ping(self) -> str:
        output = "\n--- Проверка доступности интернета ---\n"
        try:
            result = subprocess.run(['ping', '-c', '4', self.hostname], capture_output=True)
            if result.returncode == 0:
                output += "[+] Ping прошел успешно"
            else:
                output += "[-] Ping прошел неуспешно"
        except requests.RequestException:
            output += "[!] Произошла ошибка при проверке"
        return output
    
    
    def check_dns(self) -> str:
        output = "\n--- Проверка DNS  ---\n"
        try:
            socket.gethostbyname(self.hostname)
            output += "[+] DNS работает"
        except socket.gaierror:
            output += "[-] DNS не работает"
        return output
    
    def check_file(self) -> str:
        output = "\n--- Проверка файла ---\n"
        try:
            output += f"Файл - {self.test_file_path}"
            with open(self.test_file_path, "rb") as f:
                f.read()
            output += "[+] Повреждений не найдено"
        except (IOError, OSError):
            output += "[-] Файл поврежден или недоступен"
        return output
    
    def check_free_space(self) -> str:
        output = "\n--- Проверка свободного места ---\n"
        result = psutil.disk_usage('/')
        output += (
            f"Всего - {result.total / (1024**3):.2f}GB\n"
            f"Свободно - {result.free / (1024**3):.2f}GB\n"
            f"Занято - {result.total / (1024**3):.2f}GB\n"
        )
        return output

    def check_cpu(self) -> str:
        output = "\n--- Проверка загруженности процессора ---\n"
        result = psutil.cpu_percent(interval=1)
        output += f"Загрузка процессора - {result}%"
        return output

    def check_ram(self) -> str:
        output = "\n--- Проверка оперативной памяти ---\n"
        result = psutil.virtual_memory()
        output += (
            f"Всего - {result.total / (1024**3):.2f}GB\n"
            f"Свободно - {result.free / (1024**3):.2f}GB\n"
            f"Занято - {result.total / (1024**3):.2f}GB\n"
        )
        return output
    
    def check_services(self) -> str:
        output = "\n--- Проверка служб ---\n"
        for service in self.services:
            result = subprocess.run(["systemctl", "is-active", service], capture_output=True)
            if result.returncode == 0:
                output += f"[+] Служба {service} активна"
            else:
                output += f"[+] Служба {service} не активна"
        return output 

    def check_db_connect(self): 
        output = "\n--- Проверка подключения База данных ---\n"
        try:
            connection = mysql.connector.connect(self.db_config)
            if connection.is_connected():
                output += "[+] Успешно подключено"
            else:
                output += "[-] Не удалось подключиться"
        except:
            output += "[!] При подключении произошли неполадки, проверьте данные"
