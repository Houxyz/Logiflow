from psycopg2 import sql
import logging
from .db_connection import connect_to_database

logger = logging.getLogger("db_models")

class BaseModel:
    """Base class for database models"""
    
    @staticmethod
    def execute_query(query, params=None, fetch=True):
        """Execute a SQL query and return results if needed"""
        conn = connect_to_database()
        result = None
        
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query, params)
                
                if fetch:
                    result = cursor.fetchall()
                else:
                    conn.commit()
                
                cursor.close()
                conn.close()
                return result
            except Exception as e:
                logger.error(f"Error executing query: {e}")
                if conn:
                    conn.close()
                return None
        return None

class User(BaseModel):
    """User model for database operations"""
    
    @staticmethod
    def create_user(username, password, email, role='user'):
        """Create a new user in the database"""
        query = """INSERT INTO users (username, password, email, role) 
                  VALUES (%s, %s, %s, %s) RETURNING id"""
        params = (username, password, email, role)
        return BaseModel.execute_query(query, params)
    
    @staticmethod
    def get_user_by_username(username):
        """Get user by username"""
        query = "SELECT * FROM users WHERE username = %s"
        params = (username,)
        return BaseModel.execute_query(query, params)
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        query = "SELECT * FROM users WHERE id = %s"
        params = (user_id,)
        return BaseModel.execute_query(query, params)
    
    @staticmethod
    def update_user(user_id, data):
        """Update user information"""
        # Build dynamic query based on provided data
        query_parts = []
        params = []
        
        for key, value in data.items():
            query_parts.append(f"{key} = %s")
            params.append(value)
        
        params.append(user_id)  # Add user_id for WHERE clause
        
        query = f"UPDATE users SET {', '.join(query_parts)} WHERE id = %s"
        return BaseModel.execute_query(query, params, fetch=False)

class Shipment(BaseModel):
    """Shipment model for database operations"""
    
    @staticmethod
    def create_shipment(origin, destination, status, client_id, details=None):
        """Create a new shipment record"""
        query = """INSERT INTO shipments (origin, destination, status, client_id, details) 
                  VALUES (%s, %s, %s, %s, %s) RETURNING id"""
        params = (origin, destination, status, client_id, details)
        return BaseModel.execute_query(query, params)
    
    @staticmethod
    def get_shipments_by_client(client_id):
        """Get all shipments for a specific client"""
        query = "SELECT * FROM shipments WHERE client_id = %s"
        params = (client_id,)
        return BaseModel.execute_query(query, params)
    
    @staticmethod
    def update_shipment_status(shipment_id, new_status):
        """Update the status of a shipment"""
        query = "UPDATE shipments SET status = %s WHERE id = %s"
        params = (new_status, shipment_id)
        return BaseModel.execute_query(query, params, fetch=False)