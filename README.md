# iFarm

A Flask-based e-commerce application for farming products with admin and user management.

## Project Overview

**iFarm** is a web application built with Flask and SQLAlchemy that provides:
- **User Management**: User signup, login, and profile management
- **Product Catalog**: Browse and manage farming products
- **Shopping Cart**: Add/remove items and manage cart
- **Checkout System**: Secure payment processing
- **Admin Panel**: Manage products, orders, and users
- **Order History**: Track user purchase history
- **Database Migrations**: SQLAlchemy migrations via Alembic

## Tech Stack

- **Backend**: Flask 3.1.1, SQLAlchemy 2.0.41
- **Database**: PostgreSQL (default), MySQL, or SQLite (dev)
- **ORM**: SQLAlchemy + Alembic (migrations)
- **Forms**: WTForms with CSRF protection
- **Authentication**: Flask-WTF session-based
- **Email**: Flask-Mail
- **Environment**: python-dotenv for configuration

## Prerequisites

- Python 3.8+ (Python 3.11+ recommended)
- PostgreSQL 12+, MySQL 5.7+, or SQLite (for development)
- pip or poetry (package manager)

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/oyeks-ayo/ifarm.git
cd ifarm
```

### 2. Create and activate virtual environment

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example environment file:
```bash
cp config/.env.example config/.env
```

Then edit `config/.env` and add your actual database credentials and secrets:
```properties
DATABASE_URL=postgresql://postgres:password@localhost:5432/ifarm_db
SECRET_KEY=your_generated_secret_key_here
FLASK_DEBUG=1
```

**To generate a secure SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Initialize the database

```bash
# Create tables
flask db upgrade

# Or from Python shell:
# python -c "from pkg import app, db; with app.app_context(): db.create_all()"
```

### 6. (Optional) Load sample data

```bash
# Add any seed data here
python scripts/seed_data.py
```

## Running the Application

### Start the Flask development server:
```bash
python run.py
```

The application will be available at `http://localhost:5000`

### With custom host/port:
```bash
python -c "from pkg import app; app.run(debug=True, host='0.0.0.0', port=8000)"
```

## Project Structure

```
ifarm/
├── config/                 # Configuration files
│   ├── config.py          # Flask config class
│   ├── .env               # Environment variables (DO NOT commit)
│   └── .env.example       # Template for .env
├── migrations/            # Alembic database migrations
│   ├── alembic.ini
│   ├── versions/          # Migration files
│   └── env.py
├── pkg/                   # Main application package
│   ├── __init__.py        # App initialization
│   ├── models.py          # Database models (User, Product, Cart, etc.)
│   ├── forms.py           # WTForms definitions
│   ├── routes/            # Route handlers
│   │   ├── admin_routes.py
│   │   └── user_routes.py
│   ├── static/            # Static assets (CSS, JS, images)
│   │   └── products/      # Product images
│   └── templates/         # HTML templates
│       ├── admin/         # Admin pages
│       └── users/         # User-facing pages
├── run.py                 # Application entry point
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── .env.example          # Environment template
├── README.md             # This file
└── .editorconfig         # Code style settings
```

## Database

### Migrations

Create a new migration after model changes:
```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

View migration history:
```bash
flask db history
```

### Supported Databases

- **PostgreSQL** (recommended for production)
  ```
  DATABASE_URL=postgresql://user:pass@localhost:5432/ifarm_db
  ```
- **MySQL**
  ```
  DATABASE_URL=mysql+pymysql://user:pass@localhost:3306/ifarm_db
  ```
- **SQLite** (development only)
  ```
  DATABASE_URL=sqlite:///ifarm.db
  ```

## Development Workflow

### 1. Activate virtual environment
```bash
# Windows
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

### 2. Install development dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the server
```bash
python run.py
```

### 4. Make changes and test

### 5. Commit changes (make sure `.env` is NOT committed):
```bash
git add .
git commit -m "feat: add new feature"
git push origin main
```

## Key Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 3.1.1 | Web framework |
| SQLAlchemy | 2.0.41 | ORM |
| Flask-SQLAlchemy | 3.1.1 | Flask + SQLAlchemy integration |
| Flask-Migrate | 4.1.0 | Database migrations |
| Flask-WTF | 1.2.2 | Forms with CSRF protection |
| Flask-Mail | 0.10.0 | Email sending |
| python-dotenv | 1.1.1 | Environment variables |
| psycopg2-binary | 2.9.11 | PostgreSQL driver |
| mysql-connector | 2.2.9 | MySQL driver |

See `requirements.txt` for full list.

## Security Considerations

- **Never commit `.env`** – it contains sensitive credentials (already in `.gitignore`)
- **Use strong SECRET_KEY** – generate with `secrets.token_hex(32)`
- **Use HTTPS in production** – configure Flask behind a reverse proxy (Nginx, Apache)
- **Restrict database access** – use firewall rules and least-privilege DB users
- **Enable CSRF protection** – Flask-WTF is already configured
- **Validate user input** – WTForms validators are in place

## Testing

(To be implemented)

```bash
# Run tests
pytest

# With coverage
pytest --cov=pkg tests/
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

### "No such table" or migration errors
- Run `flask db upgrade` to apply migrations
- Check database connection in `config/.env`

### Port 5000 already in use
- Kill the existing process or use a different port:
  ```bash
  python -c "from pkg import app; app.run(port=8000)"
  ```

### Database connection refused
- Verify PostgreSQL/MySQL is running
- Check credentials in `config/.env`
- Ensure database exists: `psql -l` or `mysql -u root -e "SHOW DATABASES;"`

## Contributing

1. Create a new branch: `git checkout -b feature/your-feature`
2. Make changes and commit: `git commit -m "feat: describe your feature"`
3. Push to GitHub: `git push origin feature/your-feature`
4. Create a Pull Request
5. Ensure `.env` is never committed

## License

(Specify license if applicable)

## Contact

Maintainer: [@oyeks-ayo](https://github.com/oyeks-ayo)

---

**Last Updated**: November 14, 2025
