This folder contains Alembic configuration for database migrations.

Usage (from project root):

```bash
cd backend
alembic -c alembic.ini revision --autogenerate -m "init"
alembic -c alembic.ini upgrade head
```

Note: alembic must be installed in your Python environment.
