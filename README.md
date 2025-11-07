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

## Setup Instructions

### Prerequisites

- Python 3.10+
- pip
- virtualenv (recommended)

### Installation

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd CropRecommendation
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional for development):
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   OPENWEATHER_API_KEY=your-api-key
   SOIL_GRIDS_API_KEY=your-api-key
   GOOGLE_TRANSLATE_API_KEY=your-api-key
   ```

5. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the application**:
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

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

