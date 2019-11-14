import os

env = os.environ.get("MONGO_ENV", "development")

# URL = "mongodb://newspaper:newspaper@cluster0-5i2ms.mongodb.net/retryWrites=true&w=majority"
# URL = "mongodb://localhost:27017"
all_environments = {
    "development": {"host": "localhost", "port": 27017, "user": None, "password": None},
    "production": {"host": "x.x.x.x", "port": 27017, "user": "production", "password": "production"}
}

db_env_config = all_environments[env]
