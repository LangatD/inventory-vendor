from app.__init__ import create_app, db
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

if __name__ == "__main__":
    from os import getenv
    port = int(getenv("PORT", 8080))  
    app.run(host="0.0.0.0", port=port, debug=True)