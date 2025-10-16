'''
# Civic Engagement Intelligence Platform

A comprehensive platform for managing civic engagement campaigns with AI-powered recommendations, role-based access control, and advanced analytics.

## Overview

The Civic Engagement Intelligence Platform is designed to help organizations, political campaigns, NGOs, and public figures manage their civic engagement efforts effectively. The platform combines traditional campaign management tools with cutting-edge AI capabilities to provide intelligent recommendations, content generation, and performance analytics.

## Key Features

### 🎯 Campaign Management

- Create and manage multiple campaigns with different objectives
- Track campaign lifecycle from draft to completion
- Define target audiences and campaign objectives
- Monitor campaign performance in real-time

### 🤖 AI-Powered Agents

The platform includes four specialized AI agents:

1.  **Narrative Architect:** Analyzes public discourse and suggests narrative frameworks aligned with campaign goals
2.  **Content Synthesizer:** Generates educational explainer content based on campaign objectives
3.  **Distribution Optimizer:** Recommends optimal posting times, channels, and content formats
4.  **Feedback Intelligence:** Analyzes engagement data and flags potential misinformation

### 👥 User Management

- Seven distinct user roles with granular permissions
- Role-based access control (RBAC) for all features
- Multi-tenant organization support
- Comprehensive user activity tracking

### 📊 Analytics Dashboard

- Real-time campaign performance metrics
- Interactive data visualizations
- Engagement tracking and sentiment analysis
- Exportable reports and insights

### 🔒 Security & Compliance

- JWT-based authentication
- Comprehensive audit logging
- Compliance reporting and monitoring
- Data privacy controls

## User Roles

| Role | Description | Key Permissions |
|------|-------------|----------------|
| **Super Admin** | Full system access | All permissions |
| **Organization Admin** | Manage organization resources | User management, campaign management, content approval |
| **Campaign Manager** | Create and manage campaigns | Campaign CRUD, request AI recommendations |
| **Content Creator** | Create campaign content | Content creation and editing |
| **Analyst** | View analytics and reports | Analytics access, report generation |
| **Reviewer** | Review AI recommendations | Review and approve AI-generated content |
| **Viewer** | Read-only access | View campaigns, content, and analytics |

## Technology Stack

### Backend

- **Framework:** Flask (Python)
- **Database:** PostgreSQL / SQLite
- **Authentication:** JWT (Flask-JWT-Extended)
- **AI Integration:** OpenAI GPT-4
- **ORM:** SQLAlchemy

### Frontend

- **Framework:** React 18
- **Build Tool:** Vite
- **Styling:** Tailwind CSS
- **UI Components:** shadcn/ui
- **Charts:** Recharts
- **Icons:** Lucide React
- **Routing:** React Router

## Project Structure

```
civic-platform/
├── backend/                 # Flask backend application
│   ├── app/
│   │   ├── models/         # Database models
│   │   ├── routes/         # API route handlers
│   │   ├── services/       # Business logic and AI agents
│   │   └── utils/          # Utility functions
│   ├── run.py              # Application entry point
│   ├── seed_data.py        # Database seeding script
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend application
│   ├── src/
│   │   ├── components/     # Reusable React components
│   │   ├── pages/          # Page components
│   │   ├── contexts/       # React contexts
│   │   └── lib/            # Utility functions and API client
│   ├── package.json        # Node.js dependencies
│   └── vite.config.js      # Vite configuration
├── DEPLOYMENT_GUIDE.md     # Comprehensive deployment instructions
└── README.md               # This file
```

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL (for production) or SQLite (for development)
- OpenAI API key

### Backend Setup

1.  **Navigate to backend directory:**

    ```bash
    cd backend
    ```

2.  **Create virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment:**

    ```bash
    cp .env.example .env
    ```

    Edit `.env` and add your configuration:

    ```
    DATABASE_URL="sqlite:///../instance/app.db"
    JWT_SECRET_KEY="your-secret-key"
    OPENAI_API_KEY="your-openai-api-key"
    CORS_ORIGINS="http://localhost:3000"
    ```

5.  **Initialize database:**

    ```bash
    python seed_data.py
    ```

6.  **Run the backend:**

    ```bash
    python run.py
    ```

    The API will be available at `http://127.0.0.1:5000`.

### Frontend Setup

1.  **Navigate to frontend directory:**

    ```bash
    cd frontend
    ```

2.  **Install dependencies:**

    ```bash
    npm install
    ```

3.  **Configure environment:**

    Create a `.env` file:

    ```
    VITE_API_BASE_URL=http://127.0.0.1:5000
    ```

4.  **Run the development server:**

    ```bash
    npm run dev
    ```

    The application will be available at `http://localhost:3000`.

### Default Login Credentials

After running `seed_data.py`, you can login with:

- **Email:** admin@example.com
- **Password:** admin123

**⚠️ Important:** Change the default password immediately after first login.

## API Documentation

### Authentication Endpoints

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and receive JWT token
- `POST /api/auth/refresh` - Refresh JWT token
- `GET /api/auth/me` - Get current user information

### User Management

- `GET /api/users` - List all users
- `GET /api/users/<id>` - Get user by ID
- `POST /api/users` - Create new user
- `PUT /api/users/<id>` - Update user
- `DELETE /api/users/<id>` - Delete user

### Organization Management

- `GET /api/organizations` - List all organizations
- `GET /api/organizations/<id>` - Get organization by ID
- `POST /api/organizations` - Create new organization
- `PUT /api/organizations/<id>` - Update organization
- `DELETE /api/organizations/<id>` - Delete organization

### Campaign Management

- `GET /api/campaigns` - List all campaigns
- `GET /api/campaigns/<id>` - Get campaign by ID
- `POST /api/campaigns` - Create new campaign
- `PUT /api/campaigns/<id>` - Update campaign
- `DELETE /api/campaigns/<id>` - Delete campaign

### AI Recommendations

- `GET /api/ai/recommendations` - List all recommendations
- `POST /api/ai/recommendations` - Request new AI recommendation
- `PUT /api/ai/recommendations/<id>/review` - Review recommendation

## Development

### Running Tests

**Backend tests:**

```bash
cd backend
pytest
```

**Frontend tests:**

```bash
cd frontend
npm test
```

### Code Style

**Backend:**

- Follow PEP 8 style guide
- Use Black for code formatting
- Use pylint for linting

**Frontend:**

- Follow ESLint configuration
- Use Prettier for code formatting

### Contributing

1.  Fork the repository
2.  Create a feature branch (`git checkout -b feature/amazing-feature`)
3.  Commit your changes (`git commit -m 'Add amazing feature'`)
4.  Push to the branch (`git push origin feature/amazing-feature`)
5.  Open a Pull Request

## Deployment

For comprehensive deployment instructions, please refer to the [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md).

### Quick Deployment Options

- **Backend:** Heroku, AWS, DigitalOcean, or any VPS
- **Frontend:** Netlify, Vercel, or static hosting
- **Database:** PostgreSQL (recommended for production)

## Security Considerations

- Always use HTTPS in production
- Keep JWT secret keys secure and rotate regularly
- Use strong database passwords
- Enable rate limiting on API endpoints
- Regularly update dependencies
- Implement proper CORS configuration
- Enable audit logging for compliance

## Compliance Features

The platform includes built-in compliance features:

- **Audit Logging:** All user actions are logged
- **Data Privacy:** User data protection mechanisms
- **Content Provenance:** Track AI-generated content
- **Compliance Reports:** Generate compliance reports for organizations
- **Access Control:** Granular permission system

## Monitoring and Maintenance

### Health Check

```bash
curl https://api.your-domain.com/health
```

### Logs

- Backend logs: Application logs via systemd or hosting platform
- Database logs: PostgreSQL logs
- Frontend logs: Browser console and error tracking service

### Backup

- Database: Automated daily backups recommended
- Configuration: Store `.env` files securely
- Code: Version control with Git

## Troubleshooting

### Common Issues

**Database connection errors:**

- Verify database credentials in `.env`
- Check database service is running
- Ensure database exists

**CORS errors:**

- Check `CORS_ORIGINS` in backend `.env`
- Verify frontend is using correct API URL

**AI recommendation failures:**

- Verify OpenAI API key is valid
- Check API rate limits
- Review error logs

## Roadmap

- [ ] Mobile application (iOS/Android)
- [ ] Advanced sentiment analysis
- [ ] Multi-language support
- [ ] Integration with social media platforms
- [ ] Real-time collaboration features
- [ ] Advanced reporting and export options

## License

This project is proprietary software. All rights reserved.

## Support

For support, please contact:

- **Email:** support@civicplatform.com
- **Documentation:** [docs.civicplatform.com](https://docs.civicplatform.com)
- **Issues:** GitHub Issues

## Acknowledgments

- OpenAI for GPT-4 API
- React and Vite communities
- Flask and SQLAlchemy maintainers
- All contributors to this project

---

**Built with ❤️ for civic engagement and democratic participation.**

**Version:** 1.0.0  
**Last Updated:** October 2025
'''
