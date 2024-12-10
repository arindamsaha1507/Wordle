"""Database operations for the Wordle Sanskrit project."""

import psycopg2
import bcrypt
import toml

secrets = toml.load(".streamlit/secrets.toml")

# Database connection details
HOST = "wordle-db-sanskrit-wordle.f.aivencloud.com"
PORT = 28064
DATABASE = "defaultdb"
USER = "avnadmin"
PASSWORD = secrets["DB_PASSWORD"]
SSLMODE = "require"


def connect_to_db():
    """Connect to the PostgreSQL database."""
    connection = psycopg2.connect(
        host=HOST,
        port=PORT,
        database=DATABASE,
        user=USER,
        password=PASSWORD,
        sslmode=SSLMODE,
    )

    return connection


def disconnect_from_db(
    cursor: psycopg2.extensions.cursor, connection: psycopg2.extensions.connection
):
    """Disconnect from the PostgreSQL database."""
    connection.commit()
    cursor.close()
    connection.close()


def create_table():
    """Create a table for user information."""
    connection = connect_to_db()
    cursor = connection.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        email VARCHAR(100) NOT NULL UNIQUE,
        password_hash VARCHAR(200) NOT NULL
    );
    """
    )

    disconnect_from_db(cursor, connection)


def insert_user(username: str, email: str, raw_password: str):
    """Insert a user into the table."""
    connection = connect_to_db()
    cursor = connection.cursor()

    create_table()

    # Hash the password
    hashed_password = bcrypt.hashpw(
        raw_password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    # Insert user data into the table

    try:
        cursor.execute(
            """
        INSERT INTO users (username, email, password_hash)
        VALUES (%s, %s, %s)
        """,
            (username, email, hashed_password),
        )

    except psycopg2.errors.UniqueViolation as e:  # pylint: disable=no-member
        print(f"Error: {e}")

    disconnect_from_db(cursor, connection)


def remove_user(username: str):
    """Remove a user from the table."""
    connection = connect_to_db()
    cursor = connection.cursor()

    cursor.execute(
        """
    DELETE FROM users
    WHERE username = %s
    """,
        (username,),
    )

    disconnect_from_db(cursor, connection)


def get_all_users():
    """Get all users from the table."""
    connection = connect_to_db()
    cursor = connection.cursor()

    cursor.execute(
        """
    SELECT * FROM users
    """
    )

    users = cursor.fetchall()
    disconnect_from_db(cursor, connection)

    return users


def delete_users_table():
    """Delete the table."""

    connection = connect_to_db()
    cursor = connection.cursor()

    cursor.execute(
        """
    DROP TABLE users
    """
    )

    disconnect_from_db(cursor, connection)


def main():
    """Main function."""
    # Example: Insert a sample user
    username = "q"
    email = "q@q.q"
    raw_password = "secure_password"

    insert_user(username, email, raw_password)

    data = get_all_users()

    print(data)

    # Example: Remove the sample user

    remove_user(username)

    data = get_all_users()

    print(data)

    # Example: Delete the table

    delete_users_table()


if __name__ == "__main__":
    main()
