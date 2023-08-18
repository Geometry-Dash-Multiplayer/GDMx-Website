from flask import Flask, render_template

# Create an instance of the Flask class
app = Flask(__name__)

# Define a route and a function to handle it
@app.route('/')
def index():
    return render_template("index.html")


# Run the app if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")