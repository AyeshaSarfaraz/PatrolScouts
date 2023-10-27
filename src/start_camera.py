import socket
import time

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput

picam2 = Picamera2()
video_config = picam2.create_video_configuration({"size": (480, 270)})
picam2.configure(video_config)
encoder = H264Encoder(40000000, False, 10)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", 1430))
    sock.listen()

    picam2.encoders = encoder

    while True:  # Run indefinitely
        conn, addr = sock.accept()
        stream = conn.makefile("wb")
        encoder.output = FileOutput(stream)
        picam2.start_encoder(encoder)
        picam2.start()
        
        try:
            while True:
                time.sleep(1)  # You can adjust the sleep interval if needed
        except KeyboardInterrupt:
            # Press Ctrl+C to stop the script
            pass
        
        picam2.stop()
        picam2.stop_encoder()
        conn.close()
