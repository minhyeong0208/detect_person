from flask import Flask, render_template, request, jsonify
from detect import run
import os
import cv2
from tracking import person_tracker

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home_frame.html')


@app.route('/process_video', methods=['POST'])
def process_image():
    videos = request.files.getlist('video')  # 사용자가 업로드한 동영상 파일들
    upload_dir = "../image/"
    frames_list = []

    for i, video_file in enumerate(videos):
        upload_path = os.path.join(upload_dir, video_file.filename)
        video_file.save(upload_path)

        frames = []
        cap = cv2.VideoCapture(upload_path)
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps

        current_time = 0
        while current_time < duration:
            cap.set(cv2.CAP_PROP_POS_MSEC, int(current_time * 1000))
            success, frame = cap.read()
            if not success:
                break

            frames.append(frame)
            current_time += 1
        cap.release()

        frames_list.append(frames)

    results_list = []
    total_person = []
    for i, frames in enumerate(frames_list):
        results = []
        video_person = []    
        for j, frame in enumerate(frames):
            save_dir = '../image/frame/'  # 이미지를 저장할 경로와 파일명
            frame_path = os.path.join(save_dir, f"frame_{i}_{j}.png")
            cv2.imwrite(frame_path, frame)
            cnt, lab, save_path = run(weights='./runs/train/person_yolov5s_results/weights/best.pt', conf_thres=0.5, source=frame_path, exist_ok=True,
                                      line_thickness=2)
            result = {
                'cnt': cnt,
                'lab': lab,
                'save_path': save_path,
            }
            key = j
            count_person = {}
            if lab[0] == 'person':
                value = cnt[0]
            else:
                value = 0
            count_person = {
                key : value
            }
            video_person.append(count_person)
            results.append(result)
        total_person.append(video_person)
        print(total_person)
        results_list.append(results)
    #move_info=[{0:" 초기 탐색"},{1:"A 에서 B 로 1명 이동"},{2:"B 에서 A 로 2명 이동"},{3:"B 에서 외부로 1명 "}
#,{4:"A 에서 외부로 1명 이동"} ,{5:"외부에서 A 로 1명 이동"} ,{6:"A 에서 B 로 1명 이동"},{7:"외부에서 B 로 3명 이동"},{8:"B 에서 A 로 4명 이동"}]
        
    move_info=person_tracker(total_person)
    #return render_template("result_frame.html", results_list=results_list, move_info=move_info)
    return jsonify(total_person=total_person)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)