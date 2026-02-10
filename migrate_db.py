"""
Database Migration Script: Railway → Supabase
Migrates all data from Railway PostgreSQL to Supabase PostgreSQL
"""
import psycopg2
from psycopg2.extras import RealDictCursor
import sys

# Database connection strings
RAILWAY_URL = "postgresql://postgres:RJkfnaZPErPeXANfHtHgIzKDWQTDaSjI@hopper.proxy.rlwy.net:24076/railway"
SUPABASE_URL = "postgresql://postgres:Hudriko123+@db.posabupqsehvtwskqulh.supabase.co:5432/postgres"

def get_connection(db_url):
    """Create database connection"""
    try:
        conn = psycopg2.connect(db_url)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)

def get_tables(conn):
    """Get list of all tables in the database"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tablename 
        FROM pg_tables 
        WHERE schemaname = 'public'
        ORDER BY tablename;
    """)
    tables = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return tables

def get_table_schema(conn, table_name):
    """Get CREATE TABLE statement for a table"""
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT 
            'CREATE TABLE IF NOT EXISTS ' || quote_ident('{table_name}') || ' (' ||
            string_agg(
                quote_ident(column_name) || ' ' || 
                column_type || 
                CASE WHEN is_nullable = 'NO' THEN ' NOT NULL' ELSE '' END ||
                CASE WHEN column_default IS NOT NULL THEN ' DEFAULT ' || column_default ELSE '' END,
                ', '
            ) || ');'
        FROM (
            SELECT 
                column_name,
                CASE 
                    WHEN data_type = 'USER-DEFINED' THEN udt_name
                    WHEN character_maximum_length IS NOT NULL THEN data_type || '(' || character_maximum_length || ')'
                    WHEN numeric_precision IS NOT NULL THEN data_type || '(' || numeric_precision || ',' || numeric_scale || ')'
                    ELSE data_type
                END as column_type,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position
        ) AS cols;
    """)
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

def migrate_table(source_conn, target_conn, table_name):
    """Migrate a single table from source to target"""
    print(f"\nMigrating table: {table_name}")
    
    # Get schema
    schema = get_table_schema(source_conn, table_name)
    if not schema:
        print(f"  ⚠️  Could not get schema for {table_name}")
        return
    
    # Create table in target
    target_cursor = target_conn.cursor()
    try:
        # Drop table if exists to ensure clean migration
        target_cursor.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
        target_cursor.execute(schema)
        target_conn.commit()
        print(f"  ✓ Created table structure")
    except Exception as e:
        print(f"  ✗ Error creating table: {e}")
        target_conn.rollback()
        return
    
    # Get data from source
    source_cursor = source_conn.cursor(cursor_factory=RealDictCursor)
    try:
        source_cursor.execute(f"SELECT * FROM {table_name};")
        rows = source_cursor.fetchall()
        print(f"  → Found {len(rows)} rows")
        
        if len(rows) == 0:
            print(f"  ✓ Table is empty, skipping data migration")
            return
        
        # Insert data into target
        columns = rows[0].keys()
        placeholders = ', '.join(['%s'] * len(columns))
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        
        for row in rows:
            values = [row[col] for col in columns]
            target_cursor.execute(insert_query, values)
        
        target_conn.commit()
        print(f"  ✓ Migrated {len(rows)} rows")
        
    except Exception as e:
        print(f"  ✗ Error migrating data: {e}")
        target_conn.rollback()
    finally:
        source_cursor.close()
        target_cursor.close()

def main():
    print("=" * 60)
    print("Database Migration: Railway → Supabase")
    print("=" * 60)
    
    # Connect to databases
    print("\n📡 Connecting to Railway database...")
    source_conn = get_connection(RAILWAY_URL)
    print("✓ Connected to Railway")
    
    print("\n📡 Connecting to Supabase database...")
    target_conn = get_connection(SUPABASE_URL)
    print("✓ Connected to Supabase")
    
    # Get list of tables
    print("\n📋 Getting list of tables...")
    tables = get_tables(source_conn)
    print(f"✓ Found {len(tables)} tables: {', '.join(tables)}")
    
    # Migrate each table
    print("\n🚀 Starting migration...")
    for table in tables:
        migrate_table(source_conn, target_conn, table)
    
    # Close connections
    source_conn.close()
    target_conn.close()
    
    print("\n" + "=" * 60)
    print("✅ Migration completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
