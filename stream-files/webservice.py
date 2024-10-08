import os
import subprocess
from http.server import SimpleHTTPRequestHandler, HTTPServer

IMAGE_FOLDER = "/home/pi-cam/streamfiles/images"
LATEST_IMAGE_PATH = os.path.join(IMAGE_FOLDER, "latest.jpg")
video_images_dir = '/home/pi-cam/timelaps-files-2/images'
video_output_path = './static/video.mp4'

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
        '-vf', 'scale=640:480', '-r', '24', video_output_path
    ]
    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"Video generated successfully at {video_output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating video: {e}")

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/generate-video':
            generate_video()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Video generation started. Check back shortly!")
        else:
            super().do_GET()

if __name__ == "__main__":
    PORT = 8808
    os.chdir("/home/pi-cam/streamfiles")
    httpd = HTTPServer(("0.0.0.0", PORT), MyHandler)
    print(f"Serving at port {PORT}")
    httpd.serve_forever()