import os
import sys
from sqlalchemy import create_engine, MetaData, Table, insert, text
from sqlalchemy.orm import Session

# Konfigurácia (tieto URL si user môže upraviť alebo zadať cez env vars)
# Defaultne nastavíme smer Supabase -> Railway (najpravdepodobnejší scenár)
SOURCE_DB_URL = "postgresql://postgres:Hudriko.123@db.posabupqsehvtwskqulh.supabase.co:5432/postgres"
TARGET_DB_URL = "postgresql://postgres:RJkfnaZPErPeXANfHtHgIzKDWQTDaSjI@hopper.proxy.rlwy.net:24076/railway"

def migrate_data():
    print("=== DATA MIGRATION TOOL ===")
    print(f"Source: {SOURCE_DB_URL.split('@')[1]}")
    print(f"Target: {TARGET_DB_URL.split('@')[1]}")
    print("===========================")

    # 0. Vytvoriť schému v Target DB (ak neexistuje)
    print("\nInitializing target schema...")
    from app import app, db
    # Dočasne prepneme URI pre create_all
    original_uri = app.config['SQLALCHEMY_DATABASE_URI']
    app.config['SQLALCHEMY_DATABASE_URI'] = TARGET_DB_URL
    with app.app_context():
        db.create_all()
        print("✅ Schema created (or already exists).")
    
    try:
        source_engine = create_engine(SOURCE_DB_URL)
        target_engine = create_engine(TARGET_DB_URL)
        
        # Test connections
        with source_engine.connect() as conn:
            print("✅ Source connection OK")
        with target_engine.connect() as conn:
            print("✅ Target connection OK")

        source_meta = MetaData()
        source_meta.reflect(bind=source_engine)
        
        target_meta = MetaData()
        target_meta.reflect(bind=target_engine)

        # Poradie tabuliek pre migráciu (kvôli Foreign Keys)
        # Najprv nezávislé tabuľky, potom závislé
        tables_order = [
            'user',      # Users first
            'client',    # Depends on user
            'supplier',  # Depends on user
            'invoice',   # Depends on user, client, supplier
            'invoice_item', # Depends on invoice
            'quotation', # If exists
            'quotation_item', # If exists
            'activity_log' # Depends on user
        ]

        # Filtrujeme len tie, čo existujú v source
        tables_to_migrate = [t for t in tables_order if t in source_meta.tables]
        
        # Pridáme ostatné tabuľky, ktoré nie sú v zozname (ak nejaké sú)
        for table_name in source_meta.tables:
            if table_name not in tables_to_migrate and table_name != 'alembic_version':
                tables_to_migrate.append(table_name)

        print(f"Tables to migrate: {tables_to_migrate}")

        with target_engine.begin() as target_conn:
            # 1. Vyčistiť target (voliteľné - opatrne!)
            # Pre istotu mažeme v opačnom poradí kvôli FK
            print("\nCleaning target database...")
            for table_name in reversed(tables_to_migrate):
                if table_name in target_meta.tables:
                    print(f"  Clearing {table_name}...")
                    target_conn.execute(target_meta.tables[table_name].delete())
            
            # 2. Kopírovať dáta
            print("\nCopying data...")
            for table_name in tables_to_migrate:
                print(f"Processing {table_name}...")
                source_table = source_meta.tables[table_name]
                
                # Načítaj dáta zo source
                with source_engine.connect() as source_conn:
                    rows = source_conn.execute(source_table.select()).fetchall()
                
                if not rows:
                    print(f"  - No rows found, skipping.")
                    continue
                
                print(f"  - Migrating {len(rows)} rows...")
                
                # Insert do target
                # Musíme použiť target metadata pre table definition
                # Ak tabuľka neexistuje v target, mali by sme ju vytvoriť (ale spoliehame sa na db.create_all z appky)
                if table_name in target_meta.tables:
                    target_table = target_meta.tables[table_name]
                    # Konvertuj rows na list dictov
                    data = [dict(row._mapping) for row in rows]
                    target_conn.execute(insert(target_table), data)
                else:
                    print(f"  ⚠️ Table {table_name} does not exist in target database! Run app first to create schema.")

            # 3. Reset sekvencií (aby IDčka pokračovali správne)
            print("\nResetting sequences...")
            for table_name in tables_to_migrate:
                if table_name in target_meta.tables:
                     # Predpokladáme Primary Key je 'id'
                    pk = 'id'
                    # Zistíme max ID
                    max_id = target_conn.execute(text(f"SELECT MAX({pk}) FROM \"{table_name}\"")).scalar()
                    if max_id:
                        print(f"  - Resetting sequence for {table_name} to {max_id + 1}")
                        target_conn.execute(text(f"SELECT setval('{table_name}_{pk}_seq', {max_id})"))

    except Exception as e:
        print(f"\n❌ MIGRATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        return

    print("\n✅ MIGRATION COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    confirm = input("This will OVERWRITE data in Target DB. Are you sure? (y/n): ")
    if confirm.lower() == 'y':
        migrate_data()
    else:
        print("Migration cancelled.")
