import subprocess
import re

def extract_scene_times(input_video):
    scene_times = []
    command = [
        'ffmpeg', '-i', input_video,
        '-filter:v', "select='gt(scene,0.4)',showinfo",
        '-f', 'null', '-'
    ]
    output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)

    # Parse output to extract scene times
    for match in re.finditer(r"pts_time:(\d+\.\d+)", output):
        time = float(match.group(1))
        scene_times.append(time)

    # Add the beginning and the length of the video
    video_info = subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_video], universal_newlines=True)
    video_length = float(video_info.strip())
    scene_times.insert(0, 0.0)  # Beginning of the video
    scene_times.append(video_length)  # End of the video
    return scene_times

def split_video(input_video, output_prefix, scene_times, codec='copy'):
    for i in range(len(scene_times) - 1):
        start_time = scene_times[i] + 0.10
        end_time = scene_times[i + 1] - 0.10
        output_file = f"{output_prefix}_{i + 1}.mp4"
        start_time_str = f"{start_time:.2f}"
        end_time_str = f"{end_time:.2f}"

        command = [
            'ffmpeg', '-i', input_video,
            '-ss', start_time_str,
            '-to', end_time_str,
            '-c:v', codec,
            output_file
        ]
        # print(command)
        subprocess.run(command)
        

input_video = 'input_video.mp4'
output_prefix = 'clip'
scene_times = extract_scene_times(input_video)
# print(scene_times)
split_video(input_video, output_prefix, scene_times, codec='libx264')
