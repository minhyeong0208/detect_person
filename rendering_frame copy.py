from flask import Flask, render_template, request, jsonify
from detect import run
import os
from moviepy.editor import VideoFileClip
import cv2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/process_video', methods=['POST'])
def process_image():
    video_file = request.files['video']  # 사용자가 업로드한 동영상 파일
    upload_dir = "../image/"
    upload_path = os.path.join(upload_dir, video_file.filename)
    
    frames = []
    cap = cv2.VideoCapture(upload_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
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
    
    results = []
    for i, frame in enumerate(frames):
        save_dir = '../image/frame/'  # 이미지를 저장할 경로와 파일명
        frame_path = os.path.join(save_dir, f"frame_{i}.png")
        cv2.imwrite(frame_path, frame)
        cnt, lab, save_path = run(weights='./runs/train/person_yolov5s_results/weights/best.pt', conf_thres=0.5, source=frame_path, exist_ok=True, line_thickness=2)
        result = {
            'cnt': cnt,
            'lab': lab,
            'save_path': save_path
        }
        results.append(result)
    
    length = len(results)
    # 결과를 다른 템플릿으로 전달
    return render_template("result_frame.html", results=results,length=length)
    #return jsonify(results=results, length=length)

if __name__ == '__main__':
    app.run( host='127.0.0.1',port=5000, debug=True)
    