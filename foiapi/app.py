import logging
import foiapi.config as config
from flask import Flask
from foiapi.controller import routes
import pyldapi
import argparse

app = Flask(__name__, template_folder=config.TEMPLATES_DIR, static_folder=config.STATIC_DIR)
app.register_blueprint(routes.routes)


# run the Flask app
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Queensland Features of Interest Dataset')
    parser.add_argument('--init', action="store_true", default=False, help='Initialise the application then exit (rofr.ttl etc)')
    args, unknown = parser.parse_known_args()

    logging.basicConfig(filename=config.LOGFILE,
                        level=logging.DEBUG,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(message)s')

    pyldapi.setup(app, config.APP_DIR, config.DATASET_URI)

    # run the Flask app
    if not args.init:
        app.run(debug=config.DEBUG, threaded=True, use_reloader=False)
