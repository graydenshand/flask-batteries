from src import create_app
import os
from src.config import DevelopmentConfig, ProductionConfig

if os.environ.get("FLASK_ENV") == "development":
    app = create_app(config=DevelopmentConfig)
else:
    app = create_app(config=ProductionConfig)
