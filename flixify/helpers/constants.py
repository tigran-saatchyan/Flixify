"""Constants module"""
import os
from pathlib import Path

# jwt secret and algorithm
JWT_SECRET = '$O4eHb_CekpeTHbl_CekpeT$'
JWT_ALGORITHM = 'HS256'

# hashing parameters
CRYPTOGRAPHIC_HASH_FUNCTION = 'sha256'
PWD_HASH_SALT = b'zis_iz_sikret_solt_shhhh'
PWD_HASH_ITERATIONS = 100_000

# logging folders
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = os.path.join(BASE_DIR, "../logs")

# SQLite db engine and location
SQLITE_DEV_DB_NAME = 'sqlite:///' + os.path.join(
    BASE_DIR,
    'flask_boilerplate_main.db'
    )

SQLITE_TEST_DB_NAME = 'sqlite:///' + os.path.join(
    BASE_DIR, 'flask_boilerplate_test.db'
)
