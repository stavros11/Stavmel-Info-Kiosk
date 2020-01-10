import webbrowser
import threading
from app import app


if __name__ == "__main__":
  #threading.Timer(1, webbrowser.open_new("http://127.0.0.1:5000/"))
  #app.run(port=5000)
  app.run(debug=True)
