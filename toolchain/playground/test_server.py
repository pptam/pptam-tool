from flask import Flask
import random
import time

app = Flask(__name__)

last_wait_time = 1
wait_time_direction = +0.1

@app.route("/")
def index():
    global last_wait_time
    global wait_time_direction

    if last_wait_time>5:
        wait_time_direction = -0.1

    last_wait_time = last_wait_time + wait_time_direction
    time.sleep(last_wait_time)    
    return "Hi"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=True, debug=True)