# House Listings API

A Django REST Framework API for querying house listings data with advanced filtering, pagination, and field selection capabilities.

## Features

- RESTful API for house listings data
- Advanced filtering capabilities:
  - Price range filtering
  - Bedroom/bathroom count filtering
  - Location-based filtering (city, state, zipcode)
  - Property type filtering
  - Year built filtering
- Field selection to optimize response payload
- Pagination support
- Search functionality across multiple fields
- Ordering by various fields
- API rate limiting
- Request logging
- Error handling
- CORS support
- OpenAPI/Swagger documentation

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd takehome-be
```

2. Create and activate a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the `listings` directory:
```bash
# Django settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings
DATABASE_URL=sqlite:///db.sqlite3

# API settings
API_RATE_LIMIT=100

# CORS settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Logging settings
LOG_LEVEL=INFO
LOG_FILE=api.log
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Load sample data (if available):
```bash
python manage.py loaddata sample-data/houses.json
```

## Running the Server

Start the development server:
```bash
python manage.py runserver
```

The API will be available at http://127.0.0.1:8000/api/

## API Documentation

### Base URL
```
http://127.0.0.1:8000/api/
```

### Endpoints

#### Houses List
```
GET /api/houses/
```

Query Parameters:
- `fields`: Comma-separated list of fields to include in response
- `min_price`: Minimum price filter
- `max_price`: Maximum price filter
- `min_bedrooms`: Minimum number of bedrooms
- `max_bedrooms`: Maximum number of bedrooms
- `min_bathrooms`: Minimum number of bathrooms
- `max_bathrooms`: Maximum number of bathrooms
- `city`: Filter by city
- `state`: Filter by state
- `zipcode`: Filter by zipcode
- `home_type`: Filter by home type
- `year_built`: Filter by year built
- `tax_year`: Filter by tax year
- `search`: Search across address, city, state, and zip_code
- `ordering`: Order by field (prefix with '-' for descending)
- `page`: Page number for pagination
- `page_size`: Number of items per page (max: 100)

Example Request:
```
GET /api/houses/?min_price=300000&max_price=500000&min_bedrooms=2&fields=id,address,price,bedrooms
```

#### House Detail
```
GET /api/houses/{id}/
```

### Response Format

Example Response:
```json
{
    "count": 100,
    "next": "http://127.0.0.1:8000/api/houses/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "address": "123 Main St",
            "price": 350000,
            "bedrooms": 3,
            "bathrooms": 2,
            "square_feet": 2000,
            "year_built": 1990,
            "city": "San Francisco",
            "state": "CA",
            "zipcode": "94105",
            "home_type": "Single Family"
        }
    ]
}
```

## API Features

### Field Selection
Use the `fields` query parameter to specify which fields to include in the response:
```
GET /api/houses/?fields=id,address,price,bedrooms
```

### Filtering
Multiple filter parameters can be combined:
```
GET /api/houses/?min_price=300000&max_price=500000&min_bedrooms=2
```

### Search
Search across multiple fields:
```
GET /api/houses/?search=San Francisco
```

### Ordering
Order results by any field:
```
GET /api/houses/?ordering=-price  # Descending order
GET /api/houses/?ordering=bedrooms  # Ascending order
```

### Pagination
Results are paginated with 20 items per page by default:
```
GET /api/houses/?page=2&page_size=50
```

## Security Features

- Rate limiting (100 requests per minute by default)
- CORS protection
- Secure headers
- Request logging
- Error handling middleware

## Development

### Running Tests
```bash
python manage.py test
```

### Code Style
The project follows PEP 8 style guidelines.

## Production Deployment

For production deployment:
1. Set `DEBUG=False` in `.env`
2. Use a production-grade WSGI server (e.g., Gunicorn)
3. Configure a production database
4. Set up proper CORS settings
5. Configure proper logging
6. Use environment variables for sensitive data

## License

[Your License Here]

## Contributing

[Your Contributing Guidelines Here]

