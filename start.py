import os
import time
import subprocess
import sys

files = ["main_nsk.py", "main_alt_kr.py", "main_krasn_kr.py", "main_irk_obl.py", "main_kem_obl.py"]

# Получить путь к интерпретатору Python в текущем виртуальном окружении
venv_python = sys.executable

for file in files:
    subprocess.Popen([venv_python, file])
    time.sleep(240)  # Пауза на 4 минуты
