import io
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv 
from config import Config
from services.cv_service import ImageMatcher
from services.ai_service import GeoAnalyzer

load_dotenv()

app = Flask(__name__)
CORS(app)
Config.init_app(app)

matcher = ImageMatcher()
geo_analyzer = GeoAnalyzer(Config.GOOGLE_API_KEY)

@app.route('/api/przetworz', methods=['POST'])
def handle_upload():
    file1_list = request.files.getlist('obraz1') # Wycinek (cutout)
    file2_list = request.files.getlist('obraz2') # Referencje (ref)
    
    if not file1_list or not file2_list:
        return jsonify({"error": "Brak wymaganych plików (obraz1 i obraz2)"}), 400

    try:
        cutout_bytes = file1_list[0].read()
        file1_list[0].seek(0) 

        max_matches = -1
        best_result = None

        for ref_file in file2_list:
            ref_bytes = ref_file.read()
            cv_result = matcher.process(cutout_bytes, ref_bytes)
            
            if "err" in cv_result:
                continue
            
            current_matches = cv_result.get("matches", 0)
            if current_matches > max_matches:
                max_matches = current_matches
                best_result = cv_result

        if best_result is None:
             return jsonify({
                "status": "failure",
                "message": "Nie udało się dopasować obrazu do żadnej referencji."
             }), 404

        ai_result_text = geo_analyzer.analyze_image(cutout_bytes)

        final_response = {
            "status": "success",
            "matches": max_matches,
            "result": best_result.get("result_base64", ""), # Obraz wynikowy z CV
            "geoInfo": ai_result_text
        }

        return jsonify(final_response)

    except Exception as e:
        print(f"Błąd serwera: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__  == '__main__':
    app.run(debug=True, port=5000)