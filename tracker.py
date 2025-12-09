from ultralytics import YOLO
import cv2
import pandas as pd
import os

class VideoTracker:
    def __init__(self, model_name='yolov8n.pt'):
        self.model = YOLO(model_name)

    def process_video(self, video_path, output_path='tracking_results.csv'):
        # using stream=True to handle long videos without OOM
        results = self.model.track(source=video_path, persist=True, verbose=False, stream=True)
        
        tracking_data = []

        # Get FPS from video to calculate timestamps on the fly
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()
        if fps <= 0:
            fps = 30.0 # Default if failed

        frame_idx = 0
        for result in results:
            frame_idx += 1
            # Check if boxes exist in the result
            if result.boxes is None or result.boxes.id is None:
                continue

            # Extract info
            boxes = result.boxes.xywh.cpu().numpy()
            track_ids = result.boxes.id.int().cpu().numpy()
            class_ids = result.boxes.cls.int().cpu().numpy()
            
            current_time = (frame_idx - 1) / fps

            for box, track_id, class_id in zip(boxes, track_ids, class_ids):
                tracking_data.append({
                   'frame': frame_idx - 1, # 0-indexed
                   'track_id': track_id,
                   'class_id': class_id,
                   'x': box[0],
                   'y': box[1],
                   'w': box[2],
                   'h': box[3],
                   'timestamp': current_time
                })

        # Save to CSV
        df = pd.DataFrame(tracking_data)
        df.to_csv(output_path, index=False)
        print(f"Tracking completed. Results saved to {output_path}")
        return df

if __name__ == "__main__":
    # Test run
    tracker = VideoTracker()
    tracker.process_video("test_video.mp4")
