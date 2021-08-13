import os
from pytube import YouTube
from moviepy.editor import *

class Operator:
	""" Operator for downloading and editing the video """
	
	def __init__(self):
		self.video_url = input("Enter YouTube video URL: ")
		self.clip_start = input("Enter clip start time: ")
		self.clip_end = input("Enter clip end time: ")
		self.title = input("Enter video title: ")
		self.subtitle = input("Enter video subtitle: ")

	def download(self):
		""" Downloads a YouTube video """
		video_data = YouTube(self.video_url)
		stream = video_data.streams.filter(res="720p").first()
		stream.download(filename='video.mp4')

	def edit(self):
		""" Clips the downloaded video """
		clip = VideoFileClip("video.mp4").subclip(self.clip_start,self.clip_end)
		clip = clip.resize(newsize=(1280,720))
		clip.write_videofile("video_edited.mp4")
		clip.close()
		# os.remove("video.mp4")

	def generate_intro(self):
		""" generates intro for the video """
		clip = ColorClip((1280,720), (0,0,0), duration=5)
		clip = clip.set_duration(5)

		text_clip = TextClip(self.title, font="Helvetica", fontsize=90, color="white")
		text_clip = text_clip.set_pos('center').set_duration(5)

		text_clip1 = TextClip(self.subtitle, font="Helvetica", fontsize=60, color="white")
		text_clip1 = text_clip1.set_pos(('center', 400)).set_duration(5)

		intro = CompositeVideoClip([clip, text_clip, text_clip1])
		intro.write_videofile(filename="intro.mp4", fps=1)

		video_clip = VideoFileClip("video_edited.mp4")
		final_clip = concatenate_videoclips([intro, video_clip])
		final_clip.write_videofile(f"{self.title}.mp4")
		final_clip.save_frame("thumbnail.png", t=2)

		intro.close()
		video_clip.close()
		final_clip.close()
		os.remove("video_edited.mp4")
		os.remove("intro.mp4")