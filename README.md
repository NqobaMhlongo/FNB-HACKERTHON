# Path2Work — Skills Passport & Work-Readiness Platform

Path2Work is a Flask web application designed to help candidates demonstrate their work readiness through a skills passport, assessments, and evidence of practical skills. Employers can review candidate profiles and filter candidates using pathway, trust level, and readiness score.

## Features

- Candidate registration and login
- Candidate dashboard and skills passport
- Work-proof / assessment workflow
- Verification service and readiness scoring
- Employer dashboard with candidate filters
- SQLite database for local development
- Seed script that creates demo accounts and sample data

## Requirements

- Python 3.10 or newer recommended
- `pip` (Python package installer)
- Windows, macOS, or Linux

The commands below use Windows PowerShell. If your project specifies versions in `requirements.txt`, install those versions instead.

## Setup on Windows

### 1. Download or clone the project

If the project is hosted on GitHub, clone it with:

```powershell
git clone https://github.com/NqobaMhlongo/FNB-HACKERTHON.git
cd FNB-HACKERTHON
```

If you already have the project folder, open that folder in VS Code and open **Terminal → New Terminal**. Change to the project directory if needed:

```powershell
cd "C:\dev\path2work"
```

### 2. Create and activate a virtual environment

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use the environment's Python directly without activating it:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
```

### 3. Install dependencies

First check whether the project includes `requirements.txt`:

```powershell
Get-ChildItem
```

If it exists, run:

```powershell
python -m pip install -r requirements.txt
```

If there is no `requirements.txt`, install the packages used by the current project:

```powershell
python -m pip install Flask Flask-SQLAlchemy Werkzeug
```

### 4. Create / seed the local database

Run the seed script from the project root:

```powershell
python seed.py
```

The seed script should print a success message and list the demo accounts. Running it may reset or recreate sample data depending on how `seed.py` is implemented. Do not run it against a database containing data you need to preserve unless you have checked the script first.

The current demo password reported by the seed script is `password123` for the listed demo accounts.

### 5. Start the application

```powershell
python run.py
```

When Flask starts, open this URL in your browser:

**http://127.0.0.1:5000**

To access it from another device on the same local network, use your computer's current local IP address and port `5000` (for example, `http://10.0.0.10:5000`). The IP address can change. Allow access through Windows Firewall only on a trusted network.

Stop the development server by returning to the terminal and pressing **Ctrl+C**.

## Demo accounts

The seed script currently reports these accounts:

| Role | Email | Password |
|---|---|---|
| Verified candidate | `thabo.nkosi@uct.ac.za` | `password123` |
| New candidate | `lerato.mokoena@tut.ac.za` | `password123` |
| Employer | `talent@paystack-sa.co.za` | `password123` |

These are development/demo credentials only. Do not use these passwords for real accounts or deploy the app with demo credentials enabled.

## Common issues

### `git status` says “not a git repository”

The project folder has not been initialized as a Git repository, or the terminal is in the wrong folder. From the project root, run:

```powershell
git init
git status
```

If you intend to publish this project to GitHub, check the remote before adding it:

```powershell
git remote -v
```

### `ModuleNotFoundError`

Make sure the virtual environment is active, then install dependencies:

```powershell
python -m pip install -r requirements.txt
```

If there is no `requirements.txt`, install Flask, Flask-SQLAlchemy, and Werkzeug as described above.

### Database file is locked / cannot be zipped

Stop the running Flask server with **Ctrl+C** before copying or compressing the SQLite database. Do not include the local database in Git unless the project specifically needs a sanitized demo database. The seed script is the intended way to create demo data.

### Port 5000 is already in use

Stop the other Flask process or configure the application to use a different port if the project supports it.

### Login or demo data is missing

From the project root, run:

```powershell
python seed.py
```

Check the seed script before rerunning it if you need to preserve existing local data.

## Project structure

The current project layout includes:

```text
path2work/
├── app/
│   ├── routes/
│   ├── services/
│   ├── templates/
│   ├── __init__.py
│   ├── models.py
│   └── config.py
├── requirements.txt
├── run.py
├── seed.py
└── path2work.db        # Local SQLite database; usually not committed
```

The exact files may differ as the project evolves.

## Development notes

- `run.py` starts the Flask development server. It is intended for local development, not production hosting.
- `seed.py` creates demo data for testing.
- Keep secrets and environment-specific configuration out of source control.
- Avoid committing `.venv/`, `__pycache__/`, `.env`, local database files, and other generated artifacts.
- If the app uses a Flask secret key in `app/config.py`, replace any development value with a secure environment-based value before deployment.

## License

Add the license required by your project or hackathon before distributing the application.
