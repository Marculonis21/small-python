import flask
import time
app = flask.Flask(__name__)

start = time.time()

@app.route("/time")
def do_count_some_cars():
    return("{} seconds".format(time.time() - start))

app.run(host="0.0.0.0",debug=True)
