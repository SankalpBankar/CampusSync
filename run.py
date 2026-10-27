import os
from app import create_app

# Local development entry point. Port 5001 avoids common Windows port-5000 conflicts.
app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 5001)), debug=True)
