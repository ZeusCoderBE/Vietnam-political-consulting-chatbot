from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import app.Query_VectorDB as sq
from flask_cors import CORS
import os

load_dotenv()
API_GENERATETOR = os.getenv("APIS_GEMINI")
run_app = Flask(__name__)
CORS(run_app)

@run_app.route('/')
def index():
    return render_template('index.html')

# Cập nhật endpoint này để nhận dữ liệu từ form
@run_app.route('/query', methods=['POST'])
def query_endpoint():
    query = request.form.get("query") 
    try:
        response = sq.result_query(query, API_GENERATETOR)
        print(response)
        return jsonify({"result": response})
    except Exception as e:
        return jsonify({"error": f"Đã xảy ra lỗi: {str(e)}"}), 500

# Run the Flask app
if __name__ == '__main__':
   run_app.run(debug=True,port=5000)
