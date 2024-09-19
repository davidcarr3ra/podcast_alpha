from utils import *
import os
import json

def download_channel_transcripts(channel_url):
	print(f"Calling download_channel_transcripts with input: {channel_url}")
	"""Fetches all video IDs from a channel and downloads transcripts."""
	failed_downloads = []
	try:
		channel_name = extract_channel_name_from_url(channel_url)
		print(f"Channel name: {channel_name}")

		# Create directory for channel
		channel_dir = os.path.join("..", "output", channel_name)
		os.makedirs(channel_dir, exist_ok=True)

		# Create directory for transcripts
		transcripts_dir = os.path.join(channel_dir, "transcripts")
		os.makedirs(transcripts_dir, exist_ok=True)

		# Get existing video IDs
		existing_video_ids = set()
		for filename in os.listdir(transcripts_dir):
			if filename.endswith(".txt"):
				with open(os.path.join(transcripts_dir, filename), 'r') as f:
					first_line = f.readline().strip()
					if first_line.startswith("Video ID:"):
						video_id = first_line.split(":")[1].strip()
						existing_video_ids.add(video_id)
		print(f"Existing video IDs: {len(existing_video_ids)}")

		# Fetch all videos from the channel
		all_video_ids = set(get_video_ids_from_channel(channel_url))
		print(f"Total video IDs: {len(all_video_ids)}")

		# Get new video IDs
		new_video_ids = all_video_ids - existing_video_ids
		print(f"New video IDs to process: {len(new_video_ids)}")

		# Loop through each new video in the channel and download transcripts
		for video_id in new_video_ids:
			success, error = download_youtube_transcript(video_id, transcripts_dir)
			if not success:
				video_url = f"https://www.youtube.com/watch?v={video_id}"
				failed_downloads.append((video_url, error))

		print(f"All new transcripts for {channel_name} have been downloaded.")
		if failed_downloads:
			print(f"Failed to download transcripts for {len(failed_downloads)} videos.")
			print("Failed video URLs and errors:")
			for url, error in failed_downloads:
				print(f"{url}: {error}")
			
			# Save failed downloads to a file
			failed_downloads_file = os.path.join(channel_dir, f"{channel_name}_failed_downloads.json")
			with open(failed_downloads_file, 'w', encoding='utf-8') as f:
				json.dump(failed_downloads, f, ensure_ascii=False, indent=4)
			print(f"Failed downloads saved to {failed_downloads_file}")
	except Exception as e:
		error_message = str(e)
		print(f"Error fetching videos or transcripts from channel: {error_message}")
		failed_downloads.append((channel_url, error_message))
	
	return failed_downloads

def process_channels(channel_urls):
	print("Starting main execution")
	for channel_url in channel_urls:
		print(f"Processing channel: {channel_url}")
		download_channel_transcripts(channel_url)
	print("Main execution completed")

if __name__ == "__main__":
	CHANNEL_URLS = [
		# "https://www.youtube.com/@nntalebproba",
		# "https://www.youtube.com/@Bankless",
		# "https://www.youtube.com/@TheRollupCo",
		"https://www.youtube.com/@empirepod",
		"https://www.youtube.com/@LoganJastremski",
		"https://www.youtube.com/@LightspeedpodHQ",
		"https://www.youtube.com/@nftnow",
		"https://www.youtube.com/@UnchainedCrypto",
		"https://www.youtube.com/@0xresearchPodcast",
		"https://www.youtube.com/@theblockcrunchpodcast",
		"https://www.youtube.com/@UncommonCore",
		"https://www.youtube.com/@zeroknowledgefm",
		"https://www.youtube.com/@a16zcrypto",
	]
	process_channels(CHANNEL_URLS)