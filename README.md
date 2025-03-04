# Expense and Event Tracker

## Overview

Expense and Event Tracker is a comprehensive web application that helps users manage their personal expenses and track events efficiently. Built with Angular and Flask, the application provides a user-friendly interface for financial and event management.

## Features

### Expense Management
- Track daily expenses
- Categorize expenses
- Generate expense reports
- Monthly and yearly spending analysis

### Event Management
- Create and manage personal events
- Set event categories and locations
- View upcoming events
- Event summary and insights

## Technology Stack

### Backend
- Python
- Flask
- SQLAlchemy
- PostgreSQL
- JWT Authentication

### Frontend
- Angular
- RxJS
- NgRx
- PrimeNG
- Tailwind CSS

### DevOps
- Docker
- Docker Compose
- Nginx

## Prerequisites
- Docker
- Docker Compose
- Node.js (v18+)
- Python (v3.11+)

## Installation

### Local Development

1. Clone the repository
```bash
git clone https://github.com/yourusername/expense-event-tracker.git
cd expense-event-tracker
```

2. Start the application
```bash
docker-compose up --build
```

3. Access the application
- Frontend: `http://localhost`
- Backend API: `http://localhost:5000`
- PgAdmin: `http://localhost:8080`

## Environment Variables

### Backend
- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET_KEY`: Secret key for JWT token generation

### Frontend
- `API_BASE_URL`: Backend API base URL

## Development

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```

### Frontend
```bash
cd frontend
npm install
ng serve
```

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
ng test
```

## Deployment
The application is containerized and can be deployed using Docker Compose. For production, configure environment-specific settings in `.env` files.

## Security
- JWT-based authentication
- Password hashing
- CORS configuration
- Secure nginx configuration

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License.