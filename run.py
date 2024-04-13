from app import create_app
from app.config import Config

app = create_app()

if __name__ == '__main__':
   
   host = Config.HTTP_HOST
   port = Config.HTTP_PORT

   app.run(host=host, port=port, debug=True)