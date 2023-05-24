from flask import Flask, render_template, request
from detect import run
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('result.html')


@app.route('/process_image', methods=['POST'])
def process_image():
    image_file = request.files['image']  # 사용자가 업로드한 이미지 파일
    save_dir = './static/IMG/'  # 이미지를 저장할 경로와 파일명
    save_path = os.path.join(save_dir, image_file.filename)
    image_file.save(save_path)  # 이미지 파일 저장

    # run 함수 실행
    cnt, lab = run(weights='./runs/train/person_yolov5s_results/weights/best.pt', conf_thres=0.5, source=save_path, exist_ok=True, line_thickness=2)
    length = len(cnt)

    # 결과를 다른 템플릿으로 전달
    return render_template("home.html", cnt=cnt, lab=lab, length=length, save_path=save_path)




if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000, debug=True)
    