# JWT Flask RESTful API

This project is a Flask-based RESTful API that implements JSON Web Token (JWT) authentication. It provides secure user authentication and authorization for API endpoints.

## Features

- JWT-based authentication
- Protected routes requiring valid tokens
- Token expiration and refresh functionality

## Prerequisites

- Python 3.7 or higher
- Flask
- Virtual environment (optional but recommended)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/jwt_flask.git
    cd jwt_flask/project
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Configure the `.env` file:
    - Create a `.env` file in the project directory.
    - Add the necessary environment variables, such as `SECRET_KEY` and database configuration.

4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask application:
    ```bash
    python -m app
    ```

2. Access the application at `http://127.0.0.1:5000`.

## API Endpoints

- **POST /register**: Register a new user.
- **POST /login**: Authenticate a user and return a JWT.
- **GET /protected**: Access a protected route (requires a valid JWT).