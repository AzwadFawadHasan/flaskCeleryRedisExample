# FlaskCeleryRedisExample

This repository demonstrates a simple way to perform asynchronous tasks using Flask, Celery, and Redis.

## Introduction

FlaskCeleryRedisExample provides a basic setup for implementing a task queue with Flask and Celery, using Redis as the broker. This is an ideal starting point for Python developers looking to integrate asynchronous task processing into their Flask applications.

## Prerequisites

- Python 3.x
- Redis Server

## Setup Instructions

### Step 1: Install Redis on Windows 10

1. Download the latest version of Redis for Windows from the [official GitHub repository](https://github.com/microsoftarchive/redis/releases).
2. Unzip the downloaded file.
3. Copy the file path of the unzipped folder.
4. Add the copied file path to your Windows environment variables.
5. Open Command Prompt and start the Redis server with the following command:
    ```sh
    redis-server
    ```

### Step 2: Install Flask and Celery

1. Install Flask and Celery using pip:
    ```sh
    pip install flask celery
    ```
   Alternatively, you can install all the required packages from the `requirements.txt` file:
    ```sh
    pip install -r requirements.txt
    ```

### Step 3: Run the Application

1. Create a Redis account and note the password and endpoint provided.
2. Start the Flask application with the following command:
    ```sh
    py app.py
    ```
3. Open a separate terminal and start the Celery worker with one of the following commands:
    ```sh
    celery -A app.celery worker --loglevel=info
    ```
    Or for a solo pool:
    ```sh
    celery -A app.celery worker --loglevel=info --pool=solo
    ```

## Contributing

Feel free to fork this repository and submit pull requests to contribute to the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
