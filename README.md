# Python Course Project: Person API

This project is part of the Udemy course [Python 3 do Zero ao Avançado](https://www.udemy.com/course/python-3-do-zero-ao-avancado/). It demonstrates building a REST API for managing persons using FastAPI, MongoDB, and Docker with modern software architecture patterns.

## Features

- Create, read, and retrieve persons
- Asynchronous operations with Motor (MongoDB async driver)
- Containerized with Docker and Docker Compose
- Clean architecture with CQRS pattern (Commands and Queries)
- Dependency Injection using FastAPI's `Depends`
- Environment-based configuration management
- Type-safe data models with Pydantic

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs with automatic DI
- **Uvicorn**: ASGI server for running FastAPI
- **Motor**: Asynchronous MongoDB driver
- **Pydantic**: Data validation and serialization
- **MongoDB**: NoSQL database
- **Docker & Docker Compose**: Containerization
- **Python 3.8+**: Programming language

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd python-course
   ```

2. Ensure Docker and Docker Compose are installed.

3. Start the services:
   ```bash
   docker-compose up --build
   ```

   This will start MongoDB and the web application.

## Configuration

The application uses environment-based configuration:

- **Development**: Default settings for local development
- **Production**: Uses environment variables for production deployment

### Environment Variables

For production deployment, set the following environment variable:
- `ENV=production`
- `PROD_DB_URL`: MongoDB connection URL for production

## Usage

The API will be available at `http://localhost:8000`.

### API Endpoints

- **GET /**: Health check
  - Response: `{"Message": "healthy"}`

- **GET /person/{id}**: Get a person by ID
  - Parameters: `id` (string)
  - Response: Person object or 404 if not found

- **GET /person/**: Get all persons
  - Response: List of Person objects

- **POST /person/**: Create a new person
  - Body: JSON with person data (name, age, address, is_pep)
  - Response: Created person's ID

### Person Model

```json
{
  "id": "string",
  "name": "string",
  "age": "integer",
  "address": {
    "street": "string",
    "city": "string",
    "state": "string",
    "zip_code": "string"
  },
  "is_pep": "boolean"
}
```

## Architecture

This project follows Clean Architecture principles with CQRS pattern:

### Dependency Injection
- Uses FastAPI's built-in DI system with `Depends`
- Dependencies are injected from outer layers to inner layers
- Easy to test and maintain

### Layers
- **Presentation Layer** (`main.py`): FastAPI routes and DI setup
- **Application Layer** (`features/`): CQRS handlers (Commands and Queries)
- **Infrastructure Layer** (`infra/`): Database connection and repository implementations
- **Domain Layer** (`models/`): Business entities and validation

## Project Structure

```
python-course/
├── main.py                  # FastAPI app with DI configuration
├── settings.py              # Configuration management (Dev/Prod)
├── requirements.txt         # Python dependencies
├── dockerfile               # Docker image configuration
├── docker-compose.yml       # Multi-container setup
├── features/                # Application layer (CQRS)
│   ├── create_person/
│   └── get_person/
├── infra/                   # Infrastructure layer
│   ├── database.py          # Database connection (DI-enabled)
│   └── person_repository.py # Data access layer
├── models/                  # Domain layer
│   ├── person.py
│   └── address.py
└── README.md
```

## Development

To run locally without Docker:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start MongoDB (locally or via Docker)

3. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

### Running Tests

```bash
pytest
```

### Code Quality

- Uses type hints throughout the codebase
- Follows PEP 8 style guidelines
- Implements proper error handling

## Contributing

This is a course project. Feel free to experiment and learn!

## License

[Add license if applicable]
