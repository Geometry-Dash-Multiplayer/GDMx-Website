from flask import render_template

from models.app import app


@app.errorhandler(404) # Not Found
def page_not_found(error):
    return render_template('error_pages/404.html'), 404


@app.errorhandler(403) # No permission
def page_not_found(error):
    return render_template('error_pages/404.html'), 404


@app.errorhandler(500) # Internal Server Error
def internal_server_error(error):
    return render_template('error_pages/500.html'), 500


# Run the app if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
