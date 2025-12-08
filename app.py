import os
from flask import Flask, request, jsonify
from flask_cors import CORS

from config import Config
from services.cv_service import ImageMatcher
from services.ai_service import GeoAnalyzer

app = Flask(__name__)
CORS(app)
Config.init_app(app)

matcher = ImageMatcher()
geo_analyzer = GeoAnalyzer(Config.GOOGLE_API_KEY)

@app.route('/api/przetworz', methods=['POST'])
def handle_upload():
    if 'obraz1' not in request.files or 'obraz2' not in request.files:
        return jsonify({"Error": "Brak wymaganych plików"}), 400

    file1 = request.files['obraz1'] # cutout
    file2 = request.files['obraz2'] # ref

    path1 = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
    path2 = os.path.join(app.config['UPLOAD_FOLDER'], file2.filename)

    try:
        file1.save(path1)
        file2.save(path2)

        cv_result = matcher.process(path1, path2)

        if "err" in cv_result:
            return jsonify(cv_result) 

        ai_result_text = geo_analyzer.analyze_image(path2)

        final_response = {
            "status": "success",
            "matches": cv_result["matches"],
            "result": cv_result["result_base64"],
            "geoInfo": ai_result_text
        }

        return jsonify(final_response)

    except Exception as e:
        print(f"BŁĄD SERWERA: {str(e)}")
        return jsonify({"Error": str(e)}), 500
        
    finally:
        if os.path.exists(path1): os.remove(path1)
        if os.path.exists(path2): os.remove(path2)

if __name__  == '__main__':
    app.run(debug=True, port=5000)