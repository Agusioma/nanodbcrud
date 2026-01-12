## PesaPal Developer Challenge 2026

### Part 2. The CRUD app - Summary of its working

This is a simple Django app that feeds of nanoDB. It simulates a gaming leaderboard where the players are ranked according to the score. The UI is made using bootstrap. You can try it out by following the steps below.

#### 1. Cloning the repo

```bash
git clone https://github.com/Agusioma/nanodbcrud.git
cd nanodbcrud
```

#### 2. Activating the virtual environment and installing Django dependency

```bash
python -m venv venv                                         
source venv/bin/activate
pip install django
```

#### 3. Starting the app

Run the command below:

```bash
python manage.py runserver
```

Head on to the browser at `127.0.0.1:8000` where you will be presented with an interface where you can enter the data, view, update, and delete it.

![](2026-01-12_15-38.png)
