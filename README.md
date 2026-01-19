# Python Course Project: Person API

This project is part of the Udemy course [Python 3 do Zero ao Avançado](https://www.udemy.com/course/python-3-do-zero-ao-avancado/). It demonstrates building a REST API for managing persons using FastAPI, MongoDB, and Docker.

## Features

- Create, read, and retrieve persons
- Asynchronous operations with Motor (MongoDB async driver)
- Containerized with Docker and Docker Compose
- Clean architecture with CQRS pattern (Commands and Queries)

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI
- **Motor**: Asynchronous MongoDB driver
- **Pydantic**: Data validation and serialization
- **MongoDB**: NoSQL database
- **Docker & Docker Compose**: Containerization

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

## Project Structure

- `main.py`: FastAPI application entry point
- `features/`: CQRS handlers for create and get operations
- `infra/`: Database connection and repository
- `models/`: Pydantic models for Person and Address
- `requirements.txt`: Python dependencies
- `dockerfile`: Docker image configuration
- `docker-compose.yml`: Multi-container setup

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

## Contributing

This is a course project. Feel free to experiment and learn!

## License

[Add license if applicable]
