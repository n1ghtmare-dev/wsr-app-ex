import requests
import psutil
import socket
import subprocess



class Service:
    def check_internet(self, hostname: str = "google.com") -> str:
        output = "\n--- Проверка доступности интернета ---\n"
        try:
            result = requests.get(hostname)
            if result.status_code == 200:
                output += "[+] Интернет доступен"
            else:
                output += "[-] Интернет недоступен"
        except requests.RequestException:
            output += "[!] Проблемы с подключением, проверьте хост"
        return output
    
    def check_ping(self, hostname: str = "google.com") -> str:
        output = "\n--- Проверка доступности интернета ---\n"
        try:
            result = subprocess.run(['ping', '-c', '4', hostname], capture_output=True)
            if result.returncode == 0:
                output += "[+] Ping прошел успешно"
            else:
                output += "[-] Ping прошел неуспешно"
        except requests.RequestException:
            output += "[!] Произошла ошибка при проверке"
        return output
    
    
    def check_dns(self, hostname: str = "googываle.com") -> str:
        output = "\n--- Проверка DNS  ---\n"
        try:
            socket.gethostbyname(hostname)
            output += "[+] DNS работает"
        except socket.gaierror:
            output += "[-] DNS не работает"
        return output
    
    def check_file(self, file_path: str = "test.txt") -> str:
        output = "\n--- Проверка файла ---\n"
        try:
            output += f"Файл - {file_path}"
            with open(file_path, "rb") as f:
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

a = Service()
print(a.check_ram())
        