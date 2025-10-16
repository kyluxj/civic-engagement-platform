'''
# Civic Engagement Intelligence Platform - Frontend

This directory contains the React frontend for the Civic Engagement Intelligence Platform dashboard.

## Features

- **Authentication:** Secure login and session management.
- **Dashboard:** Centralized dashboard with key metrics and activity overview.
- **User Management:** Interface for managing users and their roles.
- **Organization Management:** CRUD interface for organizations.
- **Campaign Management:** Comprehensive campaign creation and management tools.
- **AI Recommendations:** Interface for requesting and reviewing AI-powered recommendations.
- **Analytics:** Data visualizations and performance analytics.
- **Role-Based Access:** Dynamic UI that adapts to user permissions.

## Setup and Installation

1.  **Install dependencies:**

    ```bash
    npm install
    ```

2.  **Configure environment variables:**

    Create a `.env` file in the `frontend` directory:

    ```
    VITE_API_BASE_URL=http://127.0.0.1:5000
    ```

3.  **Run the development server:**

    ```bash
    npm run dev
    ```

    The application will be available at `http://localhost:3000`.

## Building for Production

To create a production build, run:

```bash
npm run build
```

The production-ready files will be in the `dist` directory.

## Tech Stack

- **React:** Frontend library for building user interfaces.
- **Vite:** Build tool for modern web development.
- **Tailwind CSS:** Utility-first CSS framework.
- **shadcn/ui:** Re-usable components built with Radix UI and Tailwind CSS.
- **Recharts:** Composable charting library built on React components.
- **Lucide React:** Beautiful and consistent icons.
- **React Router:** Declarative routing for React.
'''
