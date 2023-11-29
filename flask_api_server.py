import logging
from flask import Flask, request, render_template
from flask_restful import Resource, Api, reqparse, inputs
from gpiozero import PWMLED, Device
from gpiozero.pins.pigpio import PiGPIOFactory

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("main")
logger.setLevel(logging.INFO)

# Device.pin_factor = PiGPIOFactory()

app = Flask(__name__)
api = Api(app)

LED_GPIO_PIN = 21
led = None
state = {"level": 50}  # initial brightness level of our LED


def init_led():
    global led
    led = PWMLED(LED_GPIO_PIN)
    led.value = (state["level"] / 100)  # gpiozero library expects a value between 0.0 & 1.0


@app.route("/", methods=["GET"])  # decorator
def index():
    return render_template("index_api_client.html", pin=LED_GPIO_PIN)


class LEDControl(Resource):
    def __init__(self):
        # Initialize a request parser for parsing request arguments from the JS
        self.args_parser = reqparse.RequestParser()
        self.args_parser.add_argument(
            name="level",
            required=True,
            type=inputs.int_range(0, 100),
            help="Set the LED brightness level",
            default=None,
        )

    def get(self):
        # Handle GET requests to return the state of the LED
        return state

    def post(self):
        global state
        args = self.args_parser.parse_args()
        logging.info(f"{args}")
        logging.info(f"{state['level']}")

        state["level"] = args.level
        #led.value = state["level"] / 100
        logger.info(f"LED brightness level is: {str(state['level'])}")
        return state


api.add_resource(LEDControl, "/led")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
