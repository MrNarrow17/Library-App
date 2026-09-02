# Library Management System

A comprehensive Django-based library management system with user authentication, book borrowing, author management, and order tracking. Built with modern web technologies and a sleek glassmorphism UI.

![Django](https://img.shields.io/badge/Django-6.1-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)
![REST Framework](https://img.shields.io/badge/REST-3.18-red.svg)

---

## Overview

This is a full-featured library management system that allows users to browse books, place orders, and manage their borrowings. Librarians can manage the book catalog, authors, and oversee all orders. The system includes both server-side rendered templates for the main interface and a RESTful API for programmatic access.

**Key Features:**

- User authentication (login, registration, profile management)
- Browse and search books by title or author
- Borrow books with configurable loan periods
- Track active and past orders
- Author management
- Admin dashboard for order management
- RESTful API with versioning
- Beautiful glassmorphism UI with dark theme
- Docker support for easy deployment

---

## Prerequisites

- Python 3.12+
- PostgreSQL 15+ (or SQLite for development)
- pip (Python package manager)
- Docker & Docker Compose (optional)

---

## Installation

### Option 1: Using Docker (Recommended)

1. **Clone the repository:**

```bash
git clone <repository-url>
cd library-system
```

2. **Build and run with Docker Compose:**

```bash
docker-compose up --build
```

The application will be available at `http://localhost:8000`.

### Option 2: Manual Setup

1. **Clone the repository:**

```bash
git clone <repository-url>
cd library-system/library
```

2. **Create and activate a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables** (create a `.env` file):

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

5. **Configure PostgreSQL:**

```bash
# Create a PostgreSQL database
createdb postgres
```

6. **Apply migrations:**

```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Create a superuser:**

```bash
python manage.py createsuperuser
```

8. **Run the development server:**

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

## Quick Start

### Creating Your First Users

1. Navigate to `/auth/register` to create a new visitor account
2. Login with the created credentials
3. Visit `/admin` and login with the superuser account to manage the system

### Managing Books and Authors

1. Login as a librarian/superuser
2. Go to **Authors** (`/author/list`) to add authors
3. Go to **Books** (`/book`) to add books and assign authors
4. Users can now browse and borrow books

### Borrowing a Book

1. Login as a regular user
2. Browse the book collection
3. Click **Borrow** on any available book
4. Track your orders in **My Orders** (`/order`)

---

## Features Walkthrough

### Authentication

- **Login** – `/auth/` – Secure authentication with email and password
- **Register** – `/auth/register` – Create new user accounts
- **Profile Edit** – `/auth/edit` – Update personal information and change password

### Book Management

- **Book List** – `/book` – Browse all books with search and filter capabilities
- **Book Detail** – `/book/<id>` – View detailed book information, description, and authors
- **Add Book** – `/book/create` – Librarians only – Add new books to the catalog
- **Edit Book** – `/book/<id>/edit` – Update book details
- **Delete Book** – `/book/<id>/delete` – Remove books from the system

### Author Management

- **Author List** – `/author/list` – View all authors with their associated books
- **Add Author** – `/author/create` – Librarians only – Add new authors
- **Delete Author** – `/author/delete/<id>` – Remove authors (only if they have no books)

### Order System

- **My Orders** – `/order` – View your borrowing history and active orders
- **All Orders** – `/order/all` – Admin view of all orders in the system
- **Create Order** – `/order/create` – Borrow a book with a 14-day loan period
- **Close Order** – `/order/<id>/close` – Mark orders as returned

### User Management

- **User List** – `/user/list` – View all registered users
- **User Detail** – `/user/<id>` – View detailed user profile information

---

## REST API

The system includes a versioned REST API (v1) with endpoints for books, orders, authors, and users.

### Base URL

```
/api/v1/
```

### Authentication

API endpoints require authentication via:

- Session authentication (for web interface users)
- Basic authentication (for API clients)

### Endpoints

| Method | Endpoint                             | Description           | Permissions   |
| ------ | ------------------------------------ | --------------------- | ------------- |
| GET    | `/api/v1/book`                       | List all books        | Public        |
| POST   | `/api/v1/book`                       | Create a book         | Admin         |
| GET    | `/api/v1/book/<id>`                  | Get book details      | Public        |
| PUT    | `/api/v1/book/<id>`                  | Update a book         | Admin         |
| DELETE | `/api/v1/book/<id>`                  | Delete a book         | Admin         |
| GET    | `/api/v1/order`                      | List all orders       | Admin         |
| POST   | `/api/v1/order`                      | Create an order       | Admin         |
| GET    | `/api/v1/order/<id>`                 | Get order details     | Admin         |
| PUT    | `/api/v1/order/<id>`                 | Update an order       | Admin         |
| DELETE | `/api/v1/order/<id>`                 | Delete an order       | Admin         |
| GET    | `/api/v1/user/<id>/order`            | Get user's orders     | Authenticated |
| POST   | `/api/v1/user/<id>/order`            | Create order for user | Authenticated |
| GET    | `/api/v1/user/<id>/order/<order_id>` | Get specific order    | Authenticated |

### Example API Request

```bash
# Get all books
curl -X GET http://localhost:8000/api/v1/book \
  -H "Accept: application/json"

# Create a book (admin only)
curl -X POST http://localhost:8000/api/v1/book \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Django for APIs",
    "description": "Build web APIs with Django",
    "count": 5,
    "author_ids": [1, 2],
    "year_of_publication": "2024-01-01"
  }'
```

---

## Testing

The project includes Selenium tests for authentication workflows.

```bash
# Run all tests
python manage.py test tests/

# Run specific test
python manage.py test tests.test_auth.LoginLogoutSystemTest
```

### Test Coverage

The test suite validates:

- Successful login with valid credentials
- Successful logout
- Failed login with invalid credentials
- Error messages for invalid login attempts

---

## Docker Deployment

For production deployment:

1. **Set environment variables** in your `.env` file
2. **Build the Docker image:**

```bash
docker-compose build
```

3. **Run the container:**

```bash
docker-compose up -d
```

4. **Apply migrations and create superuser:**

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## License

This project is open source and available under the [MIT License](LICENSE).

---
