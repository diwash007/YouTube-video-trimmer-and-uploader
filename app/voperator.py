import os, shutil
from pytube import YouTube
from moviepy.editor import *


class Operator:
	""" Operator for downloading, editing and uploading the video """
	
	def __init__(self, video_loc):
		if video_loc != "yt" and video_loc != "local":
			print("Invalid input!!")
			exit(0)
		else:
			if video_loc == "yt":
				self.video_url = input("Enter YouTube video URL: ")
				self.download()
			print("[For local, video file should be called 'video.mp4']")
			self.clip_start = input("Enter clip start time: ")
			self.clip_end = input("Enter clip end time: ")
			self.title = input("Enter video title: ")
			self.subtitle = input("Enter video subtitle: ")

	def download(self):
		""" Downloads a YouTube video """
		print("Downloading video ...")
		try:
			video_data = YouTube(self.video_url)
			stream = video_data.streams.filter(res="720p").first()
			if stream == None:
				print("The video must have resolution of 16:9 and at least be 720p.")
				exit(0)
			stream.download(filename='video.mp4')
		except:
			print("Couldn't download the video. Please try again!")
			exit(0)

	def operate(self, operation):
		""" Operates if edit only or edit+upload """
		if operation == "1":
			self.edit()
			print("Edit successfull!")
		elif operation == "2":
			self.edit()
			self.upload()
		else:
			print("Invalid input!!")
			exit(0)

	def edit(self):
		""" Clips the downloaded video """
		try:
			clip = VideoFileClip("video.mp4").subclip(self.clip_start,self.clip_end)
			self.generate_intro()
			final_clip = concatenate_videoclips([self.intro, clip])
			final_clip.write_videofile(f"{self.title}.mp4")
			final_clip.save_frame("thumbnail.png", t=2)
			final_clip.close()
			clip.close()
			self.intro.close()
		except:
			print("Either 'video.mp4' is not in the current directory.")
			print("Or You entered Invalid input!!")
			exit(0)

	def generate_intro(self):
		""" generates intro for the video """
		clip = ColorClip((1280,720), (0,0,0), duration=5)
		clip = clip.set_duration(5)
		text_clip = TextClip(self.title, fontsize=90, color="white")
		text_clip = text_clip.set_pos('center').set_duration(5)
		text_clip1 = TextClip(self.subtitle, fontsize=60, color="white")
		text_clip1 = text_clip1.set_pos(('center', 400)).set_duration(5)
		self.intro = CompositeVideoClip([clip, text_clip, text_clip1])

	def upload(self):
		""" uploads video and thumbnail """
		try:
			# video upload
			description = input("\nEnter video description: ")
			keywords = input("Enter keywords for video [comma separated]: ")
			os.system(f'python helpers/upload_video.py\
						--file="{self.title}.mp4"\
		               	--title="{self.title} | {self.subtitle}"\
		               	--description="{self.title} | {self.subtitle} | {description}"\
		               	--keywords="{keywords}"\
		               	--category="20"\
		               	--privacyStatus="private"') # category: '20' is for gaming
		except:
			print("Couldn't upload the video. Please try again later.")
			exit(0)

		try:
			# thumbnail upload
			video_id = input("\nCopy paste the video ID: ")
			os.system(f'python helpers/upload_thumbnail.py --video-id="{video_id}"\
						--file="thumbnail.png"')
		except:
			print("Couldn't upload the thumbnail.")

	def backup(self):
		""" backs up files in a folder """
		files  = ["thumbnail.png", "video.mp4", f"{self.title}.mp4"]
		cwd = os.getcwd()
		os.system(f'mkdir "{self.title}"')
		for file in files:
			shutil.move(f"{cwd}\\{file}", f"{cwd}\\{self.title}\\{file}")
		print(f"Files backed up in folder '{self.title}'")