'''
# Civic Engagement Intelligence Platform - Backend

This directory contains the Flask backend for the Civic Engagement Intelligence Platform.

## Features

- **Authentication:** JWT-based authentication and user management.
- **User Roles:** Role-based access control (RBAC) for different user types.
- **Organizations:** Multi-tenant organization management.
- **Campaigns:** Campaign creation and lifecycle management.
- **AI Agents:** Integration with OpenAI for AI-powered recommendations.
- **Auditing:** Comprehensive audit logging for all major actions.

## Setup and Installation

1.  **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure environment variables:**

    Create a `.env` file in the `backend` directory by copying the `.env.example` file:

    ```bash
    cp .env.example .env
    ```

    Update the `.env` file with your database URI and JWT secret key:

    ```
    DATABASE_URL="sqlite:///../instance/app.db"
    JWT_SECRET_KEY="your-super-secret-key"
    OPENAI_API_KEY="your-openai-api-key"
    CORS_ORIGINS="http://localhost:3000"
    ```

4.  **Run the application:**

    ```bash
    python run.py
    ```

    The API will be available at `http://127.0.0.1:5000`.

5.  **Seed the database (optional):**

    To populate the database with initial data for testing, run:

    ```bash
    python seed_data.py
    ```

## API Endpoints

- `/api/auth`: Authentication and user registration.
- `/api/users`: User management.
- `/api/organizations`: Organization management.
- `/api/campaigns`: Campaign management.
- `/api/ai`: AI agent recommendations.

For detailed endpoint information, please refer to the source code in the `app/routes` directory.
'''
