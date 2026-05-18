# Shopping Cart REST API

![CI](https://github.com/bmiegoc1-dev/RepoForTestingPurposes/actions/workflows/ci.yml/badge.svg)

A REST API for managing a shopping cart and product catalog, built with Python and Flask.

---

## What this project does

This API lets you:
- Add and remove products from a user's shopping cart
- View the cart contents and total price
- Manage a product catalog — add products and browse what's available

The project includes a simple browser-based frontend for interacting with the API visually, as well as full support for direct HTTP requests via tools like Postman or curl.

---

## Tech stack

| Technology | What it's used for |
|---|---|
| Python + Flask | building the API and handling HTTP requests |
| SQLAlchemy | talking to the database using Python objects instead of raw SQL |
| PostgreSQL | storing users, products, and cart data |
| Docker + Docker Compose | running the app and database together in isolated containers |
| HTML / CSS / JavaScript | browser-based frontend for interacting with the API |
| pytest | automated testing |
| GitHub Actions | running tests automatically on every push |

---

## Project structure

```
cart_project/
  main.py                      # app entry point — creates and starts Flask

  api/
    cart_routes.py             # endpoints: add, remove, view cart
    store_routes.py            # endpoints: add product, view catalog

  cart_service/
    cart_manager.py            # business logic for cart operations
    store_manager.py           # business logic for catalog operations

  infrastructure/
    models.py                  # database table definitions

  exceptions/
    exceptions.py              # custom error types

  tests/
    conftest.py                # shared test setup
    test_cart_routes.py        # tests for cart endpoints
    test_store_routes.py       # tests for store endpoints

  static/
    index.html                 # browser frontend
```

Each layer has one job. Routes only handle HTTP. Managers only handle logic. Models only handle data. This makes the code easier to read and extend.

---

## How to run

You have two options. Use **Docker** if you want the simplest setup. Use **Local** if you want faster day-to-day development.

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed (for the Docker option)
- Python 3.12 and PostgreSQL installed locally (for the local option)

---

### Option 1 — Docker (recommended for first run)

Docker will set up both the database and the app for you automatically. No manual database setup needed.

**1. Clone the repository**
```bash
git clone https://github.com/bmiegoc1-dev/RepoForTestingPurposes.git
cd RepoForTestingPurposes/cart_project
```

**2. Create your `.env` file**
```bash
cp .env.example .env
```
Open `.env` and set your own password if you want, or leave the defaults for local testing.

**3. Start everything**
```bash
docker compose up --build
```

The API is now running at `http://localhost:5000`.
Open `http://localhost:5000` in your browser to use the frontend.

To stop it:
```bash
docker compose down
```

---

### Option 2 — Local (without Docker)

You need PostgreSQL running on your machine with a database ready.

**1. Clone the repository**
```bash
git clone https://github.com/bmiegoc1-dev/RepoForTestingPurposes.git
cd RepoForTestingPurposes/cart_project
```

**2. Create a virtual environment and install dependencies**
```bash
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**3. Create your `.env` file**
```bash
cp .env.example .env
```
Edit `.env` and set `DATABASE_URL` to point to your local PostgreSQL instance.

**4. Run the app**
```bash
cd cart_project
python main.py
```

The API is now running at `http://localhost:5000`.
Open `http://localhost:5000` in your browser to use the frontend.

---

## API endpoints

### Cart

| Method | Endpoint | What it does |
|---|---|---|
| `POST` | `/add` | Add a product to a user's cart |
| `DELETE` | `/remove` | Remove a product from a user's cart |
| `GET` | `/total/<user_id>` | Get the total price of a user's cart |
| `GET` | `/get_cart/<user_id>` | Get all items in a user's cart |

### Store

| Method | Endpoint | What it does |
|---|---|---|
| `POST` | `/add_store` | Add a product to the catalog |
| `GET` | `/catalog` | Get all products in the catalog |

---

### Example requests

**Add a product to the catalog**
```bash
curl -X POST http://localhost:5000/add_store \
  -H "Content-Type: application/json" \
  -d '{"name": "Cola", "price": 2.50, "quantity": 100}'
```

**Add a product to a cart**
```bash
curl -X POST http://localhost:5000/add \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "product_id": 1, "quantity": 2}'
```

**View a user's cart**
```bash
curl http://localhost:5000/get_cart/1
```

**Get cart total**
```bash
curl http://localhost:5000/total/1
```

---

## Running tests

Tests use an in-memory SQLite database — no running database needed.

```bash
cd cart_project
pytest
```

---

## CI — automated testing

Every push to GitHub automatically runs the full test suite via GitHub Actions. The badge at the top of this file shows the current status.
