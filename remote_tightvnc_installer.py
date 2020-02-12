import getpass
import os
import time
import shutil
from colorama import Back, Fore, Style, init
import subprocess


def my_ping():
    global name_pc
    name_pc = input("Введи имя компа:")
    global ping
    ping = os.system("ping %s -n 1 -w 1" % name_pc)
    return ping


def winmr():
    while 5 > 2:
        try_connect = os.system("winrs -r:%s echo ok" % name_pc)
        if try_connect == 0:
            print("Ок служба работает")
            break
        else:
            print("\n\nСлужба оключена сейчас будем включать")
            user = input("\nВведи свою учётку вида (hq\login):")
            password = getpass.getpass("Введи пароль от учетки:")
            winrm = '"winrm quickconfig -quiet & REG ADD HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\services\WinRM /v DelayedAutoStart /d 0 /f"'
            print("Создаем задачу пользователю...")
            rs = os.system('SCHTASKS /Create /S %s /U %s /P %s /F /RL HIGHEST /RU "System" /SC HOURLY /TN RS /TR %s' %
                           (name_pc, user, password, winrm))
        if rs == 1:
            print(
                Fore.RED + "Error не могу создать задачу у пользователя, завершаю скрипт")
            print(Style.RESET_ALL)
            os.system("pause")
            os.abort()
        os.system("timeout /t 7")
        print(Fore.GREEN + "Запускаем remote shell...")
        print(Style.RESET_ALL)
        rs1 = os.system("SCHTASKS /Run /S %s /U %s /P %s /TN RS" %
                        (name_pc, user, password))
        os.system("timeout /t 7")
        print(Fore.GREEN + "\nУдаляем задачу...")
        print(Style.RESET_ALL)
        rs2 = os.system("SCHTASKS /Delete /S %s /U %s /P %s /TN RS /F" %
                        (name_pc, user, password))
        try_connect = os.system("winrs -r:%s echo ok" % name_pc)


def tight():
    os.system("xcopy silent_install \\%s\c$\TV\ /i" % name_pc)
    os.system("xcopy tightvnc-2.7.10-setup-32bit.msi \\%s\c$\TV\ /i" % name_pc)
    os.system("xcopy tightvnc-2.7.10-setup-64bit.msi \\%s\c$\TV\ /i" % name_pc)
    time.sleep(5)
    os.system("winrs -r:%s C:\TV\silent_install.bat" % name_pc)


def silent_install():
    # shutil.copy("tightvnc-2.7.10-setup-64bit.msi", "\\\\%s\c$\TV\ /i" % name_pc )
    subprocess.call(
        "xcopy tightvnc-2.7.10-setup-64bit.msi \\\\%s\c$\TV\ /i" % name_pc)
    subprocess.call(
        "xcopy tightvnc-2.7.10-setup-32bit.msi \\\\%s\c$\TV\ /i" % name_pc)
    subprocess.call("xcopy silent_install.bat \\\\%s\c$\TV\ /i" % name_pc)
    os.system("winrs -r:%s C:\TV\silent_install.bat" % name_pc)


my_ping()
while ping == 1:
    print("Хост недоступен")
    my_ping()
winmr()
silent_install()
