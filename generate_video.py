import cv2
import numpy as np

def create_bouncing_ball_video(filename="test_video.mp4", duration=10, fps=30, width=640, height=480):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))

    # Ball properties
    radius = 20
    color = (0, 0, 255) # Red
    pos = np.array([width // 2, height // 2], dtype=float)
    vel = np.array([5, 4], dtype=float)

    # Second ball
    radius2 = 15
    color2 = (0, 255, 0) # Green
    pos2 = np.array([100, 100], dtype=float)
    vel2 = np.array([-3, 6], dtype=float)


    for i in range(duration * fps):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Update ball 1
        pos += vel
        if pos[0] - radius < 0 or pos[0] + radius > width:
            vel[0] = -vel[0]
        if pos[1] - radius < 0 or pos[1] + radius > height:
            vel[1] = -vel[1]
        
        cv2.circle(frame, (int(pos[0]), int(pos[1])), radius, color, -1)

        # Update ball 2
        pos2 += vel2
        if pos2[0] - radius2 < 0 or pos2[0] + radius2 > width:
            vel2[0] = -vel2[0]
        if pos2[1] - radius2 < 0 or pos2[1] + radius2 > height:
            vel2[1] = -vel2[1]

        cv2.circle(frame, (int(pos2[0]), int(pos2[1])), radius2, color2, -1)
        
        # Add frame number text
        cv2.putText(frame, f"Frame: {i}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        out.write(frame)

    out.release()
    print(f"Video saved to {filename}")

if __name__ == "__main__":
    create_bouncing_ball_video()
