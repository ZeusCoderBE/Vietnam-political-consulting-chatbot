from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from app.vector_database.result import result_query
from flask_cors import CORS
from app.etl.etl import ETL
    
load_dotenv()
run_app = Flask(__name__)
CORS(run_app)
@run_app.route('/')

def index():
    return render_template('index.html')
@run_app.route('/query', methods=['POST'])
def query_endpoint():
    data = request.get_json()   
    query = data.get("query") 
    try:
        response = result_query(query)
        return jsonify({"result": response})
    except Exception as e:
        return jsonify({"error": f"Đã xảy ra lỗi: {str(e)}"}), 500
@run_app.route("/add_links", methods=["POST"])
def add_links():
    data = request.get_json() 
    link = data.get("link")  
    try:
        etl_link=ETL([link]) 
        data_link=etl_link.extract_data_from_link()
        etl_link.load_qdrant(data_link)
        return jsonify({"result": "Thêm thành công"})
    except Exception as e:
        return jsonify({"error": f"Đã xảy ra lỗi: {str(e)}"}), 500
if __name__ == '__main__':
   run_app.run(debug=True,port=5000)
