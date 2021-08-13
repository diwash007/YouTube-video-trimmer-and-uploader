import os
from video_maker import Operator

if __name__ == "__main__":

	op = Operator()
	choice = input("Enter\n\t1 for YouTube video\n\t2 for local video\n:")
	if choice == "1":
		op.download()
	op.edit()
	op.generate_intro()

	# video upload
	description = input("\nEnter your channel name: ")
	keywords = input("Enter keywords for video [comma separated]: ")
	original_creator = input("Enter Original Creator channel name: ")
	os.system(f'python upload_video.py\
				--file="{op.title}.mp4"\
               	--title="{op.title} | {op.subtitle} | {description}"\
               	--description="{op.title} \\n {op.subtitle} \\n {description} \\n original video by {original_creator}: {op.video_url}"\
               	--keywords="{keywords}"\
               	--category="20"\
               	--privacyStatus="public"') # category: '20' is for gaming
	os.remove(f"{op.title}.mp4")

	# thumbnail upload
	video_id = input("\nCopy paste the video ID: ")
	os.system(f'python upload_thumbnail.py --video-id="{video_id}"\
				--file="thumbnail.png"')
	os.remove("thumbnail.png")