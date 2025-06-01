from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get database URL
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+pymysql://event_user:your_password@localhost:3306/event_platform"
)

def test_connection():
    try:
        # Create engine
        engine = create_engine(DATABASE_URL)
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            print(f"Test query result: {result.fetchone()}")
            
        # Test database exists
        with engine.connect() as connection:
            result = connection.execute(text("SELECT DATABASE()"))
            db_name = result.fetchone()[0]
            print(f"✅ Connected to database: {db_name}")
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure MySQL server is running")
        print("2. Check your database credentials")
        print("3. Verify the database 'event_platform' exists")
        print("4. Ensure the user has proper permissions")

if __name__ == "__main__":
    test_connection()
