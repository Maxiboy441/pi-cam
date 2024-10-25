import os
import subprocess
from http.server import SimpleHTTPRequestHandler, HTTPServer
from PIL import Image
import numpy as np

IMAGE_FOLDER = "./images"
LATEST_IMAGE_PATH = os.path.join(IMAGE_FOLDER, "latest.jpg")
video_images_dir = '../timelaps-files/images'
video_output_path = './static/video.mp4'
DARK_THRESHOLD = 50

def generate_video():
    images = sorted(
        [os.path.join(video_images_dir, img) for img in os.listdir(video_images_dir) if img.endswith('.jpg')],
        key=lambda x: os.path.getmtime(x)
    )

    if len(images) == 0:
        print("No images found in the directory to create the video.")
        return

    ffmpeg_cmd = [
    'ffmpeg', '-y', '-pattern_type', 'glob', '-i', f'{video_images_dir}/*.jpg',
    '-vf', 'scale=640:480,setpts=1.5*PTS', '-r', '24', video_output_path
    ]

    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"Video generated successfully at {video_output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating video: {e}")

def is_dark(image_path, threshold=DARK_THRESHOLD):
    try:
        with Image.open(image_path) as img:
            grayscale_img = img.convert("L")
            pixel_data = np.array(grayscale_img)
            avg_brightness = np.mean(pixel_data)

            return avg_brightness < threshold

    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return False

def delete_dark_images(folder_path):
    deleted_count = 0
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            if is_dark(file_path):
                print(f"Deleting {filename} - too dark")
                os.remove(file_path)
                deleted_count += 1
    return deleted_count

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/generate-video':
            generate_video()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Video generation started. Check back shortly!")
        elif self.path == '/cleanup-timelapse':
            deleted_count = delete_dark_images(video_images_dir)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f"Cleanup completed. {deleted_count} dark images deleted.".encode())
        else:
            super().do_GET()

if __name__ == "__main__":
    PORT = 8808
    os.chdir("./")
    httpd = HTTPServer(("0.0.0.0", PORT), MyHandler)
    print(f"Serving at port {PORT}")
    httpd.serve_forever()