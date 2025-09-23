import psycopg2
from psycopg2 import sql
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("database.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("db_connection")

def connect_to_database():
    """
    Establishes a connection to the PostgreSQL database.
    Returns a connection object if successful, None otherwise.
    """
    try:
        # Connection parameters
        conn_params = {
            "host": "localhost",      
            "database": "Db_LogiXport",
            "user": "postgres",      
            "password": "Dork0909",  
            "port": "5432"          
        }
        
        # Establish connection
        connection = psycopg2.connect(**conn_params)
        logger.info("Successfully connected to PostgreSQL database")
        return connection
    
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        return None

def test_connection():
    """
    Tests the database connection by executing a simple query.
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()
            logger.info(f"PostgreSQL database version: {db_version}")
            
            # Close cursor and connection
            cursor.close()
            conn.close()
            logger.info("Database connection closed")
            return True
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            if conn:
                conn.close()
            return False
    return False

if __name__ == "__main__":
    test_connection()