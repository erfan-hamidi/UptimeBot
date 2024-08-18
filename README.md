# UptimeBot
UptimeBot is a network management tool built with Django and Django REST framework. It monitors websites, email services, routers, and switches, performing checks every 5 minutes. Notifications are sent via SMS or email for any service disruptions.

![screenshot](/screenshot/Screenshot.png)

## Features

- Monitor website uptime with customizable check intervals.
- Record detailed check results including response time, status code, and headers.
- Trigger immediate checks via the API.
- Get notified when a monitored website goes down.
- Manage monitors, checks, and results via a RESTful API.
- Swagger and ReDoc documentation for easy API exploration.

## Tech Stack

- **Backend:** Django, Django Rest Framework, Celery
- **Task Queue:** Celery with Redis
- **Database:** PostgreSQL (or SQLite for local development)
- **API Documentation:** Swagger (via drf-yasg)

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL (or SQLite for local development)
- Redis (for Celery)
- Virtualenv (optional but recommended)

### Steps

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/uptimebot.git
    cd uptimebot
    ```

2. **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure the database:**

    Update the `DATABASES` setting in `uptimebot/settings.py` to point to your PostgreSQL database. For local development, you can use SQLite aslo can use Postgresql:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / "db.sqlite3",
        }
    }
    ```

5. **Run database migrations:**

    ```bash
    python manage.py migrate
    ```

6. **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

8. **Start Redis (if not already running):**

    ```bash
    redis-server
    ```

9. **Start the Celery worker and Celery Beat scheduler:**

    In separate terminal windows, run:

    ```bash
    celery -A uptimebot worker -l info
    celery -A uptimebot beat -l info
    ```

## Usage

### API Endpoints

- **List Monitors:** `GET /monitor/monitors/`
- **Create Monitor:** `POST /monitor/monitors/`
- **Retrieve Monitor:** `GET /monitor/monitors/{id}/`
- **Update Monitor:** `PUT /monitor/monitors/{id}/`
- **Delete Monitor:** `DELETE /monitor/monitors/{id}/`
- **Perform Check:** `POST /monitor/monitors/{id}/check/`
- **List Checks:** `GET /monitor/checks/`
- **List Check Results:** `GET /monitor/check-results/`

### API Documentation

Access the Swagger UI for interactive API documentation:

- **Swagger UI:** [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
- **ReDoc UI:** [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

### Admin Interface

Access the Django Admin interface:

- **URL:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Credentials:** Use the superuser credentials you created during setup.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for any enhancements, bug fixes, or features you'd like to add.

### Running Tests

To run tests, use:

```bash
python manage.py test
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.
### Explanation of the README

- **Introduction**: Provides an overview of the project and its purpose.
- **Features**: Lists the main functionalities of the service.
- **Tech Stack**: Lists the technologies used in the project.
- **Installation**: Provides step-by-step instructions on how to set up the project locally.
- **Usage**: Explains how to interact with the API and access documentation.
- **Contributing**: Encourages contributions and provides guidelines for contributing.
- **License**: Mentions the project’s licensing.
- **Acknowledgements**: Credits the tools and frameworks used in the project.

This `README.md` is designed to be comprehensive and informative, helping users and developers quickly understand the project and get started.
