from src import create_app
import os
from src.config import DevelopmentConfig, ProductionConfig
import subprocess
from threading import Thread

if os.environ.get("FLASK_ENV") == "development":
    t = Thread(
        target=subprocess.run, args=["npx webpack serve"], kwargs={"shell": True}
    )
    t.start()
    app = create_app(config=DevelopmentConfig)
else:
    subprocess.run("npx webpack")
    app = create_app(config=ProductionConfig)

if __name__ == "__main__":
    app.run("0.0.0.0", os.environ.get("PORT", 5000))
