from . import main

@main.route("/")
def home():
    return "Hello from the routes blueprint!"