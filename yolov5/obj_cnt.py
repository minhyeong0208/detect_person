from flask import Flask, render_template
from detect import run

#cnt, lab = run(weights='./runs/train/person_yolov5s_results/weights/best.pt', conf_thres=0.5, source='../carrier.jpg', exist_ok=True, line_thickness=2)
#print(cnt)
#print(lab)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    image = '../carrier.jpg'
    cnt, lab = run(weights='./runs/train/person_yolov5s_results/weights/best.pt',conf_thres=0.5, source=image, exist_ok=True, line_thickness=2)
    length = len(cnt)
    return render_template("index.html",cnt=cnt,lab = lab,length=length)

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000, debug=True) #0.0.0.0
