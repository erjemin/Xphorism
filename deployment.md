# Развертывание: Raspberry pi → Debian → virtualenv → Python/Django → nginx → uWSGI

В моем случае разворачиваю проект под Raspberry pi 3 и операционной системой Raspbian GNU/Linux 8.0, которая представляет из себя разновидность Debian (jessie, Linux version 4.4.21-v7+) собранной специально под Raspberry pi. Развертывание под другие разновидности Debian (Ubuntu, Runtu, gNewSense и пр.) принципиально не отличается.

На «голом» Raspberry pi уже есть суперпользователь по умолчанию -- **pi**. У него открыт доступ по SSH. Но в силу того, что такой пользователь есть на всех Raspberry pi, то для безопасности лучше закрыть ему SSH-доступ, создать нового пользователя и выполнять команды и запускать нужные нам сервисы от его имени. Наш пользователь будет называться **[user]**, замените его на своего.

**!!!ВАЖНО: ВСЕ ЗНАЧЕНИЯ, ПОМЕЩЕННЫЕ В КВАДРАТНЫЕ СКОБКИ НАДО ЗАМЕНИТЬ НА СВОИ СОБСТВЕННЫЕ. ЭТО КАСАЕТСЯ ИМЕНИ [user], ПАРОЛЕЙ [password], [адрес сайта] И ВСЕГО ТАКОГО ПРОЧЕНО. В ОБЩЕМ, ВЫ МЕНЯ ПОНЯЛИ!!!**

## Полезные «ритуальные» действия при первом запуске Rasperry pi под Debian

### Меняем имя хоста

Не лишним будет сменить имя (hostname) нашему серверу. Чтобы сменить его надо дать команду `sudo hostname [new-hostname]`. Срабатывает это не всегда, так что лучше сразу поступить более радикальным методом -- отредактировав конфигурационный файл `/etc/hostname`. Используем текстовый редактор **nano**:
```bash
sudo nano /etc/hostname
```
В этом файле всего одно слово -- debian -- имя нашего хоста. Удаляем и вписываем наше [hostname]. Сохраняем файл `Ctrl+O` и `Enter`, а затем выходим из редактора `Ctrl+X`.

Перезагружаемся, чтобы изменения вступили в силу:
```bash
sudo reboot
```

Теперь надо добавить наш новый hostname в список доступных хостов. Открываем на редактирование `/etc/hosts`:
```bash
sudo nano /etc/hosts
```
Находим в нем строчку:
```bash
127.0.0.1     localhost
```
и вписываем в нее нашt новое имя сервера (hostname). Должно получиться как-то так:
```bash
127.0.0.1       localhost       [hostname]
```
Сохраняем файл `Ctrl+O` и `Enter`, а выходим из редактора `Ctrl+X`.

### Меняем локаль -- русифицируем

Локаль -- это серверная инфраструктура для поддержки в системе нескольких языков. С её помощью поддерживается алфавит, порядок сортировки, формат даты и много чего полезного, что очень важно для работы будущего веб-сервера. Кроме того можно будет настроить язык сообщений на русский, что тоже пригодится. Запускаем утилиту смены локали:
```bash
sudo dpkg-reconfigure locales
```
На первом экране утилиты `dpkg-reconfigure` нам предложат выбрать локали. По умолчанию стоит `en_US.UTF-8 UTF-8`. Нам нужно добавить, как минимум русский `ru_RU.UTF-8 UTF-8`.

На втором экране `dpkg-reconfigure` выбирается язык отображения и системных сообщений (для всей системы, а не для конкретного пользователя). Выбираем `ru_RU.UTF-8`.

Иногда, чтобы локали вступили в силу, нужно перегрузиться: `sudo reboot`. Если случайно установили лишние локали, то удалить лишние можно с помощью `apt-get install localepurge`.

### Установка часового пояса

Для корректной работы с временем нам нужно задать часовой пояс нашего сервера. Тогда и в скриптах и в базе данных время будет отображаться корректно:
```bash
sudo dpkg-reconfigure tzdata
```

### Апдейт, апгрейд и чистка

Теперь можно обновить пакеты в системе:
```bash
sudo apt-get update
```
Обновить систему:
```bash
sudo apt-get upgrade
```
И очистить ее от лишних пакетов:
```bash
sudo apt-get autoremove
sudo apt-get autoclean
```

### «Растягиваем» партицию и файловую систему

