import cv2
import os
from detect import run

def save_frame(frames_list):
    results_list = []
    total_person=[]
    move_info=[]
    for i, frames in enumerate(frames_list):
        results = []
        video_person={}
        for j, frame in enumerate(frames):
            save_dir = '../image/frame/'  # 이미지를 저장할 경로와 파일명
            frame_path = os.path.join(save_dir, f"frame_{i}_{j}.png")
            cv2.imwrite(frame_path, frame)
            cnt, lab, save_path = run(weights='yolov5s.pt', conf_thres=0.5, source=frame_path, exist_ok=True,
                                      line_thickness=2)
            result = {
                'cnt': cnt,
                'lab': lab,
                'save_path': save_path
            }
            key = j
            if lab[0] == 'person':
                value = cnt[0]
            else:
                value = 0
            video_person[key]=value
            results.append(result)
        total_person.append(video_person)
        #print(total_person)
        
        results_list.append(results)
    
    return results_list, total_person

    