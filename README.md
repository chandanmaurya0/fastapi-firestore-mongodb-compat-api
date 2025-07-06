# FastAPI with MongoDB

A FastAPI application with MongoDB integration following best practices, using Poetry for dependency management.

## 📋 Features

- 🚀 Async MongoDB connection using Motor
- ✅ Pydantic v2 models for data validation
- ⚙️ Environment variables configuration
- 👥 User management with CRUD operations
- 🔒 Password hashing with bcrypt
- 🌐 CORS middleware
- 🏗️ Clean architecture with separation of concerns
- 🧪 Type hints throughout the codebase

## 🚀 Prerequisites

- Python 3.10+
- MongoDB server (local or remote)
- Poetry (for dependency management)

## 🛠️ Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd fastapi-firestore-mongodb-compat-api
   ```

2. Install Poetry (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Install project dependencies:
   ```bash
   poetry install
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with the following content:
   ```env
   MONGODB_URL=mongodb://localhost:27017
   DATABASE_NAME=fastapi_mongodb
   ```
   Adjust the values according to your MongoDB setup.

5. Activate the Poetry shell (optional but recommended):
   ```bash
   poetry shell
   ```

6. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

7. Open your browser and visit: http://localhost:8000/docs

## 📂 Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application setup
│   ├── config.py            # Configuration settings
│   ├── database/
│   │   ├── __init__.py
│   │   └── db.py            # Database connection and utilities
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py          # User model and schemas
│   ├── routes/
│   │   ├── __init__.py
│   │   └── user_route.py    # User-related API endpoints
│   └── utils/
│       ├── __init__.py
│       └── security.py      # Security utilities (password hashing)
├── .env.example             # Example environment variables
├── poetry.lock              # Poetry lock file
├── pyproject.toml           # Project dependencies and metadata
└── README.md                # This file
```

## 🚀 API Endpoints

### Users

- `POST /users/` - Create a new user
- `GET /users/` - Get all users (with pagination)
- `GET /users/{user_id}` - Get a specific user by ID
- `PUT /users/{user_id}` - Update a user
- `DELETE /users/{user_id}` - Deactivate a user (soft delete)

## 🔧 Development

### Installing new dependencies

```bash
poetry add <package-name>
```

### Running tests

```bash
poetry run pytest
```

### Formatting and Linting

```bash
# Format code with black
poetry run black .

# Check code style with flake8
poetry run flake8
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Project Structure

```
fastapi-mongodb-app/
├── .env.example           # Example environment variables
├── requirements.txt       # Project dependencies
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── config.py         # Application settings
│   ├── database/         # Database connection
│   └── models/           # Pydantic models
└── tests/                # Test files
```

## API Documentation

- Interactive API docs: http://localhost:8000/docs
- Alternative API docs: http://localhost:8000/redoc

## Development

To run the application in development mode with auto-reload:

```bash
uvicorn app.main:app --reload
```

## Testing

To run tests (you'll need to add test files):

```bash
pytest tests/
```

## Deployment

For production deployment, consider using:
- Gunicorn with Uvicorn workers
- Environment variables for configuration
- MongoDB Atlas for managed MongoDB
- Docker containerization

## License

MIT
