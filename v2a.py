"""
VIDEO TO ASCII.
"""
from PIL import Image, ImageFont, ImageDraw
from constants import ASCII, ASCII_LEN, ASCII_HEIGHT, ASCII_WIDTH
import argparse
import cv2
import numpy as np

parser = argparse.ArgumentParser(description='video to ascii')
parser.add_argument('input', help='input video file')
parser.add_argument('--output', help='output video file name (without extension)')
args = parser.parse_args()
input = args.input
file_name = input.split('.')[0]
output = args.output if args.output else f'{file_name}_ascii'

class V2A:
    def __init__(self, input, output):
        self.input = input
        self.output = output
        self.cap = cv2.VideoCapture(input)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.font_scale_factor = self.width / 3840
        self.font_size = int(24 * self.font_scale_factor)
        self.font_center = (3 / 16) * self.width
        self.monospace_font = ImageFont.truetype('SpaceMono-Regular.ttf', self.font_size)

    def _pixel_to_ascii(self, pixel):
        return ASCII[int(pixel / 255 * ASCII_LEN)]
    
    def _frame_to_ascii(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ascii_frame = ''
        for i in range(ASCII_HEIGHT):
            for j in range(ASCII_WIDTH):
                ascii_frame += self._pixel_to_ascii(gray[i, j])
            ascii_frame += '\n'
        return ascii_frame

    def convert(self):
        print(f'[ :| ] converting {self.input} to ascii...')
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(f'{self.output}.mp4', fourcc, self.fps, (self.width, self.height))
        frame_count = 0
        while True:
            print(f'[ :3 ] {frame_count / self.total_frames * 100:.1f}% done', end='\r')
            ret, frame = self.cap.read()
            if not ret:
                break
            resized_frame = cv2.resize(frame, (ASCII_WIDTH, ASCII_HEIGHT))
            ascii_frame = self._frame_to_ascii(resized_frame)
            text_frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            pil_img = Image.fromarray(text_frame)
            draw = ImageDraw.Draw(pil_img)
            for i, line in enumerate(ascii_frame.split('\n')):
                draw.text((self.font_center, i * self.font_size), line, font=self.monospace_font, fill=(255, 255, 255))
            text_frame = np.array(pil_img)
            out.write(text_frame)
            frame_count += 1
        self.cap.release()
        out.release()
        print(f'[ :) ] {self.input} converted to ascii, saved as {self.output}.mp4')

v2a = V2A(input, output)
v2a.convert()
print('[ :) ] done')
