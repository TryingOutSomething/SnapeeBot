The required software and tools before running the Telegram bot:

1. Domain name
2. MySQL database
3. Python 3.7
4. Google Sheet credentials

The credentials and configuration files are stored in a dotenv file. Create a fresh dotenv file by copying
the `.env_sample` file and renaming it to `.env`.

The structure of the dotenv file:

```
# development or production.
PYTHON_ENV= 

# The bot's token issued by BotFather on Telegram
TELEGRAM_BOT_TOKEN=

# Domain name for the bot in production mode
WEBHOOK_BASE_URL=

# Port to start the bot server
SERVER_PORT=

# Telegram user ID for users to feedback any issues
SNAPEE_ASSISTANT_ID=

# The database connection credentials
SQL_CONNECTION_USERNAME=demo
SQL_CONNECTION_PASSWORD=password
SQL_CONNECTION_HOST=localhost
SQL_CONNECTION_PORT=3306

# The path to Google sheet credentials
GOOGLE_SHEET_CREDENTIAL_PATH=

# The google sheet name and URL
TARGET_GOOGLE_SHEET_URL=
TARGET_GOOGLE_SHEET_NAME=
```

#### Domain name:

Firstly, the bot requires a domain name because it runs with the webhook method instead of polling. The bot runs on
polling mode during development and webhook mode during production.

To switch between development and production profiles, edit the `PYTHON_ENV` variable in the dotenv file.

```
PYTHON_ENV= # development or production. 
WEBHOOK_BASE_URL= # Domain name for the bot in production mode
SERVER_PORT= # Port to start the bot server behind a reverse proxy like NGINX
```

#### Database:

The bot server communicates with a MariaDB database. There are two methods to set up the database, you can use your own
hosted database or create a docker container for the database.

The sql schema is located in `docker_configs/db/init.sql`.

To create a docker image and container, run the command `docker compose up -d` in the root of the project. The database
schema and sample data is populated immediately.

To change the mapping of volumes for the database, open the `docker-compose.yaml` file and edit the `volumes` entry:

```yaml
volumes:
    - "D:\\MySQL_data:/var/lib/mysql" # maps physical device volume to docker's volume
```

To start the database in docker, run:

```
dokcer compose up -d
```

#### Google Sheet:

The bot utilises the package `Gspread`, a Python package to communicate with Google Sheets. The Google Sheet contains
the ID of Telegram users to broadcast messages.

To set up the connection, follow the guide
from [gspread documentation to get the required JSON credentials](https://docs.gspread.org/en/latest/oauth2.html)

Rename the credentials file to `client_secret.json` and place it in the `assets/bot_related` directory or anywhere you
like.

Add the path of the credentials file to the dotenv file:

```
GOOGLE_SHEET_CREDENTIAL_PATH=./assets/bot_related/client_secret.json # or the path that you placed the credentials in
```

Create a Google Sheet and share the file with the `client_email` address in the `client_secrets.json` file. Add the
Google Sheet URL and the sheet name to the dotenv file:

```
TARGET_GOOGLE_SHEET_URL=# GOOGLE SHEET URL
TARGET_GOOGLE_SHEET_NAME=# SHEET NAME
```

#### Python:

The bot server was developed using Python 3.7. To set up the bot server:

Install the required files using

```
pip install -r requirements.txt
```

If pip command does not work

```
python3 -m pip install
```

To start the server

```
python3 Bot.py
```