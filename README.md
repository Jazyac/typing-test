# Typing Speed Test Application

A web-based typing speed test application built with Django that features three distinct typing games to evaluate typing speed and accuracy.

## Features

- Three different typing test modes:
  - Random Words: Practice with common words
  - Paragraph: Test with complete paragraphs
  - Code Snippet: Practice typing code
- Real-time WPM (Words Per Minute) calculation
- Accuracy tracking
- Error counting
- User authentication and progress tracking
- Personal statistics and history
- Responsive design

## Requirements

- Python 3.8+
- Django 5.1+
- django-crispy-forms
- crispy-bootstrap5
- python-decouple

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd typing_speed_test
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Load initial data:
```bash
python manage.py loaddata core/fixtures/initial_data.json
```

6. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## Usage

1. Register a new account or login if you already have one
2. Choose a typing test mode from the home page
3. Click "Start Test" to begin
4. Type the displayed text as accurately and quickly as possible
5. View your results and statistics in your profile

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 