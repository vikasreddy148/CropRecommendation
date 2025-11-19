# AI-Driven Crop Recommendation System

A Django-based web application that provides AI-powered, personalized crop recommendations to farmers based on soil properties, weather forecasts, and crop rotation history.

## Features

- **Soil Analysis**: Integration with satellite data (Soil Grids, Bhuvan APIs) and IoT sensors
- **Weather Integration**: Localized weather forecasts
- **Crop Recommendations**: ML-powered suggestions with yield, profit, and sustainability predictions
- **Multilingual Support**: Text-based chat interface in local languages
- **Offline Capability**: Core features work in low-connectivity areas

## Technology Stack

- **Backend**: Django 4.2.7, Django REST Framework
- **Database**: SQLite (development), PostgreSQL (production)
- **ML Framework**: TensorFlow, scikit-learn
- **Task Queue**: Celery + Redis
- **Frontend**: Django Templates + Bootstrap 5

## Project Structure

```
CropRecommendation/
├── apps/
│   ├── users/          # User management
│   ├── farms/          # Farm and field management
│   ├── soil/           # Soil data integration
│   ├── weather/        # Weather data integration
│   ├── recommendations/ # ML recommendation engine
│   ├── chat/           # Chat interface
│   └── translation/    # Translation services
├── crop_recommendation/ # Main project settings
├── static/             # Static files (CSS, JS, images)
├── media/              # User uploads
├── ml_training/        # ML model training scripts
├── templates/          # Base templates
└── tests/              # Test files
```

## Quick Setup

### 🚀 For First-Time Users (Downloaded from GitHub)

**📖 See [QUICK_START.md](QUICK_START.md) for detailed step-by-step instructions for both Mac and Windows.**

### Automated Setup (Recommended)

We provide automated setup scripts to make installation easier:

#### Mac:
```bash
chmod +x setup_mac.sh
./setup_mac.sh
```

#### Windows (Command Prompt):
```cmd
setup_windows.bat
```

#### Windows (PowerShell):
```powershell
.\setup_windows.ps1
```

**Note for Windows PowerShell**: If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Manual Setup

If you prefer to set up manually, follow these steps:

#### Prerequisites

- **Python 3.10 or higher** (download from [python.org](https://www.python.org/downloads/))
- **pip** (usually comes with Python)
- **Git** (optional, for cloning)

#### Installation Steps

1. **Extract the project** (if downloaded as zip) or clone the repository:
   ```bash
   cd CropRecommendation
   ```

2. **Create and activate virtual environment**:
   
   **Mac:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   
   **Windows (Command Prompt):**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```
   
   **Windows (PowerShell):**
   ```powershell
   python -m venv venv
   venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Run migrations** (sets up the database):
   ```bash
   python manage.py migrate
   ```

5. **Create superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files**:
   ```bash
   python manage.py collectstatic
   ```

7. **Run development server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the application**:
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/
   - Landing page: http://127.0.0.1:8000/landing/
   - Dashboard: http://127.0.0.1:8000/dashboard/ (requires login)

### Environment Variables (Optional)

For production or advanced configuration, create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
OPENWEATHER_API_KEY=your-api-key
SOIL_GRIDS_API_KEY=your-api-key
GOOGLE_TRANSLATE_API_KEY=your-api-key
```

## Development

### Running Tests

```bash
python manage.py test
```

### Collecting Static Files

```bash
python manage.py collectstatic
```

## API Endpoints

API documentation will be available once the API views are implemented.

## Contributing

This project is in active development. Please refer to the PROJECT_PLAN.md for detailed implementation phases.

## License

[Add your license here]

## Contact

[Add contact information here]

