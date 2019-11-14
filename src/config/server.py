import os

env = os.environ.get("PYTHON_ENV", "development")

all_environments = {
    "development": {"port": 5000, "debug": False, "swagger-url": "/api/docs"},
    "production": {"port": 8080, "debug": False, "swagger-url": None}
}

environment_config = all_environments[env]
