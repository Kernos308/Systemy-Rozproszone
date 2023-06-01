from flask import Flask
from flask import redirect
from flask import abort
app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello'


def load_user(id):
    pass


@app.route('/user/<id>')
def get_user(id):
    return 'Hello {}'.format(id.name)


if __name__ == '__main__':
    app.run()
