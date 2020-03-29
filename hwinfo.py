import os
import platform
import socket
import subprocess
import time
import random

import http.client
import psutil


version = '1.3-release'
git = 'https://github.com/Ulbwaa/HW-Info'
projects = 'https://ulbwa.suicide.today/projects/'


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


def hwinfo(htmlMarkup=True, showThreadsPercentage=True):
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

                    if _users():
                        fetch += f'\nUsers: {_users()}'

                    if not _IPs_Check():
                        fetch += f'\nGlobal IP: {_http_ip()}'
                        fetch += f'\nLocal IP: {_LocalIP()}'
                    else:
                        fetch += f'\nLocal / Global IP: {_http_ip()}'

                    if _mother_board():
                        fetch += f'\nMotherboard: {_mother_board()}'

                elif j == 'Uptime':
                    fetch += f'\n{j}: {y}'
                    fetch += f'\nBoot Time: {_BootTime()}'

                elif j == 'Host' and 'Hackintosh' in y:
                    pass

                else:
                    fetch += f'\n{j}: {y}'

        fetch += f'\nPython version: {_python_version()}'

        if _where_python():
            fetch += f'\nPython path: {_where_python()}'

        if _java_version():
            fetch += f'\nJAVA version: {_java_version()}'

        if _where_java():
            fetch += f'\nJAVA path: {_where_java()}'

        fetch += f'\nHW-Info version: {_hwinfo_version()}'

        if showThreadsPercentage:
            fetch += '\n'
            for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
                fetch += f'\nThread {i + 1} load: {round(percentage)}%'

        for i in fetch.split('- \n')[1].split('\n'):
            if i != '' and i != ' ':
                j = i.split(': ', maxsplit=1)[0]
                y = i.split(': ', maxsplit=1)[1]
                if htmlMarkup:
                    out += f'\n<b>{j}</b>: <code>{y}</code>'

                else:
                    out += f'\n{j}: {y}'
            else:
                out += '\n'

        if htmlMarkup and random.randint(1, 3) == 3:
            out += '\n\n<b>HW-Info</b> is an <b>open source project</b>. ' \
                   'You can use this module in your projects by downloading it on <b>GitHub!</b> ' \
                   f'Link to download source: <code>{git}</code>. ' \
                   f'My other projects are available for review at the following link: ' \
                   f'<code>{projects}</code>.'

        return out
    else:
        if htmlMarkup:
            return '<b>Neofetch is not installed!</b>'
        else:
            return 'Neofetch is not installed!'


def _IPs_Check():
    return str(_LocalIP()) == str(_http_ip())


def _LocalIP():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except ConnectionError:
        ip = '127.0.0.1'

    return str(ip)


def _users():
    try:
        users = []

        for user in psutil.users():
            if str(user.name) not in users:
                users.append(str(user.name))

        if users == [] or len(users) <= 0:
            return False
    except (Exception, BaseException):
        return False

    return ', '.join(users)


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
        return JAVA_temp.split('\n')[0]
    else:
        return False


def _http_ip():
    conn = http.client.HTTPConnection("ifconfig.me")
    conn.request("GET", "/ip")
    return conn.getresponse().read().decode('UTF8')


def _hwinfo_version():
    return version


def _mother_board():
    if psutil.WINDOWS:
        command = 'wmic baseboard get Manufacturer'
        mother = tools.checkOutput(command)

        if mother:
            manuf = mother.split('\n')[2]
        else:
            return False

        command = 'wmic baseboard get product'
        mother = tools.checkOutput(command)

        if mother:
            module = mother.split('\n')[2]
        else:
            return False

        return manuf + ' ' + module
    else:
        return False


def _where_python():
    command = 'where python3'
    output = tools.checkOutput(command)

    if output:
        return output.split('\n')[0]
    else:
        return False


def _where_java():
    command = 'where java'
    output = tools.checkOutput(command)

    if output:
        return output.split('\n')[0]
    else:
        return False


if __name__ == '__main__':
    tools.clearConsole()
    print('loading...')
    hw = hwinfo(False, False)
    tools.clearConsole()
    print(hw)
