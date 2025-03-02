from app import create_app


app = create_app()

if __name__ == "__main__":
    from os import getenv
    port = int(getenv("PORT", 5555))  
    app.run(host="0.0.0.0", port=port, debug=True)
