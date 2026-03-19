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
