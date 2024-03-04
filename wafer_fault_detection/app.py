from flask import Flask, render_template, jsonify, request, send_file
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.exception import CustomException
from src.logger import logging as lg
import os
from werkzeug.urls import url_quote
from src.pipeline.train_pipeline import TraininingPipeline
from src.pipeline.predict_pipeline import PredictionPipeline

app = Flask(__name__, template_folder='templets')


@app.route("/")
def home():
    return "Welcome to my application"


@app.route("/train")
def train_route():
    try:
        train_pipeline = TraininingPipeline()
        train_pipeline.run_pipeline()

        return "Training Completed."

    except Exception as e:
        raise CustomException(e,sys)

@app.route('/predict', methods=['POST', 'GET'])
def upload():
    
    try:
        if request.method == 'POST':
            print("entered Pipeline")
            # it is a object of prediction pipeline
            prediction_pipeline = PredictionPipeline(request)
            
            print("failed Pipeline")
            #now we are running this run pipeline method
            prediction_file_detail = prediction_pipeline.run_pipeline()

            
            
            lg.info("prediction completed. Downloading prediction file.")
            return send_file(prediction_file_detail.prediction_file_path,
                            download_name= prediction_file_detail.prediction_file_name,
                            as_attachment= True)


        else:
            return render_template('upload_file.html')
    except Exception as e:
        raise CustomException(e,sys)
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug= True)