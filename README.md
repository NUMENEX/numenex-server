# Getting Started with development

## Prerequisites
1. Make sure following are installed properly
    - Install Python and then install poetry

2. Clone the repo

3. Copy `.env.example` to `.env`
    - Run local psql server or get psql server from online sources like supabase (It give you a free postgres db for personal use)

4. update the `.env` file

5. Install dependencies
    - ```bash 
    poetry install
    ```

6. Spin up the server
    - ```bash
    poetry run start
    ```