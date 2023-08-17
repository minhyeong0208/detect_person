from flask import Flask, render_template, request, jsonify
from detect import run
import os
import cv2
from tracking import person_tracker
from divide_frame import divide_frame
from save_frame import save_frame

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/process_video', methods=['POST'])
def process_image():
    videos = request.files.getlist('video')  # 사용자가 업로드한 동영상 파일들
   
    frames_list = divide_frame(videos)

    results_list, total_person = save_frame(frames_list)
    
    move_info=person_tracker(total_person)     
    print(move_info)
    
    return render_template("result.html", results_list=results_list,move_info=move_info)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
