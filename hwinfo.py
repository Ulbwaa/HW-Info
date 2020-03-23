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
                    fetch += f'\nCPU Load: {getCPULoad()}'
                    fetch += f'\nCPU Architecture: {getCPUArch()}'

                elif j == 'Memory':
                    fetch += f'\n{j}: {y}'
                    fetch += f'\nSWAP: {getSwap()}'
                    fetch += f'\nStorage: {getStorage()}'

                elif j == 'Kernel':
                    fetch += f'\n{j}: {y}'
                    fetch += f'\nLocal IP: {getLocalIP()}'

                elif j == 'Uptime':
                    fetch += f'\n{j}: {y}'
                    fetch += f'\nBoot Time: {getBootTime()}'

                elif j == 'Host' and 'Hackintosh' in y:
                    pass

                else:
                    fetch += f'\n{j}: {y}'

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


def getLocalIP():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except ConnectionError:
        ip = '127.0.0.1'

    return str(ip)


def getCPUArch():
    return platform.uname().machine.replace('_', '-')


def getCPULoad():
    return f'{round(psutil.cpu_percent(0.5))}%'


def getBootTime():
    return time.ctime(psutil.boot_time())


def getSwap():
    all_ = round(psutil.swap_memory().total / 1e+6)
    used = round(psutil.swap_memory().used / 1e+6)

    return f'{used}MiB / {all_}MiB '


def getStorage():
    all_ = round(psutil.disk_usage('/.').total / 1e+9)
    used = round(psutil.disk_usage('/.').used / 1e+9)

    return f'{used}GiB / {all_}GiB '


if __name__ == '__main__':
    tools.clearConsole()
    print('loading...')
    hw = hwinfo(False)
    tools.clearConsole()
    print(hw)
