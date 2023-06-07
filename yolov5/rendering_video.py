from flask import Flask, render_template, request
from detect import run
import os
from moviepy.editor import VideoFileClip

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home_video.html')


@app.route('/process_video', methods=['POST'])
def process_image():
    video_file = request.files['video']  # 사용자가 업로드한 동영상 파일
    upload_dir = "../image/"
    upload_path = os.path.join(upload_dir, video_file.filename)
    
    # run 함수 실행
    cnt, lab, save_path = run(weights='./runs/train/person_yolov5s_results/weights/best.pt', conf_thres=0.5, source=upload_path, exist_ok=True, line_thickness=2)
    length = len(cnt)
    
    #인코딩 H.264
    input_file = save_path
    output_file = './static/IMG/result_file.mp4'
    clip = VideoFileClip(input_file)
    clip.write_videofile(output_file, codec='libx264', remove_temp=False, audio=False)
    
    
    # 결과를 다른 템플릿으로 전달
    return render_template("result_video.html", cnt=cnt, lab=lab, length=length, save_path=output_file)


if __name__ == '__main__':
    app.run( host='127.0.0.1',port=5000, debug=True)
    