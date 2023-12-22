# Project Setup Instructions

## Backend Setup

### Terminal 1

1. Open a terminal.
2. Navigate to the `backend` directory.
   ```bash
   cd backend
   ```
3. Create a virtual environment.
   ```bash
   python3 -m venv venv
   ```
4. Activate the virtual environment.
   ```bash
   source venv/bin/activate
   ```
5. Install required Python packages.
   ```bash
   pip3 install -r requirements.txt
   ```

### Terminal 2

1. Open a new terminal.
2. Start the Redis server.
   ```bash
   redis-server
   ```

### Terminal 3

1. Open another terminal.
2. Navigate to the `backend` directory.
   ```bash
   cd backend
   ```
3. Activate the virtual environment.
   ```bash
   source venv/bin/activate
   ```
4. Start Celery worker.
   ```bash
   python3 -m celery -A app.celery worker -l info
   ```

### Terminal 4

1. Open a new terminal.
2. Navigate to the `backend` directory.
   ```bash
   cd backend
   ```
3. Activate the virtual environment.
   ```bash
   source venv/bin/activate
   ```
4. Start Celery beat.
   ```bash
   python3 -m python3 -m celery -A app.celery beat -l info
   ```

### Terminal 5

1. Open another terminal.
2. Start MailHog for email testing.
   ```bash
   mailhog
   ```

## Frontend Setup

### Terminal 6

1. Open a new terminal.
2. Navigate to the `frontend` directory.
   ```bash
   cd frontend
   ```
3. Run the development server.
   ```bash
   npm run dev
   ```

Now, your backend and frontend environments should be set up and running. Adjust the instructions based on your project's specific structure and requirements.
