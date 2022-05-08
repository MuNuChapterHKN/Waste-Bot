# Waste-Bot
Il Bot è interamente scritto in Python (Python3) e la principale libreria utilizzata per interfacciarsi con [Telegram Bot API](https://core.telegram.org/bots/api) è [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot).

# Db
Per collegarsi al db è utilizzato l'orm SqlAlchemy [docs](https://docs.sqlalchemy.org/en/14/).
Deve essere presente un db postgres sulla macchina locale. La connection string (che specifica url, utente, password e db) va salvata nella variabile d'ambiente `DATABASE_URL`. Per osservare le query sql generate è possible attivare la modalità echo di SQLAlchemy settando la variabile d'ambiente `DATABASE_LOGGING` a 'True'.

### Bot token
Per il corretto funzionamento è necessario richiedere un Token tramite [BotFather](https://t.me/BotFather) e impostarlo come variabile d'ambiente tramite il comando `export`, ad esempio:
```
export TOKEN='3506992133:AGEf-GZo4uE-BhXaQ6J8T1TtlPBEpOEl2yI'
```

### Senza Poetry
Usare poetry è opzionale. Alternativamente si possono installare le dependency con
```bash
pip install -r requirements.txt
```

### Poetry
Per installare le dependencies del progetto è necessario installare sul sistema il tool [poetry](https://python-poetry.org), e dopo aver clonato il progetto eseguire `poetry install` per installare le dependencies.
Per far partire il bot (dopo aver settato le env. var. necessarie) si può utilizzare alternativamente
```bash
poetry shell
# --- exporting environment variables
python bot.py
```
oppure
```bash
# --- export environment variables
poetry run python bot.py
```
