import os
class Config:
    UPLOAD_FOLDER = 'uploads'
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

    @staticmethod
    def init_app(app):
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)
        app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER