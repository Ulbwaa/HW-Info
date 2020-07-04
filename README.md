# HW-Info
<p align="center">CLI-скрипт для сбора информации о характеристиках системы.</p>

HW-Info это командная утилита для сбора информации о системе, написанная на Python 3.7+.

HW-Info показывает информацию о вашей операционной системе, программном и аппаратном обеспечении.

HW-Info базируется на bash скрипте <a href='https://github.com/dylanaraps/neofetch'>neofetch</a>, поэтому для обеспечения работоспособности HW-Info необходимо иметь заранее установленный <a href='https://github.com/dylanaraps/neofetch'>neofetch</a>, а также Python-модуль <a href='https://pypi.org/project/psutil/'>psutil</a>.

HW-Info дополняет информацию, выводимую neofetch, а также позволяет использовать ее в ваших Python-скриптах, имея возможность использовать себя как Python-модуль.


# Установка

Как я писал выше, для работоспособности HW-Info необходим neofetch. Ознакомиться с документацией по установке neofetch можно по <a href='https://github.com/dylanaraps/neofetch/wiki/Installation'>этой</a> ссылке.

Установку модуля psutil легче всего провернуть через установщик пакетов для Python - pip. Комманда для установки psutil в эмуляторе консоли будет выглядеть подобным образом:

`python3 -m pip install psutil`

`python3 -m pip install speedtest-cli`


# Использование

Скрипт HW-Info предпологает два сценария использования:

    1. CLI-Скрипт для вывода информации о системе прямо в консоль.
    2. Python-Модуль для вывода информации в любом виде (Будь то сообщение в Telegram-боте или запись данной информации в .txt файл).

Первый сценарий предпологает запуск скрипта через комманду `python3 hwinfo.py`. 

Если вы обладаете компьютером на Unix-системе, то можно настроить запуск скрипта HW-Info используя alias, для этого нужно ввести такую команду: `alias hwinfo='python3 /fullpath/hwinfo.py'`. Помните, вы должны указать полный путь до файла hwinfo.py, иначе работать такая конструкция будет только из под папки, в которой находится hwinfo.py!


Использование HW-Info как модуль предлагает еще одну функцию, вывод информации с заранее заданным шаблоном, в котором используется html разметка по данному принципу: `<b>Key</b>: <code>Value</code>`.

Для этого необходимо импортировать модуль в ваш Python-скрипт используя `import hwinfo` и использовать функцию `hwinfo.hwinfo(htmlMarkup: bool)`, которая возвращает строку с собранными данными. 


# Пример использования

Готовый кусок кода для использования в Telegram-ботах под управлением библиотеки <a href='https://pypi.org/project/aiogram/'>aiogram</a>:

```python
from aiogram import Bot, Dispatcher, executor, types
import hwinfo

bot = Bot(token='TOKEN')

dp = Dispatcher(bot)


@dp.message_handler(commands=['hwinfo', 'fetch', 'hw'])
async def hw_info(message: types.Message):
    text = '<b>Loading...</b>'
    temp_message = await message.reply(text, parse_mode='html')
    fetch = await hwinfo.hwinfo(True)
    return await temp_message.edit_text(fetch, parse_mode='html')

@dp.message_handler(commands=['speedtest', 'hwinfo-speedtest', 'hw-speedtest'])
async def hw_info_speedtest(message: types.Message):
    text = '<b>Loading...</b>'
    temp_message = await message.reply(text, parse_mode='html')
    speedtest = await hwinfo.speedtest(True)
    return await temp_message.edit_text(speedtest, parse_mode='html')


if __name__ == '__main__':
    hwinfo.tools.clearConsole()
    print('Started!')
    executor.start_polling(dp, skip_updates=True)
```


# Скриншоты

Как отдельное приложение:
<p align="center">
    <img src="https://i.imgur.com/vs7LTCQ.jpg" alt="HW-Info в качестве отдельного CLI скрипта.">
</p>

Как Python-модуль:
<p align="center">
    <img src="https://i.imgur.com/pLLnCvy.png" alt="HW-Info в качестве Python-модуля." height="550px">
</p>
<p align="center">(В данном случае HW-Info используется в <a href='https://t.me/QuotesAPI_bot'>Telegram-боте.</a>)</p>