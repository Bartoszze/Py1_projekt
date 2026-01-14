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
    file1 = request.files.getlist('obraz1') 
    file2_list = request.files.getlist('obraz2') 
    
    if not file1 or not file2_list:
        return jsonify({"error": "Brak wymaganych plików"}), 400

    try:
        cutout_bytes = file1[0].read()
        
        max_matches = 0
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
    
        ai_result_text = geo_analyzer.analyze_image(cutout_bytes)
        final_response = {
            "status": "success",
            "matches": max_matches,
            "geoInfo": ai_result_text,
            "result": best_result.get("result_base64", "") if best_result else ""
        }
        
        if not best_result:
             final_response["message"] = "Brak dopasowania."

        return jsonify(final_response)

    except Exception as e:
        print(f"Błąd serwera: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__  == '__main__':
    app.run(debug=True, port=5000)