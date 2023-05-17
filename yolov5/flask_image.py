from flask import Flask, jsonify
from detect import run

app = Flask(__name__)

@app.route('/', methods=['GET'])
def object_count():
    # cap = cv2.VideoCapture("../test.mp4") 
    
    cnt, lab = run(weights='./runs/train/person_yolov5s_results/weights/best.pt', conf_thres=0.5, source='../carrier.jpg', exist_ok=True, line_thickness=2)
    length = len(cnt)
    dict = {}
    for i in range(length):
        dict[lab[i]] = cnt[i]
    return jsonify(dict)

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000, debug=True) #0.0.0.0
    