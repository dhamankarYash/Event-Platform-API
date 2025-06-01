import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

print("🔍 Testing Database Connection")
print("=" * 40)
print(f"Database URL: {DATABASE_URL}")

if not DATABASE_URL:
    print("❌ DATABASE_URL not found in .env file")
    exit(1)

try:
    # Create engine
    engine = create_engine(DATABASE_URL)
    
    # Test connection
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1 as test"))
        row = result.fetchone()
        
        if row and row[0] == 1:
            print("✅ Database connection successful!")
            
            # Test database existence
            result = connection.execute(text("SELECT DATABASE()"))
            db_name = result.fetchone()[0]
            print(f"✅ Connected to database: {db_name}")
            
            # Test table creation capability
            connection.execute(text("CREATE TABLE IF NOT EXISTS test_table (id INT PRIMARY KEY)"))
            connection.execute(text("DROP TABLE test_table"))
            print("✅ Database operations working!")
            
        else:
            print("❌ Database test query failed")
            
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    print("\n🔧 Troubleshooting steps:")
    print("1. Make sure MySQL is running")
    print("2. Check if database 'event_platform' exists")
    print("3. Verify user 'event_user' has correct permissions")

    print("4. Check .env file configuration")

    print("4. Check .env file configuration")

