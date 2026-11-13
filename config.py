"""Central configuration. Values can be overridden with environment variables."""
import os

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com").rstrip("/")
STANDARD_USER = os.getenv("STANDARD_USER", "standard_user")
LOCKED_OUT_USER = os.getenv("LOCKED_OUT_USER", "locked_out_user")
PASSWORD = os.getenv("PASSWORD", "secret_sauce")
