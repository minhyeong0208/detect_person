# 프로젝트명: 사람 이동 추적 및 VR 환경 표시

#### 개요
본 프로젝트는 한 공간 내에 순차적으로 배열된 카메라가 동시에 촬영한 영상을 분석하여, 사람이 몇 명 있는지와 몇 번 카메라에서 몇 번 카메라로 이동했는지 확인할 수 있는 프로그램을 개발하였다. 또한, 이러한 정보를 토대로 VR 환경에서 어떻게 사람들이 붐비고 이동했는지 시각화할 수 있다. 이 프로젝트는 Visual Studio Code에서 개발되었으며, 대부분의 코드는 Python을 사용하였다. 추가적으로 해당 프로그램은 크라우드 매니지먼트 관련 시뮬레이션에도 적용이 가능할 것이다.

#### 주요 기능
동시간대에 촬영된 여러 영상의 데이터를 통합 분석
사람 수 및 이동 경로 추적
VR 환경에서 이동 경로 시각화

#### 사용한 모델
YOLOv5s 모델을 사용하여 사람 탐지를 진행하였다.

#### 로컬 환경에서 테스트 방법
웹 환경에서 rendering.py 파일의 app.route('/')를 통해 프로젝트에 접속한다. 그러면 사용자는 동영상을 순차적으로 업로드할 수 있다.
'Detect' 버튼을 클릭하여 동영상에서 사람을 감지한다.
결과 창에서 사람이 몇 명 있는지와 몇 번 카메라에서 몇 번 카메라로 이동했는지를 확인할 수 있다.

---

#### 작동 방식
1. home.html에서 영상을 로컬로 불러옴 (이후 rendering.process_image()로 전달)
2. rendering.py에서 divide_frame.py를 이용하여 영상을 분할
3. 분할된 영상을 save_frame.py에 전달
4. save_frame.py에서 각 분할된 이미지를 detect.py의 run() 함수를 이용하여 객체 탐지
5. 탐지된 이미지 및 정보를 save_frame.py를 거쳐 rendering.py로 전송
6. 객체 정보를 tracking.py의 person_tracker() 함수를 이용하여 사람 객체의 이동 정보를 저장
7. 탐지된 이미지와 사람 객체 이동 정보를 result.html으로 전달
8. result.html에서 각 이미지와 프레임당 이동 정보를 프레임 단위로 보여줌
```
Usage - sources:
    $ python detect.py --weights yolov5s.pt --source 0                               # webcam
                                                     img.jpg                         # image
                                                     vid.mp4                         # video
                                                     screen                          # screenshot
                                                     path/                           # directory
                                                     list.txt                        # list of images
                                                     list.streams                    # list of streams
                                                     'path/*.jpg'                    # glob
                                                     'https://youtu.be/Zgi9g1ksQHc'  # YouTube
                                                     'rtsp://example.com/media.mp4'  # RTSP, RTMP, HTTP stream

Usage - formats:
    $ python detect.py --weights yolov5s.pt                 # PyTorch
                                 yolov5s.torchscript        # TorchScript
                                 yolov5s.onnx               # ONNX Runtime or OpenCV DNN with --dnn
                                 yolov5s_openvino_model     # OpenVINO
                                 yolov5s.engine             # TensorRT
                                 yolov5s.mlmodel            # CoreML (macOS-only)
                                 yolov5s_saved_model        # TensorFlow SavedModel
                                 yolov5s.pb                 # TensorFlow GraphDef
                                 yolov5s.tflite             # TensorFlow Lite
                                 yolov5s_edgetpu.tflite     # TensorFlow Edge TPU
                                 yolov5s_paddle_model       # PaddlePaddle
                                    
```