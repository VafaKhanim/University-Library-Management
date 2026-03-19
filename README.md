# University Library Management System

A RESTful API for managing university library operations, built with **FastAPI** and **SQLAlchemy**. Designed for library staff to manage books, users, borrowing, and reservations.

---

## Features

- 🔐 Admin authentication with JWT
- 📚 Book management (add, update, delete, search)
- 👥 User management (students & teachers)
- 📖 Borrowing & returning books
- 🔖 Reservation system with FIFO queue
- ⚠️ Overdue tracking & fine calculation
- 📊 Statistics dashboard

---

## Tech Stack

| | |
|---|---|
| Framework | FastAPI |
| Database | SQLite |
| ORM | SQLAlchemy 2.0 |
| Auth | JWT (python-jose) |
| Password | Bcrypt (passlib) |
| Validation | Pydantic v2 |

---

## OOP & Design Patterns

- **Singleton** — Settings, Database connection
- **Factory** — UserFactory (Student/Teacher)
- **Strategy** — Notification system (Email/SMS/App)
- **Observer** — Reservation queue notifications
- **Inheritance** — User → Student, Teacher
- **Abstraction** — Abstract base classes (ABC)
- **Encapsulation** — Private attributes, properties
- **Composition** — Library contains Books, Users, Records

---

## Getting Started

### Requirements
- Python 3.11+

### Installation
```bash
# Clone the repository
git clone https://github.com/VafaKhanim/University-Library-Management.git
cd University-Library-Management

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your values
```

### Run
```bash
uvicorn app.main:app --reload
```

API will be available at `http://127.0.0.1:8000`

---

## API Documentation

After running the server, visit:

- **Swagger UI** → `http://127.0.0.1:8000/docs`
- **ReDoc** → `http://127.0.0.1:8000/redoc`

---

## API Endpoints

### Authentication
| Method | URL | Description |
|---|---|---|
| POST | `/auth/login` | Admin login → JWT token |

### Users
| Method | URL | Description |
|---|---|---|
| POST | `/users/` | Create user |
| GET | `/users/` | List all users |
| GET | `/users/{id}` | Get user |
| PUT | `/users/{id}` | Update user |
| DELETE | `/users/{id}` | Delete user |

### Books
| Method | URL | Description |
|---|---|---|
| POST | `/books/` | Add book |
| GET | `/books/` | List books (search & filter) |
| GET | `/books/{id}` | Get book |
| PUT | `/books/{id}` | Update book |
| DELETE | `/books/{id}` | Delete book |

### Borrowing
| Method | URL | Description |
|---|---|---|
| POST | `/borrow/` | Borrow a book |
| POST | `/borrow/return` | Return a book |
| GET | `/borrow/active` | Active borrows |
| GET | `/borrow/overdue` | Overdue books |
| GET | `/borrow/history/{user_id}` | User borrow history |

### Reservations
| Method | URL | Description |
|---|---|---|
| POST | `/reservations/` | Reserve a book |
| DELETE | `/reservations/{user_id}/{book_id}` | Cancel reservation |
| GET | `/reservations/book/{book_id}` | Book reservation queue |

### Statistics
| Method | URL | Description |
|---|---|---|
| GET | `/stats/` | System statistics |

---

## Project Structure
```
app/
├── core/               # Config, database, security
├── models/             # SQLAlchemy models
├── schemas/            # Pydantic schemas
├── services/           # Business logic
├── routers/            # API endpoints
├── notifications/      # Strategy pattern
└── factories/          # Factory pattern
```

---

## Default Admin

On first run, an admin account is automatically created using credentials from `.env`:
```
Username: admin
Password: admin123  (change in .env)
```

---

