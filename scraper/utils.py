import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import os
import re

def get_video_ids_from_channel(channel_url):
	"""Extracts all video IDs from a YouTube channel using yt-dlp."""
	try:
		# Options to prevent downloading and just extract metadata
		ydl_opts = {
			'quiet': True,  # Suppress yt-dlp's output
			'no_warnings': True,
			'extract_flat': True,  # Extract only the video information, no download
			'dump_single_json': True  # Output the result as JSON
		}

		# Use yt-dlp to extract the video metadata from the channel
		with yt_dlp.YoutubeDL(ydl_opts) as ydl:
			result = ydl.extract_info(channel_url, download=False)

			# Recursive function to extract video IDs
			def extract_video_ids(entries):
				video_ids = []
				for entry in entries:
					if '_type' in entry and entry['_type'] == 'url' and 'id' in entry:
						# Extract the video ID
						video_ids.append(entry['id'])
					elif 'entries' in entry:
						# If this entry contains more nested entries, recurse
						video_ids.extend(extract_video_ids(entry['entries']))
				return video_ids

			# Extract video IDs from the top-level entries
			video_ids = extract_video_ids(result['entries'])
			return video_ids

	except Exception as e:
		print(f"An error occurred: {e}")
		return []

def get_video_details(video_id):
	"""Fetches the title and publish date of a YouTube video using yt-dlp."""
	try:
		# Options to prevent downloading the video, just get metadata
		ydl_opts = {
			'quiet': True,  # Suppress yt-dlp output
			'no_warnings': True,  # Suppress warnings
			'force_generic_extractor': True,  # Make sure to only extract info
		}

		# YouTube video URL
		video_url = f"https://www.youtube.com/watch?v={video_id}"

		# Use yt-dlp to extract metadata
		with yt_dlp.YoutubeDL(ydl_opts) as ydl:
			info = ydl.extract_info(video_url, download=False)
			title = info.get('title')
			publish_date = info.get('upload_date')  # Date in YYYYMMDD format

			# Format the publish date nicely
			formatted_publish_date = f"{publish_date[:4]}-{publish_date[4:6]}-{publish_date[6:]}"

			return title, formatted_publish_date

	except Exception as e:
		raise Exception(f"Error fetching video info: {str(e)}")

def extract_channel_name_from_url(url):
	if "@" in url:
		return url.split("@")[1].split("/")[0]
	return url  # Return the original input if it doesn't contain '@'

import time
import random

def exponential_backoff(func, max_retries=5, base_delay=1, max_delay=60):
	"""
	Implements exponential backoff for the given function.
	"""
	def wrapper(*args, **kwargs):
		for attempt in range(max_retries):
			try:
				return func(*args, **kwargs)
			except Exception as e:
				if attempt == max_retries - 1:
					raise e
				delay = min(base_delay * (2 ** attempt) + random.uniform(0, 1), max_delay)
				print(f"Attempt {attempt + 1} failed. Retrying in {delay:.2f} seconds...")
				time.sleep(delay)
	return wrapper

def download_youtube_transcript(video_id, download_path):
	print(f"Calling download_youtube_transcript for video_id: {video_id}")
	"""Downloads and saves the transcript of a YouTube video."""
	
	@exponential_backoff
	def fetch_and_save_transcript():
		# Get video details
		title, published_date = get_video_details(video_id)
		url = f"https://www.youtube.com/watch?v={video_id}"

		# Sanitize the title to make it safe for file names
		sanitized_title = sanitize_filename(title)

		# Create filename
		filename = os.path.join(download_path, f"{sanitized_title}_{published_date}_transcript.txt")

		# Check if file already exists
		if os.path.exists(filename):
			print(f"Transcript already exists at {filename}. Skipping download.")
			return True, None

		# Fetch transcript
		transcript = YouTubeTranscriptApi.get_transcript(video_id)

		# Format transcript
		formatter = TextFormatter()
		text_transcript = formatter.format_transcript(transcript)

		# Prepare content with video ID, title, date, and URL
		content = f"Video ID: {video_id}\nTitle: {title}\nPublished Date: {published_date}\nURL: {url}\n\n{text_transcript}"

		# Save transcript to a file
		os.makedirs(download_path, exist_ok=True)
		with open(filename, "w", encoding="utf-8") as f:
			f.write(content)
		print(f"Transcript saved to {filename}")
		return True, None

	try:
		return fetch_and_save_transcript()
	except Exception as e:
		error_message = str(e)
		print(f"Transcript not available for {video_id} after multiple attempts: {error_message}")
		return False, error_message

def sanitize_filename(filename):
	"""
	Removes or replaces characters in a string that are not allowed in file names.
	"""
	# Remove any invalid characters (anything other than alphanumeric, dash, underscore, or space)
	return re.sub(r'[\\/*?"<>|]', "_", filename)

# if __name__ == "__main__":
# 	channel_url = "https://www.youtube.com/@nntalebproba"
# 	video_id = "TMvQeH9oo2w"
# 	title, published_date = get_video_details(video_id)
# 	print(f"Title: {title}, Published Date: {published_date}")