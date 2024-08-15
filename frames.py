import cv2
import os
from concurrent.futures import ThreadPoolExecutor
import glob
import time

# Path to the folder containing videos
videos_folder = r'C:\Users\onijo\OneDrive\Desktop\Deep_Fake_Forensics\dfdc_train_part_0'  # Replace with your folder path

# Folder to save frames
output_folder = 'Deepfake_faces'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Function to process a single video
def process_video(video_path):
    video_name = os.path.basename(video_path).split('.')[0]
    video_output_folder = os.path.join(output_folder, video_name)

    # Create a subfolder for each video
    if not os.path.exists(video_output_folder):
        os.makedirs(video_output_folder)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video {video_name}.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the number of frames to extract (10 seconds at 60 fps)
    total_frames = min(frame_count, int(10 * fps))

    # Function to save a single frame
    def save_frame(i, frame):
        frame_filename = os.path.join(video_output_folder, f'frame_{i:04d}.jpg')
        cv2.imwrite(frame_filename, frame)
        print(f"Saved: {frame_filename}")

    # Extract and save frames in parallel
    with ThreadPoolExecutor() as executor:
        futures = []
        for i in range(total_frames):
            ret, frame = cap.read()
            if not ret:
                print(f"Error: Could not read frame {i} in video {video_name}.")
                break
            futures.append(executor.submit(save_frame, i, frame))

        # Ensure all futures are completed
        for future in futures:
            future.result()

    # Release the video capture object
    cap.release()

    print(f"Finished processing video {video_name}.")

# Measure the time taken
start_time = time.time()

# Process all videos in the folder
video_files = glob.glob(os.path.join(videos_folder, '*.mp4'))  # Adjust the pattern if your videos are in a different format

with ThreadPoolExecutor() as executor:
    executor.map(process_video, video_files)

end_time = time.time()
print(f"Total time taken: {end_time - start_time} seconds")