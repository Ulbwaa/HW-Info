import os
import platform
import socket
import subprocess
import time

import psutil


class tools:
    @staticmethod
    def clearConsole():
        if psutil.WINDOWS:
            return os.system("cls")
        else:
            return os.system("clear")

    @staticmethod
    def checkOutput(command: str):
        try:
            return subprocess.check_output(command, shell=True,
                                           universal_newlines=True,
                                           stderr=subprocess.DEVNULL)

        except subprocess.CalledProcessError:
            return False


def hwinfo(htmlMarkup=True):
    if psutil.WINDOWS:
        command = 'powershell neofetch --stdout'
    else:
        command = 'neofetch --stdout'

    output = tools.checkOutput(command)

    if output:
        fetch = output.split('- \n')[0] + '- '
        out = output.split('- \n')[0] + '- '

        for i in output.split('- \n')[1].split('\n'):
            if i != '' and i != ' ':
                j = i.split(': ')[0]
                y = i.split(': ')[1]

                if j == 'CPU':
                    fetch += f'\n{j}: {y}'
                    fetch += f'\nCPU Load: {_CPULoad()}'
                    fetch += f'\nCPU Architecture: {_CPUArch()}'

                elif j == 'Memory':
                    fetch += f'\n{j}: {y}'
                    fetch += f'\nSWAP: {_swap()}'
                    fetch += f'\nStorage: {_storage()}'

                elif j == 'Kernel':
                    fetch += f'\n{j}: {y}'
                    fetch += f'\nLocal IP: {_LocalIP()}'

                elif j == 'Uptime':
                    fetch += f'\n{j}: {y}'
                    fetch += f'\nBoot Time: {_BootTime()}'

                elif j == 'Host' and 'Hackintosh' in y:
                    pass

                else:
                    fetch += f'\n{j}: {y}'

        fetch += f'\nPython version: {_python_version()}'

        if _java_version():
            fetch += f'\nJAVA version: {_java_version()}'

        for i in fetch.split('- \n')[1].split('\n'):
            if i != '' and i != ' ':
                j = i.split(': ')[0]
                y = i.split(': ')[1]
                if htmlMarkup:
                    out += f'\n<b>{j}</b>: <code>{y}</code>'

                else:
                    out += f'\n{j}: {y}'

        return out
    else:
        if htmlMarkup:
            return '<b>Neofetch is not installed!</b>'
        else:
            return 'Neofetch is not installed!'


def _LocalIP():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except ConnectionError:
        ip = '127.0.0.1'

    return str(ip)


def _CPUArch():
    return platform.uname().machine.replace('_', '-')


def _CPULoad():
    return f'{round(psutil.cpu_percent(0.5))}%'


def _BootTime():
    return time.ctime(psutil.boot_time())


def _swap():
    all_ = round(psutil.swap_memory().total / 1e+6)
    used = round(psutil.swap_memory().used / 1e+6)

    return f'{used}MiB / {all_}MiB '


def _storage():
    all_ = round(psutil.disk_usage('/.').total / 1e+9)
    used = round(psutil.disk_usage('/.').used / 1e+9)

    return f'{used}GiB / {all_}GiB '


def _python_version():
    return '{} ver. {}'.format(platform.python_implementation(),
                               platform.python_version()).split('ver. ')[1]


def _java_version():
    command = 'java -version 2>&1 | awk -F[\\\"_] \'NR==1{print $2}\''
    JAVA_temp = tools.checkOutput(command)

    if JAVA_temp:
        return JAVA_temp.split('\n')[0].split('.')[0]
    else:
        return False


if __name__ == '__main__':
    tools.clearConsole()
    print('loading...')
    hw = hwinfo(False)
    tools.clearConsole()
    print(hw)
