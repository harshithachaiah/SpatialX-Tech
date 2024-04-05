from flask import Flask
from views import handle_event

app = Flask(__name__)

app.add_url_rule('/v1/event', 'handle_event', handle_event, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True)