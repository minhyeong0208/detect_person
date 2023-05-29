from flask import Flask, render_template, request, jsonify
from detect import run
import os
from moviepy.editor import VideoFileClip

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/process_image', methods=['POST'])
def process_image():
    video_file = request.files['video']  # 사용자가 업로드한 이미지 파일
    upload_dir = "../image/"
    upload_path = os.path.join(upload_dir, video_file.filename)
    
    # run 함수 실행
    cnt, lab, save_path = run(weights='./runs/train/person_yolov5s_results/weights/best.pt', conf_thres=0.5, source=upload_path, exist_ok=True, line_thickness=2)
    length = len(cnt)
    
    input_file = save_path
    output_file = './static/IMG/result_file.mp4'
    clip = VideoFileClip(input_file)
    clip.write_videofile(output_file, codec='libx264', remove_temp=False, audio=False)
    
    # 결과를 다른 템플릿으로 전달
    return render_template("result.html", cnt=cnt, lab=lab, length=length, save_path=output_file)



if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000, debug=True)
    