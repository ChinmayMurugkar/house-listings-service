# House Listings API

A Django REST Framework API for managing house listings with features like filtering, searching, and rate limiting.

## Features

- RESTful API for house listings
- Token-based authentication
- Rate limiting
- Request logging
- Error handling
- Filtering and searching
- Pagination
- Field selection
- API documentation with Swagger/OpenAPI

## Setup

1. Clone the repository:
```bash
git clone <your-fork-url>
cd listings
```

2. Create and activate virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/token/` - Get authentication token

### Houses
- `GET /api/houses/` - List all houses
- `POST /api/houses/` - Create a new house
- `GET /api/houses/{id}/` - Get a specific house
- `PUT /api/houses/{id}/` - Update a house
- `PATCH /api/houses/{id}/` - Partially update a house
- `DELETE /api/houses/{id}/` - Delete a house

### Documentation
- `GET /api/schema/` - OpenAPI schema
- `GET /api/docs/` - Swagger UI documentation

## Filtering and Searching

The API supports various filtering options:
- Price range: `?min_price=200000&max_price=400000`
- Bedrooms: `?min_bedrooms=2&max_bedrooms=4`
- Bathrooms: `?min_bathrooms=1&max_bathrooms=3`
- Home size: `?min_home_size=1000&max_home_size=3000`
- Home type: `?home_type=Single%20Family`
- Location: `?city=Test%20City&state=TS&zipcode=12345`
- Search: `?search=Test%20City`
- Ordering: `?ordering=price` or `?ordering=-price`
- Field selection: `?fields=id,address,price`

## Rate Limiting

The API implements rate limiting (100 requests per minute by default). In debug mode, you can reset the rate limit counter:
- `GET /api/houses/reset_rate_limit/`

## Admin Interface

Access the Django admin interface at `/admin/` to manage:
- House listings
- Users and permissions
- Authentication tokens

## Environment Variables

Create a `.env` file with the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
API_RATE_LIMIT=100
CORS_ALLOWED_ORIGINS=http://localhost:3000
LOG_LEVEL=INFO
LOG_FILE=api.log
```

## Testing

Run the test suite:
```bash
python manage.py test api.tests
```

## License

MIT 