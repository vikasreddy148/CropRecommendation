# Quick Start Guide

## Running the Development Server

### Option 1: Using Virtual Environment (Recommended)

```bash
# Navigate to project directory
cd /Users/vikasreddy/CropRecommendation

# Activate virtual environment
source venv/bin/activate

# Run the server
python manage.py runserver
```

### Option 2: Using python3 directly

```bash
# Navigate to project directory
cd /Users/vikasreddy/CropRecommendation

# Activate virtual environment
source venv/bin/activate

# Run the server (python3 should work after activating venv)
python3 manage.py runserver
```

### Option 3: Create an alias (for convenience)

Add this to your `~/.zshrc` file:
```bash
alias activate-crop="cd /Users/vikasreddy/CropRecommendation && source venv/bin/activate"
```

Then you can simply run:
```bash
activate-crop
python manage.py runserver
```

## Accessing the Application

Once the server is running, access the application at:
- **Home**: http://127.0.0.1:8000/
- **Landing Page**: http://127.0.0.1:8000/landing/
- **Dashboard**: http://127.0.0.1:8000/dashboard/ (requires login)
- **Login**: http://127.0.0.1:8000/login/
- **Register**: http://127.0.0.1:8000/register/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## Common Commands

### Activate Virtual Environment
```bash
source venv/bin/activate
```

### Run Server
```bash
python manage.py runserver
```

### Create Superuser (for admin access)
```bash
python manage.py createsuperuser
```

### Run Migrations
```bash
python manage.py migrate
```

### Collect Static Files
```bash
python manage.py collectstatic
```

### Check for Errors
```bash
python manage.py check
```

### Deactivate Virtual Environment
```bash
deactivate
```

## Troubleshooting

### If `python` command not found:
- Use `python3` instead
- Or activate the virtual environment first: `source venv/bin/activate`

### If virtual environment not found:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### If port 8000 is already in use:
```bash
python manage.py runserver 8001
```