Создавая загрузочную miniSD-карту для системы, разместилось всего около 4Gb нашего «диска. Чтобы использовать весь объем нашей SD-карточки нужно увеличить раздел (партицию) диска и «растянуть» файловую систему на все доступное пространство. Самое простое -- извлечь из нашего Rasperry pi карточку памяти, вставить ее в компьютер с Ubuntu и воспользоваться утилитой `GParted` в которой изменить размер или переместить раздел (Resize/Move) [проще простого](http://help.ubuntu.ru/manual/%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%82%D0%BA%D0%B0_%D0%B4%D0%B8%D1%81%D0%BA%D0%B0). Сделать это можно было сразу после создании miniSD из img-образа.

Если по рукой нет к компьютера с Ubuntu и `GParted`, то придется следовать тернистым путем описанном [в этой статье на hadrahabr](https://habrahabr.ru/post/252973/) и google вам в помощь.


# Создание пользователя и SSH-доступ

## Создаем нового пользователя

Пока мы еще залогированы под пользователем ubuntu, но нам понадобится создать и настроить пользователя, от имени которого мы будем работать. Создадим такого пользователя и его пароль:

```bash
sudo useradd [user] -m -G 4,27 -g -c "[Имя-Фамилия-и-прочее-прочее-для-информации"
sudo passwd [user]
```
где, после ключа` -G` через запятую указаны группы в которые надо ключить вновь созданного пользователя. Для нашего Raspberry pi будет достаточно следующих групп: **4** -- *adm* (администраторы), **27** -- *sudo* (группа с правами суперпользователя, с возможность устанавливать и запускать системные пакеты). Если нам понадобится монтировать внешние накопители (например, жесткие диски подключаемые через USB) то надо добавить группу **46** (plugdev), для работы со звуком -- **29**, для работы с демонами -- **30** (dip) и так далее. Посмотреть все группу в которые включен наш базовый пользователь можно командой `id`.

Ключ `-g` присваивает первичную группу пользователей нашего текущему пользователю **pi**. Это делает все его настройки пользователя идентичным текущему и фактически будет использовать все его настройки.

## Настраиваем SSH-доступ

По идее можно разлогироваться и заходить по SSH под новым, только что созданным пользователем, но можно сразу сделать небольшие изменения в файле `/etc/ssh/sshd_config` -- конфигурации ssh-доступа:

```sudo
sudo nano /etc/ssh/sshd_config
```

Полное описание настроек `sshd_config` находится [на сайте Ubuntu](http://help.ubuntu.ru/wiki/ssh). Там содержатся вполне разумные рекомендации по увеличению безопасности. Но в нашем случае к ним нужно немного добавить. Дописываем в конце следующие две строки, и запрещаем ssh-вход пользователя **ubuntu** (пользователю по умолчанию) и разрешаем доступ нашему вновь созданному пользователю **[user]**:
```cfg
DenyUsers pi
AllowUsers [user]
```

Напоследок, убираем `#` в строчке `#Banner /etc/issue.net`. Баннеры -- это красиво и пусть он приветствует нас при каждом ssh-подключении. Сохраняем файл `/etc/ssh/sshd_config` -- `Ctrl+O` и `Enter`, а выходим из редактора `Ctrl+X`. Создаем наш красивый баннер:
```bash
sudo nano /etc/issue.net
```

И помещаем туда красивый ASCII-арт текст:
```
                       |                                   _)
    __| _` |  __| __ \  __ \   _ \  __|  __| |   |    __ \  |
   |   (   |\__ \ |   | |   |  __/ |    |    |   |    |   | |
  _|  \__,_|____/ .__/ _.__/ \___|_|   _|   \__, |    .__/ _|
                 _|                         ____/    _|
```
Можете найти в интернете онлайн-утилиты, создать и добавить что-то своё.  Сохраняем баннер `Ctrl+O` и `Enter`, а выходим из редактора `Ctrl+X`.

Также стоит удалить ssh-приветсвие, очистив файл `/etc/motd` 
```bash
sudo nano /etc/motd
```
Удаляем все. что там написано. Сохраняем `Ctrl+O` и `Enter`, а выходим из редактора `Ctrl+X`.

Очень полезно при входе в систему (не только по SSH) отобразать служебную информацию о загрузке системы. Для этого надо в ппапку `/etc/profile.d/` добавить скрипт, который будет исполнятся при каждом входе. Отнрываем вайл на редактирование:
```bash
sudo nano /etc/profile.d/sshinfo.sh
```
Помещаем в него следующий скрипт:
```bash
SystemMountPoint="/";
LinesPrefix="  ";
b=$(tput bold); n=$(tput sgr0);

SystemLoad=$(cat /proc/loadavg | cut -d" " -f1);
ProcessesCount=$(cat /proc/loadavg | cut -d"/" -f2 | cut -d" " -f1);

MountPointInfo=$(/bin/df -Th $SystemMountPoint 2>/dev/null | tail -n 1);
MountPointFreeSpace=( \
  $(echo $MountPointInfo | awk '{ print $6 }') \
  $(echo $MountPointInfo | awk '{ print $3 }') \
);
UsersOnlineCount=$(users | wc -w);

UsedRAMsize=$(free | awk 'FNR == 3 {printf("%.0f", $3/($3+$4)*100);}');

SystemUptime=$(uptime | sed 's/.*up \([^,]*\), .*/\1/');

if [ ! -z "${LinesPrefix}" ] && [ ! -z "${SystemLoad}" ]; then
  echo -e "${LinesPrefix}${b}Загрузка системы:${n}\t${SystemLoad}\t\t${LinesPrefix}${b}Процессов:${n}\t\t${ProcessesCou$
fi;

if [ ! -z "${MountPointFreeSpace[0]}" ] && [ ! -z "${MountPointFreeSpace[1]}" ]; then
  echo -ne "${LinesPrefix}${b}Диск ($SystemMountPoint):${n}\t${MountPointFreeSpace[0]} из ${MountPointFreeSpace[1]}\t\t$
fi;
echo -e "${LinesPrefix}${b}Юзеров в системе:${n}\t${UsersOnlineCount}";

if [ ! -z "${UsedRAMsize}" ]; then
  echo -ne "${LinesPrefix}${b}Память:${n}\t${UsedRAMsize}%\t\t\t";
fi;
echo -e "${LinesPrefix}${b}Аптайм:${n}\t${SystemUptime}";
```
Сохраняем `Ctrl+O` и `Enter`, и выходим из редактора `Ctrl+X`. Затем надо дать право на запуск этого скрпита:
```bash
chmod +x /etc/profile.d/sshinfo.sh
```

Чтобы настройки подействовали нужно перезапустить ssh-сервис:
```bash
sudo service ssh restart
```

Разлогируемся. Можем тут же проверить, что теперь пользователя **pi** больше в систему по SSH не пускают. Логируется вновь созданным пользователем **[user]** и мы готовы перейти к настройкам проекта. Но...

## «Вишенка на торте» -- настраиваем сообщение при входе в систему и раскрашиваем оболочку bash

При входе в систему последовательно выполняются скрипты из папки `/etc/update-motd.d`. Они обеспечивают вывод приглашения и служебной информации. Убрать часть бесполезных подсказок можно просто запретив исполнение ненужных скриптов:
```bash
sudo chmod -x /etc/update-motd.d/10-help-text
sudo chmod -x /etc/update-motd.d/51-cloudguest
```
Теперь добавим скрипт `/etc/update-motd.d/50-landscape-sysinfo`, который обеспечит вывод важной дополнительной информации о состоянии системы. Заодно это установит дополнительные пакеты, некоторые из которых пригодятся в проекте:
```bash
sudo apt install landscape-common
```

И чтобы сделать красочно-разноцветным нашу командную строку откроем на редактирование файл настроек оболочки bash пользователя `.bashrc':
```bash
nano ~/.bashrc
```
находим там строку `# force_color_prompt=yes` раскомментируем её (и удаляем в ней `#`). И чтобы совсем отпад, находим блок:
```bash
if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
```
и меняем на блок
```bash
if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[01;33m\]@\[\033[01;32m\]\h\[\033[00m\]:\[\033[00;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
```

Все! Перелогиниваемся чтобы настройки подействовали. Дальше нам понадобится сервер базы данных МySQL. Установим его:

-----

# Установка и настройка сервера MySQL

Установка сервера базы данных MySQL исключительно проста. Достаточно одной команды:
```
sudo apt-get install mysql-server
```

В процессе установки будет дважды запрошен пароль **root** -- сперпользователя базы. Лучше, чтобы пароль был посложнее и отличался от пароля нашего текущего (и всех остальных) пользователей. Так как мы будем использовать его дальше в инструкции, то обозначим его: «_secret_password_mysql_root_». 

Если при установке запрос **root**-суперпользователя базы не будет запрошен, то его придется установить вручную. Для этого можно воспользоваться инструкциями по смене root-пароля из интернет. Например: https://www.8host.com/blog/sbros-parolya-root-v-mysql-i-mariadb/

Иногда, при установке MySQL может установиться MirandaDB (сейчас идет массовая замена дистрибивов и отказ от Oracle). Miranda DB -- бинарно совместима с MySQL. 

Теперь у нас есть MySQL. Заходим в него под root-пользователем.
```bash
mysql -u root -p secret_password_mysql_root
```

Появится сообщение:
```sql
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 38
Server version: 5.5.52-0+deb8u1 (Raspbian)

Copyright (c) 2000, 2016, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```

Поздравляю, мы внутри консольного клиента MySQL. Создаем базу данных нашего проекта **(django_xphorism)**:
```sql
CREATE DATABASE django_xphorism DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
```
Затем, чтобы наше Django-приложение не работало с базой под аккаунтом  супер-пользователя **root**, создаем нового пользователя базы **[user]** с паролем «_secret_password_mysql_user_»:
```sql
GRANT ALL PRIVILEGES ON django_xphorism.* TO '[user]'@'localhost' IDENTIFIED BY 'secret_password_mysql_user';
```

Если по какой-либо причине, нам понадобится удаленный доступ от имени этого пользователя (например, для работы с базой посредством удаленного клиент-менеджера, на подобии dbForge Studio или MySQL Workbench), то можно заменить `'localhost'` на `'%'`. Если захотим разрешить этому пользователю доступ и ко всем jcnfkmysv базам в нашем MySQL-сервере, то необходимо заменить `PRIVILEGES ON django_xphorism.*` на  `PRIVILEGES ON *.*`.

Перед выходом из MySQL стоит проверить, что в ней установлен правильный часовой пояс:
```sql
SHOW VARIABLES LIKE '%time_zone%';
```

Работа с базой закончена. Можно выйти из MySQL `Ctrl+C`.

Если мы создали MySQL-пользователя с возможностью удаленного доступа, то нам понадобиться изменить конфигурационный файл MySQL. Открываем его на редактирование:

```
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
```
Находим строчку `bind-address = 127.0.0.1` и комментируем ее `# bind-address = 127.0.0.1` или, если даём доступ только с определённого IP, то указываем его: `bind-address = 192.168.1.40`. Более сложные правила доступа следует настраивать через *firewall*.

Туда же, в блок `[mysqld]` можно добавить инструкции для последующего использования юнкоровской кодировки **utf-8** при создании таблиц и баз данных.
```python
character-set-server    = utf8
collation-server        = utf8_general_ci
```

Сохраняем конфиг-файл MySQL `Ctrl+O`, `Enter` и `Ctrl+X`, а затем, перезапускаем MySQL чтобы изменения конфигурационного файла подействовали:
```
sudo service mysql restart
```

MySQL и база проекта настроены. Теперь нам нужно настроить виртуальное окружение проекта.

-----

# Развертывание проекта и настройка виртуального окружения

Развертывание системы управления деревом классификатора
-------------------------------------------------------

У нас на сервере будет нескольких сайтов, то нужно выделить отдельный каталог для каждого. Для простоты лучше называть каталог также, как и сайт. Наш сайт будет называться **[адрес сайта]**, а значит пусть и папка будет иметь такое же имя. Создадим её и перейдем внутрь:
```bash
mkdir -p $HOME/[адрес сайта]
cd $HOME/[адрес сайта]
```

Чтобы развернуть проект из git-hub-а нам понадобится система контроля версий **git**. Установим её:
```bash
sudo apt-get install git
```

Теперь мы можем просто скопировать проект из репозитория git в свою папку с помощью `git clone`:
```bash
git clone https://github.com/erjemin/Xphorism
```

Настройка виртуального окружения проекта
----------------------------------------

Для того, чтобы наш проект мог использовать собственные библиотеки python (в том числе и собственную версию Djagino) и не зависеть от общих настроек Python на сервере, надо установить серверный пакет виртуального окружения **python-virtualenv**. В него, при необходимости, можно установить даже отдельную версию самого Python.
```bash
sudo apt-get install python-virtualenv
```


Теперь развернем виртуальное окружение. Оно создаст каталог, в котором будут находится файлы виртуального окружение (версия Python, установщик пакетов pip, wheel, setuptools а также все необходимые нам пакеты, батарейки, свистелки и хрюкалки нашего проекта).
```bash
virtualenv $HOME/[адрес сайта]/env
```

Для накатывания пакетов именно в виртуальное окружение его надо активировать и сделать локальной (текущей) средой окружения.
```bash
source $HOME/[адрес сайта]/env/bin/activate
```

Теперь все наши пакеты будут устанавливаться в виртуальное окружение и попадать в папку `$HOME/[адрес сайта]/env/`. Устанавливаем необходимую нам версию фреймворка Django:
```
pip install Django==1.11.7
```

Проверяем, что Django установилась правильно и нужной версии. Вводим:
```
django-admin version
```

Если виртуальное окружение настроено и активировано правильно, а Django установлено корректно, выведется строка с текущей версией Django:
> 1.11.7

Продолжаем установку необходимых модулей -- коннекторов mySQL и прочее. Понадобится всего две библиотеки (остальные находятся в зависимостях и установятся сами... перечень всех необходимых модулей в [requirements_e450.txt](https://github.com/erjemin/Xphorism/blob/master/public/requirements_e450.txt)):
```bash
pip install MySQL-python==1.2.5
pip install django-debug-toolbar==1.8
```

Возможна ошибка по причине нехватки dev-модулей для сборки много-потоковых коннекторов. Устанавливаем их с помощью `sudo apt-get install python-dev libmysqlclient-dev build-dep python-mysqldb` и повторяем предыдущую операцию.

Наш проект подготовлен. Можем создать миграцию, которая создаст все необходимые таблицы в нашей базе дынных. Но перед тем как ее выполнить нам надо исправить настройки проекта `settings.py` и указать в ней настройки наших папок и логинов в базу данных:
```
nano $HOME/[адрес сайта]/Xphorism/Xphorism/settings.py
```

Находим в ней строки для настройки почты и меняем значения `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER` и `EMAIL_HOST_PASSWORD` для работы email:
```Python
EMAIL_HOST  = 'mail.server.ru'                 # хост почтового SMTP-сервера
EMAIL_PORT  = 2525                             # порт  почтового SMTP-сервера
EMAIL_HOST_USER = '[user]@server.ru'           # логин (email) для входа на почтовый сервер
EMAIL_HOST_PASSWORD = 'password_to_mail'       # пароль для входа на почтовый сервер
```
Аналогичные изменения вносим для настроек рабочих каталогов файлов статики, медия и базы данных. Для файлов меняем параметры `STATIC_ROOT`, `STATIC_BASE_PATH` и `MEDIA_ROOT` указывая вместо **`[user]`** имя нашего пользователя, а вместо **`[адрес сайта]`** имя папки, которая, как мы договорились ранее, совпадает с адресом сайта. Для базы данных меняем параметры `'USER'` и `'PASSWORD'`:
```Python
if (socket.gethostname() == 'debian01'):
    # НАЗНАЧЕНИЕ ДИРЕКТОРИЙ ДЛЯ ПРОДАКШН-СЕРВЕРА (RASPBERRY PI 3) ----
    STATIC_ROOT = '/home/[user]/[адрес сайта]/public/static'
    MEDIA_ROOT  = '/home/[user]/[адрес сайта]/public/public/media/'
    MY_SITE_ROOT= '/home/[user]/[адрес сайта]/public/'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': 'localhost',                         # хост для соединения с базой данных
            'PORT': '3306',                              # порт для соединения с базой данных
            'NAME': 'django_xphorism',                   # имя базы данных
            'USER': '[user]',                            # пользователь базы данных
            'PASSWORD': 'secret_password_mysql_user',    # пароль пользователя базы данных
            'OPTIONS': { 'autocommit': True, }
        }
    }
```
Кроме того, для тестирования с помощью встроенного в Django веб-сервера необходимо указать ip-адрес нашено сервера:
```Python
 ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '192.168.1.11',         # ip-адрес сервера для консольного тестирования через manager.py
    'x.cube2.ru',
]
```
Сохраняем файл `Ctrl+O` и `Enter`, а затем выходим из редактора `Ctrl+X`. Переходим в папку проекта:
```bash
cd ~/[адрес сайта]/Xphorism
```
и выполняем миграцию:
```bash
python manage.py migrate
```

Django сообщит нам о создании всех необходимых таблиц. Теперь можем проверить хорошо ли у нас с безопасностью:
```bash
python manage.py check --deploy
```

Django сообщит какие настройки в `settings.py` нам еще необходимы для ее повышения. В нашем случае должны выскочить сообщения:
> ?: (security.W001) You do not have 'django.middleware.security.SecurityMiddleware' in your MIDDLEWARE_CLASSES so the SECURE_HSTS_SECONDS, SECURE_CONTENT_TYPE_NOSNIFF, SECURE_BROWSER_XSS_FILTER, and SECURE_SSL_REDIRECT settings will have no effect.

> ?: (security.W012) SESSION_COOKIE_SECURE is not set to True. Using a secure-only session cookie makes it more difficult for network traffic sniffers to hijack user sessions.

> ?: (security.W016) You have 'django.middleware.csrf.CsrfViewMiddleware' in your MIDDLEWARE_CLASSES, but you have not set CSRF_COOKIE_SECURE to True. Using a secure-only CSRF cookie makes it more difficult for network traffic sniffers to steal the CSRF token.

> ?: (security.W017) You have 'django.middleware.csrf.CsrfViewMiddleware' in your MIDDLEWARE_CLASSES, but you have not set CSRF_COOKIE_HTTPONLY to True. Using an HttpOnly CSRF cookie makes it more difficult for cross-site scripting attacks to steal the CSRF token.

Можем их проигнорировать, так как доступа по https-протоколу (с SSL-шифрованием) наш проект поддерживать не планирует, а куки для дополнительной защиты токенов проект не использует.


Теперь создаём суперпользователя Django. С его помощью мы сможем входить в административную панель Django:
```bash
python manage.py createsuperuser
```
Нам предложат указать логин администратора Django, его email и пароль доступа. Пароль должен быть не менее восьми символов:
```
It must contain at least 8 characters.

Username (leave blank to use 'user'): [user]
Email address: [user]@mail.me
Password:
Password (again):
Superuser created successfully.
```

Теперь надо создать каталоги `media` и `static/js`, т.к. для проекта они нужны, а в дипозитории git их нет, а значит они и не были созданы при клонировании.
```bash
mkdir -p $HOME/[адрес сайта]/Xphorism/static/js
mkdir -p $HOME/[адрес сайта]/Xphorism/media
```

Теперь перенесем статические файлы панели администратора из каталогов виртуального окружения в папки статических файлов нашего сайта:
```
python manage.py collectstatic
```
Получим сообщения о переносе файлов:
```
You have requested to collect static files at the destination
location as specified in your settings:

/home/[user]/[адрес сайта]/Xphorism/static

This will overwrite existing files!
Are you sure you want to do this?

Type 'yes' to continue, or 'no' to cancel: yes
Copying '/home/[user]/[адрес сайта]/env/local/lib/python2.7/site-packages/django/contrib/admin/static/admin/fonts/Roboto-Light-webfont.woff'
Copying '/home/[user]/[адрес сайта]/env/local/lib/python2.7/site-packages/django/contrib/admin/static/admin/fonts/LICENSE.txt'
...
...
...
Copying '/home/[user]/[адрес сайта]/env/local/lib/python2.7/site-packages/django/contrib/admin/static/admin/img/gis/move_vertex_on.svg'
Copying '/home/[user]/[адрес сайта]/env/local/lib/python2.7/site-packages/django/contrib/admin/static/admin/img/gis/move_vertex_off.svg'

57 static files copied to '/home/[user]/[адрес сайта]/public/static', 8 unmodified.
```

Все! Проект развернут, настроен и готов к тестовому запуску с помощью встроенного в Django веб-сервера:
```bash
python manage.py runserver [адрес сайта]:7000
```

Теперь набрав в браузере `http://[адрес сайта]:7000` мы должны увидеть, что проект работает.

Надо учесть, что раздача статических файлов Django-сервером для разработки при работе на внешний адрес не предусмотрено. То есть статические файлы, CSS файлы, JavaScript, изображения и другие файлы по адресу MEDIA_URL и STATIC_URL не будут доступны. Нам это и не надо, так как наша цель настроить боевой веб-сервер, а не тестовый сервер разработчика. Запуск тестового веб-сервера нужна исключительно чтобы убедиться, что наш проект настроен корректно и Python-скрипты Django работают.

Если интересно, то узнать, как настроить раздачу файлов можно из раздела Django-документации: [Работа со статическими файлами (CSS, изображения)](http://djbook.ru/rel1.8/howto/static-files/index.html).

Завершаем работу тестового веб-сервера Django нажатием `Ctrl-C`

Теперь мы можем перейти к настройке боевого веб-сервера. Но перед этим нам нужно покинуть виртуальное окружение, в котором мы настроили наш проект и тестировали. Деактивация виртуального окружения производится командой `deactivate`. Теперь мы будем работать с системными библиотеками:
```bash
deactivate
```

-------

# Установка веб-сервера nginx.


На сервере может быть уже установлен другой web-сервер -- **Apache**. Придется его удалить самым радикальным способом.

Удаляем веб-сервер apache
-------------------------
Сначала удаляем все его компоненты:
```bash
sudo apt-get purge apache2 apache2-utils apache2.2-bin apache2-common
```

Затем чистим неиспользуемые («подвисшие») и зависимые пакеты, которые не удалилось деинсталлировать с помощью предыдущей команды:
```bash
sudo apt-get autoremove
```

Ищем файлы, который остались от Apache2 (папки, которые не удалились, файлы конфигураций и т.д.):
```bash
whereis apache2
```

Получаем список директорий (чаще всего одну `/etc/apache2`, в которой могли остаться конфигурационные файлы и остальной мусор), смотрим их содержимое. Если в них ничего важного нет, то удаляем командой:
```bash
sudo rm -rf /etc/apache2
```

Все. Мы избавились от Apache2.

Установка и настройка веб-сервера nginx
---------------------------------------

### подготовка к установке nginx


Установка и настройка веб-сервера nginx
---------------------------------------

### подготовка к установке nginx

В репозитрии Raspbian Linux уже есть nginx, но на всякий случай мы подключим дополнительный репозиторий самого nginx. Это позволит нам получать обновления немного раньше, чем они попадут в репозиторий Raspbian. Для проверки подлинности подписи nginx-репозитория, и чтобы избавиться от предупреждений об отсутствующем PGP-ключе во время установки пакета, необходимо добавить ключ, которым были подписаны пакеты и репозиторий nginx, в связку ключей программы apt. Загружаем этот ключ в корень домашней папки:
```bash
cd $HOME
wget http://nginx.org/keys/nginx_signing.key
```

И добавим этот ключ в связку ключей наших репозиторив:
```bash
sudo apt-key add nginx_signing.key
```
После указываем имя нужного нам дистрибутива в файле со списком репозиториев `/etc/apt/sources.list`. Открываем список на редактирование:
```bash
sudo nano /etc/apt/sources.list
```
Для системы под Ratpberry pi под Debian Linux (а на Raspbian Linux – разновидность Debian) в конец файла надо добавить:
```
deb http://nginx.org/packages/debian/ jessie nginx
deb-src http://nginx.org/packages/debian/ jessie nginx
```
Для других систем (Ubuntu/SLES/RHEL/CentOS) вместо ***jessie*** надо указать соответствующие имя дистрибутива. Кодовые имена дистрибутивов можно указать [на страничке описаний пакетов nginx](http://nginx.org/ru/linux_packages.html#distributions).

Сохраняем файл `Ctrl+O` и `Enter`, а затем выходим из редактора nano `Ctrl+X`. Теперь можно проверить обновления репозиториях. Это особенно важно если мы разворачиваем наш проект на новой машинке или свежей VPS, где девственно-чистая система:
```bash
sudo apt-get update
```

Можно, при желании, произвести и upgrade системы
```bash
sudo apt-get upgrade
```

Удаляем, теперь уже не нужный, PGP-ключ из корня домашней папки и освобождаем место:
```bash
rm $HOME/nginx_signing.key
```

### Установка nginx

В состав Django входит простенький веб-сервер, на котором мы испытали установку окружения и развертывание Django-приложения. Он позволяет сразу просмотреть работу сайта в процессе разработки, но для работы на хостинге нужно более серьезное решение. В нашем случае -- nginx.

НАм нужно его установить:
```bash
sudo art-get install nginx
```

К сожалению, в репозиториях Debian для Raspbery pi лежат не самые свежие пакеты. Иногда они реально очень старые, и если нас это не устраивает, то можно поверх уже установленной версии <накатить> версию из исходников. Сначала устанавливаем пакеты, необходимые для сборки nginx из исходников (компилятор С++, библиотеки и все такое):
```bash
sudo apt-get install gcc
sudo apt-get install build-essential
sudo apt-get install libpcre3-dev
sudo apt-get install libcurl4-openssl-dev
sudo apt-get install libexpat1-dev
```

Смотрим [на сайте nginx](http://nginx.org/ru/download.html) актуальную, стабильную версию, скачиваем ее в домашнюю директорию и распаковываем исходники. Переходим в папку, в которую все распаковалось. В ней будем собирать пакет:
```bash
cd $HOME
wget http://nginx.org/download/nginx-1.10.1.tar.gz
tar -zxvf nginx-1.10.1.tar.gz
cd nginx-1.10.1
```

Командой `nano conf.sh` создаем командный файл:
```bash
./configure --sbin-path=/usr/local/sbin \
--conf-path=/etc/nginx/nginx.conf \
--error-log-path=/var/log/nginx/error.log \
--http-log-path=/var/log/nginx/access.log \
--pid-path=/var/run/nginx.pid \
--user=www-data \
--group=www-data \
--with-http_gzip_static_module \
--with-http_realip_module \
--with-http_mp4_module \
--with-http_flv_module \
--with-http_dav_module \
--with-http_secure_link_module \
```
Сохраняем файл `Ctrl+O` и `Enter`, а затем выходим из редактора `Ctrl+X`.

В этот же файл можно добавить дополнительные модули, если мы хотим сборку с ними. Например, на такой маленькой машинке как Sapberry pi пригодился бы модуль поддержки WebDAV `--add-module=/root/nginx/nginx-webdav-ext/` (естественно, его перед сборкой тоже надо будет скачать). Но для конкретного проекта в этом нет необходимости.

Для того чтобы командный `conf.sh` файл  можно было запустить устанавливаем соответствующие права, а за тем запускаем его:
```bash
chmod +rwx conf.sh
sudo bash conf.sh
```

Если все прошло хорошо, то можно приступать с компиляции, и установить то что получится.
```bash
sudo make
sudo make install
```

nginx установлен. Если же поле `make` ругается на недостаток каких-то модулей в Linux, то придется разобраться, установить необходимое. Если же все прошло гладко (как у меня), то нужно проверить, что веб-сервер запускается:
```bash
sudo service nginx start
```
Убедиться что nginx работает корректно можно набрав _арес.нашего.сервера_ или его _ip_ в браузере. Должна отображаться страница: ***`Welcome to nginx on Debian!`***

Установка с помощью `sudo art-get install nginx` уже произвела все необходимые настройки автозапуска. Убедиться, что они работают можно перегрузив компьютер:
```bash
sudo reboot
```

Убеждаемся, что nginx запущен, снова набрав _арес.нашего.сервера_ или его _ip_ в браузере. Если мы устанавливали версию из исходников, то убедиться, что работает именно она можно набрав команду:
```bash
nginx -v
```
Получим сообщение:
> nginx version: nginx/1.10.1

Место на нашем Raspbery pi не резиновое, и теперь можем благополучно удалить папку в которой происходила сборка nginx и архив с исходниками:
```bash
rm -R $HOME/nginx-1.10.1
rm $HOME/nginx-1.10.1.tar.gz
```

### Настройка nginx для нашего проекта

Теперь надо настроить наш сайта в nginx. Создаем каталоги для хранения логов, конфигурационных файлов и сокета.
```bash
mkdir -p $HOME/[адрес сайта]/logs
mkdir -p $HOME/[адрес сайта]/config
mkdir -p $HOME/[адрес сайта]/socket
```

Создаём конфигурационный файл `[адрес_сайта]_nginx.conf`:
```bash
nano $HOME/[адрес сайта]/conf/[адрес_сайта]_nginx.conf
```
Со следующим содержанием:
```
#                      _          ___
#                     | |        |__ \
#    __  __  ___ _   _| |__   ___   ) |  _ __ _   _
#    \ \/ / / __| | | | '_ \ / _ \ / /  | '__| | | |
#     >  < | (__| |_| | |_) |  __// /_ _| |  | |_| |
#    /_/\_(_)___|\__,_|_.__/ \___|____(_)_|   \__,_|
# Конфикурационный файл nginx для сайта [адрес_сайта] ([адрес_сайта]_nginx.conf)

# не забываем изменять _user_ на имя нашего пользователя, которому будет разрешено деплоить и перезапускать сайт.

# Описываем апстрим-потоки которые должен подключить Nginx
# Для каждого сайта надо настроить свой поток, со своим уникальным именем.
# Если будете настраивать несколько python (django) сайтов - измените название upstream

upstream [адрес_сайта]_django {
    # расположение файла Unix-сокет для взаимодействие с uwsgi
    server unix:///home/[user]/[адрес_сайта]/socket/[адрес_сайта].sock;
    # также можно использовать веб-сокет (порт) для взаимодействие с uwsgi. Но это медленнее
    # server 127.0.0.1:12012; # для взаимодействия с uwsgi через веб-порт
}

# конфигурируем сервер
server {
    listen      80;                  # порт на котором будет доступен наш сайт
    server_name x.cube2.ru;    # доменное имя сайта
    charset     utf-8;               # подировка по умолчанию
    access_log  /home/[user]/[адрес_сайта]/logs/[адрес_сайта]_access.log;    # логи с доступом
    error_log   /home/[user]/[адрес_сайта]/logs/[адрес_сайта]_error.log;     # логи с ошибками
    client_max_body_size 32M; # максимальный объем файла для загрузки на сайт (max upload size)

    location /media       { alias /home/[user]/[адрес_сайта]/public/media; }   # Расположение media-файлов Django
    location /static      { alias /home/[user]/[адрес_сайта]/public/static; }  # Расположение static-файлов Django
    location /robots.txt  { root  /home/[user]/[адрес_сайта]/public; }   # Расположение robots.txt
    location /author.txt  { root  /home/[user]/[адрес_сайта]/public; }   # Расположение author.txt
    location /favicon.ico { root  /home/[user]/[адрес_сайта]/public; }   # Расположение favicon
    location /favicon.gif { root  /home/[user]/[адрес_сайта]/public; }   # Расположение favicon
    location /favicon.png { root  /home/[user]/[адрес_сайта]/public; }   # Расположение favicon
    location ~ \.(xml|html|htm)$  { root  /home/[user]/[адрес_сайта]/public; } # Расположение *.xml и *.html
    location / {
        uwsgi_pass           [адрес_сайта]_django;       # upstream обрабатывающий обращений
        include              uwsgi_params;               # конфигурационный файл uwsgi;
        uwsgi_read_timeout   1800;     # некоторые запросы на Raspbery pi очень долго обрабатываются.
        uwsgi_send_timeout   200;      # на всякий случай время записи в сокет
        }
    }
```
Проверьте все скобочки и точки с запятой... Они могут создать много неприятностей. Сохраняем файл `Ctrl+O` и `Enter`, а затем выходим из редактора nano с помощью `Ctrl+X`.

Эта конфигурация сообщает nginx, каким образом он отдает данные при обращении к **[адрес сайта]** по порту **80**. Так, при обращении статическим и загруженным пользователем файлам, он отдает их из соответствующих каталогов, а остальные запросы будут перенаправляется в Django-приложение через апстрим `[адрес_сайта]_django`, который работает через юниксовкий файл-сокет `unix:///home/[user]/[адрес сайта]/socket/[адрес_сайта].sock`.

По умолчанию файл конфигурации uWSGI находится в папке _/etc/nginx/uwsgi_params_ и мы используем именно его, но при желании мы может это переопределит. К слову сказать, в ранних версиях nginx файл _uwsgi_params_ в поставку не входил. Проверьте есть ли он у вас, и при необходимости [загрузите из git-репозитория разработчиков nginx](https://github.com/nginx/nginx/blob/master/conf/uwsgi_params).

Чтобы nginx подключил наш новый файл конфигурации сайта нужно добавьте ссылку на него в каталог `/etc/nginx/sites-enabled/`:
```bash
sudo ln -s $HOME/[адрес сайта]/config/[адрес_сайта]_nginx.conf /etc/nginx/sites-enabled/
```

Теперь нужно перезагрузить nginx
```bash
sudo service nginx restart
```

В результате статические файлы теперь будут отдаваться в браузер. Так вызвав `http://[адрес сайта]/static/img/favicon.ico` получим картинку favicon.ico:

![Что показываю по http://[адрес сайта]/static/img/favicon.ico](https://raw.githubusercontent.com/erjemin/Xphorism/master/public/static/img/favicon.ico "favicon.ico")

nginx работает. То что все в нем корректно проверяем командой: `systemctl status nginx.service`

```
? nginx.service - A high performance web server and a reverse proxy server
   Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
   Active: active (running) since Чт 2017-11-02 19:41:19 MSK; 4min 27s ago
  Process: 20175 ExecStop=/sbin/start-stop-daemon --quiet --stop --retry QUIT/5 --pidfile /run/nginx.pid (code=exited, status=0/SUCCESS)
  Process: 20187 ExecStart=/usr/sbin/nginx -g daemon on; master_process on; (code=exited, status=0/SUCCESS)
  Process: 20182 ExecStartPre=/usr/sbin/nginx -t -q -g daemon on; master_process on; (code=exited, status=0/SUCCESS)
 Main PID: 20190 (nginx)
   Memory: 2.3M
      CPU: 265ms
      CGroup: /system.slice/nginx.service
           ??20190 nginx: master process /usr/sbin/nginx -g daemon on; master_process on
           ??20191 nginx: worker process
           ??20192 nginx: worker process
           ??20193 nginx: worker process
           ??20194 nginx: worker process
```

---------------------

# Установка и настройка uWSGI

Если при настройке виртуального окружения нам не потребвался пакет разработчика пакет **python-dev**, то теперь нам обязательно нужно его установить:
```bash
sudo apt-get install python-dev
```

В nginx (как впрочем и в других веб-серверах) обмен данными с python-приложениями происходит через WSGI (Web Server Gateway Interface). В его основе лежат сокеты (нечто вроде общего блока памяти к которому может обращаться и веб-сервер, и приложение) через которые пробрасываются данные между приложением и сервером. Существуем множество сервисов WSGI -- gunicorn, passenger_wsgi, flup, FastCGI (вот [далеко не полный список WSGI] (http://wsgi.readthedocs.io/en/latest/servers.html) -- и для нашего сервера мы выберем uWSGI. Он достаточно компактен, шустрый и не прожорливый. Для миниатюрного Paspbery pi -- самое то. Можно установить uWSGI в виртуальное окружение, но если мы хотим чтобы и другие Python-сайты нашего сервера могли его использовать, то лучше производить установку на системном уровне:
```bash
sudo apt install uwsgi
```

Теперь создаем файл конфигурации uwsgi для нашего проекта. В нем буду описано какое виртуальное окружение использует проект.
```bash
nano $HOME/[адрес сайта]/config/[адрес сайта]_uwsgi.ini
```
Сожержание этого файла будет примерно таким
```
#                      _          ___
#                     | |        |__ \
#    __  __  ___ _   _| |__   ___   ) |  _ __ _   _
#    \ \/ / / __| | | | '_ \ / _ \ / /  | '__| | | |
#     >  < | (__| |_| | |_) |  __// /_ _| |  | |_| |
#    /_/\_(_)___|\__,_|_.__/ \___|____(_)_|   \__,_|
# [адрес_сайта]_uwsgi.ini -- настройки uWSGI для [адрес сайта]
[uwsgi]

# НАСТРОЙКИ ДЛЯ DJANGO
# Корневая папка проекта (полный путь)
chdir           = /home/[user]/[адрес сайта]/Xphorism
# Django wsgi файл Xphorism/wsgi.py записываем так:
module          = Xphorism.wsgi
# полный путь к виртуальному окружению
home            = /home/[user]/[адрес сайта]/env
# полный путь к файлу сокета
socket          = /home/[user]/[адрес сайта]/socket/[адрес_сайта].sock
# Исходящие сообщения в лог
daemonize       = /home/[user]/[адрес сайта]/logs/[адрес_сайта]_uwsgi.log

# ЗАГАДОЧНЫЕ НАСТРОЙКИ, ПО ИДЕЕ ОНИ НУЖНЫ, НО И БЕЗ НИХ ВСЁ РАБОТАЕТ
# расположение wsgi.py
wsgi-file       = /home/[user]/[адрес сайта]/Xphorism/Xphorism/wsgi.py
# расположение виртуального окружения (как оно работает если этот параметр не указан, не ясно)
virtualenv      = /home/[user]/[адрес сайта]/env
# имя файла при изменении которого происходит авторестарт приложения
# (когда этого параметра нет, то ничего не авторестартится, но с ним все рестартится.
# Cтоит изменить любой Python-исходник проекта, как изменения сразу вступают в силу.
touch-reload    = /home/[user]/[адрес сайта]/logs/[адрес_сайта]_reload.log

#  НАСТРОЙКИ ОБЩИЕ
# быть master-процессом
master          = true
# максимальное количество процессов
processes       = 4
# права доступа к файлу сокета. По умолчанию должно хватать 664. Но каких-то прав не хватает, поэтому 666.
chmod-socket    = 666
# очищать окружение от служебных файлов uwsgi по завершению
vacuum          = true
# количество секунд после которых подвисший процесс будет перезапущен
# Так как некоторе скрипты требуют изрядно времени (особенно полная переиндексация) то ставим значение побольше
harakiri      = 2600
# В общем случае, при некотых значениях harakiri логах uWSGI может вываливаться предупреждение:
# WARNING: you have enabled harakiri without post buffering. Slow upload could be rejected on post-unbuffered webservers
# можно оставить harakiri закомментированным, но нам нужно 900 и на него не ругается. Ругается на 30.

# разрешаем многопоточность
enable-threads  = true
vacuum          = true
thunder-lock    = true
max-requests    = 500

# пользователь и группа пользователей от имени которых запускать uWSGI
# указываем www-data: к этой группе относится nginz, и ранее мы включили в эту группу нашего [user]
uid             = www-data
gid             = www-data

print           = ---------------- Запущен uWSGI для [адрес сайта] ----------------
```

Запускаем uwsgi с нашим конфигом:
```bash
uwsgi --ini /home/[user]/[адрес сайта]/config/[адрес_сайта]_uwsgi.ini
```

### Проверка корректности работы uWSGI и что делать если что-то не так

Если ничего не заработало, то проверяем файл логов `/home/[user]/[адрес сайта]/logs/[адрес_сайта]_uwsgi.log`. Просматриваем лог с помощью команды:
```bash
cat /home/[user]/[адрес сайта]/logs/[адрес_сайта]_uwsgi.log
```

В нем отображаются все сообщения инициализации uwsgi. Внизу находятся самые свежие записи. Записи выводятся в несколько строк, и каждая запись начинается со строки: `*** Starting uWSGI`.

В случае ошибок при запуске -- разбираемся и курим мануалы.

Ошибки могут быть вот такие:
> *** WARNING: you are running uWSGI as root !!! (use the --uid flag) ***

Значит мы запустили uWSGI от имени администратора. А надо от имени текущего пользователя [user].



> *** WARNING: you are running uWSGI without its master process manager ***

Но если вы все сделали правильно в соответствии с настоящей инструкцией, критических проблем возникнуть не должно. Тем не менее просмотреть логи uwsqi все равно полезно. Например, кроме предупреждения ***WARNING: you have enabled harakiri without post buffering. Slow upload could be rejected on post-unbuffered webservers*** о котором сказано в комментариях к `[адрес_сайта]_uwsgi.ini`  нас могут беспокоить сообщения: ***!!! no internal routing support, rebuild with pcre support !!!*** Это означает, что у нас установлен однопоточный uWSGI при многопоточном nginx и процессоре. Можно установить в `[адрес_сайта]_uwsgi.ini` инструкцию использования однопоточности `enable-threads = false`, но лучше собрать многопоточный uWSGI с pcre.

Для этого нам понадобятся пакеты разработчиков.
```bash
sudo apt-get install libpcre3 libpcre3-dev
```

Нам нужно удалить неправильный uWSGI и установить новый, дав указание пересобрать его:
```
sudo pip uninstall uwsgi
sudo apt-get purge uwsgi
sudo pip install uwsgi -I
```

В конце установщик выдаст:
```
    ################# uWSGI configuration #################

    pcre = True
    kernel = Linux
    malloc = libc
    execinfo = False
    ifaddrs = True
    ssl = False
    zlib = True
    locking = pthread_mutex
    plugin_dir = .
    timer = timerfd
    yaml = embedded
    json = False
    filemonitor = inotify
    routing = True
    debug = False
    ucontext = False
    capabilities = False
    xml = expat
    event = epoll

    ############## end of uWSGI configuration #############
```

Как видим `pcre = True`, значит у нас теперь многопоточный uWSGI.

Еще раз запускаем uWSGI с нашим конфигом:
```bash
sudo uwsgi --ini /home/[user]/[адрес сайта]/config/[адрес_сайта]_uwsgi.ini
```
Открываем в браузере сайт _http://[адрес сайта]_. И если он открывается с ошибкой 502, то смотрим лог ошибок nginx:
```bash
cat /home/[user]/[адрес сайта]/logs/[адрес_сайта]_error.log
```

#### Виды ошибок:
##### Первая:
> 2017/11/04 01:05:45 [crit] 26651#0: *2 connect() to unix:///home/[user]/[адрес сайта]/sock/[адрес_сайта].sock failed (13: Permission denied) while connecting to upstream, client: 192.168.1.1, server: [адрес сайта], request: "GET / HTTP/1.1", upstream: "uwsgi://unix:///home/[user]/[адрес сайта]/sock/[адрес_сайта].sock:", host: "[адрес сайта]"

Означает, что не хватает прав на доступ к сокету. По идее в нашем `[адрес_сайта]_uwsgi.ini` должно хватать `chmod-socket = 664`, но непонятно почему не хватает. Меняем на `chmod-socket = 666`.

#### Вторая:
> 2017/11/04 01:36:34 [error] 26844#0: *7 upstream prematurely closed connection while reading response header from upstream, client: 192.168.1.1, server: [адрес сайта], request: "GET / HTTP/1.1", upstream: "uwsgi://unix:///home/[user]/[адрес сайта]/sock/[адрес_сайта].sock:", host: "[адрес сайта]"

Означает, что ошибка на стороне python-скриптов нашего Django-приложения. Очевидно мы что-то сделали неправильно при установке виртуально окружения, развертывании проекта и его настройке и проверки. Надо перепроверить развертывание и возможно повторить его.

#### Третья:
> 2017/11/04 20:18:10 [error] 649#0: *9 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 192.168.1.1, server: [адрес сайта], request: "POST /recheck HTTP/1.1", upstream: "uwsgi://unix:///home/eserg/[адрес сайта]/sock/[адрес_сайта].sock", host: "[адрес сайта]", referrer: "http://[адрес сайта]/"

Означает, что или значение `uwsgi_read_timeout` в нашем conf-файле nginx не достаточно, или параметр `harakiri` в ini-файле uWSGI маловат. У меня на всякий случай вообще выставлено в обоих случаях 3600 (один час), и это не предел. Подробнее про опции и настройки таймаутов nginx читайте документацию [тут](http://nginx.org/ru/docs/http/ngx_http_uwsgi_module.html#uwsgi_read_timeout) и [тут](http://nginx.org/ru/docs/http/ngx_http_core_module.html#reset_timedout_connection).

Хотя, возможно, просто ваш скрипт завис.

### Устанавливаем Emperor-режим uWSGI

Если сервер обслуживает несколько проектов, каждый из которых использует uWSGI, то нужно использовать режим Emperor. В этом режиме uWSGI просматривает папку с конфигурационными файлами и для каждого файла запускает отдельный подчиненный процесс (вассал).

Особенно удобно Emperor-режиме то, что если один из конфигурационных файлов будет изменен, uWSGI перезапустит соответствующего вассала.

Создаем системную папку для конфигурационных файлов:
```bash
sudo mkdir /etc/uwsgi
sudo mkdir /etc/uwsgi/vassals
```

Создаем в ней симлинк на наш ini-файл uWSGI:
```bash
sudo ln -s /home/[user]/[адрес сайта]/config/[адрес_сайта]_uwsgi.ini /etc/uwsgi/vassals/
```

Теперь, можно запустить uWSGI в режиме Emperor, указав с помощью ключа `--emperor` папку с симлимками на конфигурационное ini-файлы, и с помощью `--uid` и `--gid` пользователя и группу от имени которых должен работать uWSGI:
```bash
sudo uwsgi --emperor /etc/uwsgi/vassals --uid [user] --gid [user]
```

Чтобы  uWSGI запускался автоматически при каждой загрузке нашего Raspberri pi необходимо изменить файл `/etc/rc.local`. Открываем его на редактирование:
```bash
sudo nano /etc/rc.local
```

И перед самой последней строчкой `exit 0` вставляем в него команду запуска uWSGI. Должно получиться примерно так:
```bash
/usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals --uid [user] --gid [user]
exit 0
```
Теперь можно перезагрузить наш сервер и убедиться, что uWSGI запустился и наш сайт `[адрес_сайта]` открывается в браузере.

# Перезапуск

### Перезапуск nginx

Если меняем настройки nginx то делаем так:
```bash
sudo nginx -s reload
```
### Перезапуск Django в связке uWSGI

Если меняем скрипты Django с настройкой `touch-reload` в `uwsgi.ini` все само перезапускается. Можно сделать даже небольшой скрипт. который будет менять файл `/home/[user]/[адрес сайта]/logs/[адрес_сайта]_reload.log`и вести что-то вроде лог-файла  А если не перезапустится, то делаем так:
```bash
sudo /usr/local/bin/uwsgi --uid [user] -touch-reload
```

# Тюнинг ubuntu под Raspberry pi

В случае с развертыванием на Raspbian Linux все работает довольно шустро. Но для Ubuntu 16.06 LTE для Raspberry pi все тормозит. Особенно в базе данных.

## Тюнингуем лимиты файловой системы

Есть гипотеза, что это из-за ограничений на число одновременно открытых файлов в системе. MySQL не может изменить свои настройки выше системных и потому надо повысить системные лимиты, изменив настройки в `/etc/security/limits.conf`. Отредактируем его:

Открываем на редактирование:
```bash
sudo nano /etc/security/limits.conf
```

Найдём в нем блок куда вносятся лимиты на файлы, ftp и тому подобное (обычно закомментировано) и вставить вот такие настройки (я пока поставил в тестовом режиме, возможно цифры великоваты, но значение по умолчанию -- 1024 -- вообще остстой):
```cfg
*               hard    nofile          65536
*               soft    nofile          16384
root            hard    nofile          65536
root            soft    nofile          16384
```

Что бы не перегружать систему, а сразу задействовать настройки нужно дать команды:
```
ulimit -Hn 65536
ulimit -Sn 16384
```

## Тюнингуем MySQL

Тема сложная. Развертывание бекапа в котором есть много ключей для сортировки может стать мукой. Мукой многочасовой, так как вообще непонятно что происходит. Пока я поставил вот такие настройки:
```
key_buffer_size         = 32M
max_allowed_packet      = 32M
thread_stack            = 1024K
thread_cache_size       = 64

# innodb_open_files   = 16384
# open_files_limit    = 4096
# table_open_cache    = 1014
# key_buffer_size         = 64M
# max_connections        = 32
# table_cache            = 256
# thread_concurrency     = 40
# query_cache_limit       = 1M
# query_cache_size        = 16M

```

------

