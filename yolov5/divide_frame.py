import cv2
import os

def divide_frame(videos):
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

    return frames_list

    