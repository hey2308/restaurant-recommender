"""Configuration for Phase 1: Data Foundation Layer."""

from pathlib import Path

# Dataset from problem statement / phased architecture
DATASET_ID = "ManikaSaini/zomato-restaurant-recommendation"
DEFAULT_SPLIT = "train"

# Paths relative to this package root (phase1_data_foundation/)
PACKAGE_ROOT = Path(__file__).resolve().parent
DATA_DIR = PACKAGE_ROOT / "data"
DEFAULT_SQLITE_PATH = DATA_DIR / "restaurants.db"
DEFAULT_CSV_PATH = DATA_DIR / "restaurants_clean.csv"

# Rating and cost bounds for outlier quarantine (see edge cases)
RATING_MIN = 0.0
RATING_MAX = 5.0
COST_MIN = 0.0
COST_MAX = 500_000.0
