import app.application as app
import os

if __name__ == "__main__":
    application_path = os.path.abspath(os.path.dirname(__file__))
    os.environ['application_path'] = application_path

    config_file = os.path.join(application_path,'config.ini')
    os.environ['config_file'] = config_file

    app.main()
