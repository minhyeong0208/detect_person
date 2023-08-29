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
    
    #return render_template("result.html", results_list=results_list,move_info=move_info)

    key_format = "{}s"

    final_result = {}
    '''for idx, frames in enumerate(results_list[1]):
        key = key_format.format(idx + 1)
        person_index = frames["lab"].index("person") if "person" in frames["lab"] else 0
        cnt_value = frames["cnt"][person_index] if person_index >= 0 else 0

        final_result[key] = {
            "cam2": [cnt_value],
            #"lab": ["person"],
            #"save_path": frames["save_path"]
        }'''
    
    for video_idx, video_results in enumerate(results_list):
        video_key = key_format.format(video_idx + 1)
    
        for frame_idx, frames in enumerate(video_results):
            frame_key = key_format.format(frame_idx + 1)
            frame_key = frame_key.zfill(4)
            person_index = frames["lab"].index("person") if "person" in frames["lab"] else 0
            cnt_value = frames["cnt"][person_index] if person_index >= 0 else 0
        
            if frame_key not in final_result:
                final_result[frame_key] = {}
        
            if video_idx == 0:  # 첫 번째 영상의 경우 "cam1"에 추가
                final_result[frame_key]["cam1"] = [cnt_value]
            elif video_idx == 1:  # 두 번째 영상의 경우 "cam2"에 추가
                final_result[frame_key]["cam2"] = [cnt_value]
            

    return jsonify(final_result)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
