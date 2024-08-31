import subprocess
import threading
import time

# Function to record video
def record_video(output_file, duration=60):
    command = [
        'ffmpeg', '-f', 'dshow', '-i', 'video="USB Video Device"',  # Adjust for your virtual camera
        '-t', str(duration), 
        '-c:v', 'libx264', 
        '-preset', 'fast', 
        '-crf', '23', 
        output_file
    ]
    subprocess.run(command)

# Function to take a screenshot
def take_screenshot(video_file, screenshot_file, timestamp='00:00:01'):
    command = [
        'ffmpeg', '-i', video_file, 
        '-ss', timestamp, 
        '-vframes', '1', 
        screenshot_file
    ]
    subprocess.run(command)


def run_tasks_concurrently():
    # File paths
    video_file = 'output.mp4'
    screenshot_file = 'screenshot.png'

    # Create threads for recording video and taking screenshot
    video_thread = threading.Thread(target=record_video, args=(video_file, 60))
    screenshot_thread = threading.Thread(target=take_screenshot, args=(video_file, screenshot_file, '00:00:01'))

    # Start threads
    video_thread.start()
    screenshot_thread.start()

    # Wait for threads to complete
    video_thread.join()
    screenshot_thread.join()

if __name__ == '__main__':
    run_tasks_concurrently()





"""command = [
    'ffmpeg/bin/ffmpeg.exe',
    '-f', 'dshow',                   # DirectShow format
    '-i', f'video={InputDeviceCamera}:audio={InputDeviceMic}',  # Replace with the correct names for your devices
    '-c:v', 'libx264',               # Video codec (H.264)
    '-preset', 'ultrafast',          # Fast encoding preset
    '-t', '00:00:15',                # Duration of the recording (30 seconds)
    'output.mp4', "-y"               # Output file
]"""