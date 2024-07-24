# Getting Started with development

## Prerequisites
1. Make sure following are installed properly
    - Install Python and then install poetry

2. Clone the repo

3. Copy `.env.example` to `.env`
    - Run local psql server or get psql server from online sources like supabase (It give you a free postgres db for personal use)
4. Update `sqlalchemy.url` in alembic.ini with the postgres url

5. update the `.env` file

6. Install dependencies
    ```shell 
    poetry install
    ```
7. Run the migration
```bash
alembic upgrade head
```

8. Spin up the server
    ```shell
    poetry run start
    ```