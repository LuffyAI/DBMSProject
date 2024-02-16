import pytest
import sqlite3

DATABASE_PATH = '../db/example.db'


@pytest.fixture
def db_connection():
    """Fixture to connect to the database and tear down after tests."""
    connection = sqlite3.connect(DATABASE_PATH)
    yield connection
    connection.close()

def test_user_operations(db_connection):
    """Test inserting, selecting, and deleting a user."""
    cursor = db_connection.cursor()
    
    # Insert a new user
    insert_query = "INSERT INTO users (name, email) VALUES (?, ?)"
    user_data = ('Test User', 'testuser@example.com')
    cursor.execute(insert_query, user_data)
    db_connection.commit()

    # Select the inserted user
    select_query = "SELECT * FROM users WHERE email = ?"
    cursor.execute(select_query, (user_data[1],))
    selected_user = cursor.fetchone()
    print("Inserted user: ", selected_user)
    assert selected_user is not None, "User should be found in the database."
    assert selected_user[1] == user_data[0], "User name should match the inserted value."
    assert selected_user[2] == user_data[1], "User email should match the inserted value."

    # Delete the inserted user
    delete_query = "DELETE FROM users WHERE email = ?"
    cursor.execute(delete_query, (user_data[1],))
    db_connection.commit()

    # Verify the user has been deleted
    cursor.execute(select_query, (user_data[1],))
    user_after_deletion = cursor.fetchone()
    assert user_after_deletion is None, "User should be deleted from the database."