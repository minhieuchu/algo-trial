import os


SERVER_HOST = os.getenv("SERVER_HOST", "localhost")
SERVER_PORT = os.getenv("SERVER_PORT", 8080)

MONGODB_HOST = os.getenv("MONGODB_HOST", "localhost")
MONGODB_PORT = os.getenv("MONGODB_PORT", 27017)
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "algo_trial")
