import flask
import speedrunner_consts as consts

app = flask.Flask(__name__)
app.config["DEBUG"] = consts.IS_DEBUG

@app.route('/', methods=['GET'])
def home():
    return "<p>Speedrunner API initialized successfully</p>"

if __name__ == '__main__':
    print ('Starting speedrunner_server')
    app.run(port='5002')
    print ('Closing speedrunner_server')