# Project Setup

This README provides a step-by-step guide to set up and run the project locally.

## Prerequisites

- Python 3.x
- Redis
- MailHog

## Installation

1. Create a virtual environment:

    ```
    python3 -m venv venv
    ```

2. Install the required packages:

    ```
    pip install -r requirements.txt
    ```

## Running the Application

Open separate terminals for each of the following commands:

### Terminal 1: Start Redis Server

Start the Redis server:

```
redis-server
```

### Terminal 2: Start MailHog

Start MailHog for email testing:

```
mailhog
```

### Terminal 3: Run the Application

Run the main application:

```
python3 app.py
```

### Terminal 4: Start Celery Worker

Start the Celery worker:

```
celery -A app.celery worker -l info
```

### Terminal 5: Start Celery Beat

Start the Celery beat scheduler with a max interval of 2 seconds:

```
celery -A app.celery beat --max-interval 2 -l info
```

The application is now set up and running locally. Access it through your browser or use the provided endpoints for testing.