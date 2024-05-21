from app import create_app

app = create_app()

if __name__ == '__main__':
   
   host = app.config.get("HTTP_HOST")
   port = app.config.get("HTTP_PORT")

   app.run(host=host, port=port, debug=True)