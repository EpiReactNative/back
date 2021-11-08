# Epigram back

## Installation

Create virtual environment
```sh
py -m venv env
```

Activate virtual environment
```sh
.\env\Scripts\Activate.ps1 # PowerShell
source env/Scripts/activate # Linux
```

Install required python packages
```sh
pip install -r requirements.txt
```

Run server
```sh
py manage.py runserver
```

Migration (after model modification)
```sh
py manage.py makemigrations
py manage.py migrate
```

Swagger url [http://localhost:8000/api/swagger](http://localhost:8000/api/swagger)
