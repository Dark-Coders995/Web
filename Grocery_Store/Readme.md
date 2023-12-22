# Flask Project Setup and Virtual Environment

This readme file provides step-by-step instructions on how to set up and run a Flask project using a virtual environment and installing packages from the `requirements.txt` file.

## Prerequisites

Before you begin, make sure you have the following installed:

- Python: Make sure you have Python installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).

## Setting Up the Virtual Environment

1. **Create a Project Directory**: Start by creating a directory for your Flask project. Open a terminal and navigate to the directory where you want to create the project folder. Use the following command to create the directory:

    ```bash
    mkdir my_flask_project
    cd my_flask_project
    ```

2. **Create a Virtual Environment**: Inside your project directory, create a virtual environment. Virtual environments help isolate project-specific dependencies from your global Python environment. Run the following command:

    ```bash
    python -m venv venv
    ```

3. **Activate the Virtual Environment**: Activate the virtual environment using the appropriate command for your operating system:

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```

## Installing Packages from `requirements.txt`

1. **Clone or Create Your Flask Project**: You can either clone an existing Flask project from a repository or create your own Flask project files in the current directory.

2. **Install Packages**: Inside your activated virtual environment, you can now install the required packages listed in the `requirements.txt` file. Assuming the `requirements.txt` file is located in your project directory, use the following command:

    ```bash
    pip install -r requirements.txt
    ```

    This command will install all the packages listed in the `requirements.txt` file.

## Running the Flask Application

1. **Set Flask App**: In your terminal, navigate to the root directory of your Flask project where your main Flask application file (e.g., `app.py`) is located.

2. **Run the Flask App**: Use the following command to run your Flask application:

    ```bash
    flask run
    ```

    This command will start the Flask development server, and your app will be accessible at `http://localhost:5000`.

3. **Access Your App**: Open a web browser and navigate to `http://localhost:5000` to see your Flask application in action.

4. **Stopping the App**: To stop the Flask development server, simply press `Ctrl+C` in the terminal where the server is running.

## Deactivating the Virtual Environment

1. **Deactivate Virtual Environment**: Once you're done working on your Flask project, you can deactivate the virtual environment by running the following command in the terminal:

   ```bash
   deactivate
   ```

This concludes the setup and running instructions for your Flask project using a virtual environment and installing packages from the `requirements.txt` file. Happy Flask development!
