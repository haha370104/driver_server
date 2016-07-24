from app_config import app, port
from controller import blue_prints

for bp in blue_prints:
    app.register_blueprint(bp[0], url_prefix=bp[1])


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=port)
