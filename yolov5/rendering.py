from flask import Flask, render_template, request, jsonify
from detect import run
import os, cv2
import cv2
from divide_frame import divide_frame
from save_frame import save_frame

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/process_video', methods=['POST'])
def process_image():
    videos = request.files.getlist('video')  # 사용자가 업로드한 동영상 파일들
   
    crowded_threshold = int(request.form.get('crowded'))  # 사용자가 입력한 '포화' 임계값

    frames_list = divide_frame(videos)

    results_list, total_person = save_frame(frames_list)

    print(results_list)

    key_format = "{}s"

    final_result = {}
    

    for video_idx, video_results in enumerate(results_list):
        video_key = key_format.format(video_idx + 1)

        for frame_idx, frames in enumerate(video_results):
            frame_key = key_format.format(frame_idx + 1)
            frame_key = frame_key.zfill(4)

            person_index = frames["lab"].index("person") if "person" in frames["lab"] else 0
            cnt_value = frames["cnt"][person_index] if person_index >= 0 else 0

            if frame_key not in final_result:
                final_result[frame_key] = {}

            cam_key = "cam" + str(video_idx + 1)
            final_result[frame_key][cam_key] = [cnt_value]

    min_values = {}

    for frame_key, cam_data in final_result.items():
        min_value = min(cam_data.values())

        min_values[frame_key] = min_value

    for frame_key, min_value in min_values.items():
        for cam_key, cnt_values in final_result[frame_key].items():
            if cnt_values[0] == min_value[0]:
                cnt_values.append('O')
            elif cnt_values[0] != min_value[0]:
                cnt_values.append('X')

    return jsonify(final_result)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
