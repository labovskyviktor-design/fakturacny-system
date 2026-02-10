"""
Verify Supabase database migration
"""
import psycopg2

SUPABASE_URL = "postgresql://postgres:Hudriko123+@db.posabupqsehvtwskqulh.supabase.co:5432/postgres"

def main():
    print("Connecting to Supabase...")
    conn = psycopg2.connect(SUPABASE_URL)
    cursor = conn.cursor()
    
    # Get tables
    cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;")
    tables = cursor.fetchall()
    
    print("\nTables in Supabase:")
    for table in tables:
        print(f"  - {table[0]}")
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]};")
        count = cursor.fetchone()[0]
        print(f"    Rows: {count}")
    
    conn.close()
    print("\n✅ Verification complete!")

if __name__ == "__main__":
    main()
