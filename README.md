# TelegramPrintingService

## Overview

This is a telegram bot for handling paid printing service. It has several functions including:

- Handling printinig and scanning orders (namely `tasks`)
- A dialogue interface with keyboards for interacting with user
- A dialogue interface for admin to override the dialogue and several other functions
- Not finished miniORM for storing orders in database (i.e. `database.py`)
  - Not working migrations system for the miniORM
- Not finished payment system via Russian service [YooKassa](https://yookassa.ru/)
- Notification system for stuff (admins) via Shift mechanism

## Contributing

Do not try to contribute to this repository! You'll stuck in understanding this garbage code. Even [ruff](https://github.com/astral-sh/ruff) didn't understand our philosophy, so you don't even try.

## Setup

> [!WARNING]
> Doesn't work on windows because of legacy building of aiohttp in `aiogram 3.0.0b7`. See the [issues](https://github.com/Bomberparty/TelegramPrintingService/issues) if there's something fixed

#### Clone the repo

```shell
git clone https://github.com/Bomberparty/TelegramPrintingService
cd TelegramPrintingService
```

#### Set up the virtual environment

```shell
python3 -m venv .venv
source .venv/bin/activate
```

#### Install dependencies

```shell
pip install -r requirements.txt
```

> [!NOTE]
> If there's any error in the proccess, go to the [issues](https://github.com/Bomberparty/TelegramPrintingService/issues) to see an answer or to contact us for solving a problem

#### Initialize the database

Since the migrations system isn't working as of right now, run following to initialize the database:

```shell
python init_db.py
``` 

#### Configure the bot

Bot uses `ConfigParser` for storing all the configurations. The example configuration is stored in the `settings.ini.example` file. To set up the config, you need to do following:

Create the file from the sample:

```shell
cp settings.ini.example settings.ini
```

To make a minimal setup, disable `YOOMONEY`:

```ini
...
[YOOMONEY]
enable = False
token = YOUR_TOKEN
...
```

Fill in all other fields with your own data. For `admin_nspk_number` use any placeholder 10-digit number. Everything else should be understandable.

#### Run the whole thing

Just run it with the regular python or do whatever you want:
```shell
python bot.py
```