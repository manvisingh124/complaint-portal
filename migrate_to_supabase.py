import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

def run():
    print("=" * 60)
    print("🚀 BBDU Grievance Portal — Supabase PostgreSQL Direct Setup")
    print("=" * 60)

    db_password = os.getenv('SUPABASE_DB_PASSWORD', '')
    if not db_password or db_password == 'your_supabase_db_password':
        print("\n⚠️  SUPABASE_DB_PASSWORD is missing or set to placeholder in .env!")
        print("   Please edit .env and set your actual Supabase Database Password:")
        print("   SUPABASE_DB_PASSWORD=your_actual_password")
        print("\n   Alternatively, copy schema.sql and run it in your Supabase Dashboard SQL Editor.")
        sys.exit(1)

    print("\n1. Enabling Supabase PostgreSQL database mode...")
    os.environ['USE_SUPABASE_DB'] = 'True'

    print("2. Applying Django database migrations directly to Supabase...")
    res = subprocess.run([sys.executable, 'manage.py', 'migrate'], cwd=BASE_DIR)
    if res.returncode != 0:
        print("\n❌ Migration failed. Please verify SUPABASE_DB_PASSWORD and connection info.")
        sys.exit(res.returncode)

    print("\n3. Seeding demo accounts and complaints to Supabase...")
    res_seed = subprocess.run([sys.executable, 'seed_data.py'], cwd=BASE_DIR)
    if res_seed.returncode != 0:
        print("\n❌ Seeding failed.")
        sys.exit(res_seed.returncode)

    print("\n🎉 SUCCESS! Your Supabase database is fully provisioned and seeded!")

if __name__ == '__main__':
    run()
