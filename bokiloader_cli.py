import os
import requests
import argparse
import platform
from pytube import YouTube
from pydub import AudioSegment
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error


def download_image(image_url, save_path):
    print("[INFO] Entering download_image")
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as img_file:
            img_file.write(response.content)
        print(f"[SUCCESS] Downloaded thumbnail: {save_path}")
    else:
        print("[ERROR] Failed to download thumbnail.")
        return None
    print("[INFO] Exiting download_image")
    return save_path


def add_cover_to_mp3(mp3_path, cover_path):
    print("[INFO] Entering add_cover_to_mp3")
    audio = MP3(mp3_path, ID3=ID3)
    try:
        audio.add_tags()
    except error as ce:
        print("[ERROR] Error adding the audio tag")
        print(ce)
        pass
    with open(cover_path, 'rb') as img_file:
        audio.tags.add(APIC(
            encoding=3,  # UTF-8
            mime='image/jpeg',  # MIME type of the image
            type=3,  # Cover front
            desc=u'Cover',
            data=img_file.read()
        ))
    audio.save()
    print(f"[SUCCESS] Added cover to MP3: {mp3_path}")
    print("[INFO] Exiting add_cover_to_mp3")


def download_and_convert(link, destination):
    print(f"Downloading video from: {link}")

    try:
        yt = YouTube(link)
        stream = yt.streams.get_by_itag(251)  # audio-only stream

        video_title = yt.title
        video_chanel = yt.author
        if "-" in video_title:
            music_name = video_title.title().replace(" ", "")
        else:
            music_title = video_title.title().replace(" ", "")
            music_name = video_chanel + " - " + music_title
        thumbnail_url = yt.thumbnail_url

        downloaded_file = stream.download(output_path=destination, filename=music_name)
        base, ext = os.path.splitext(downloaded_file)
        converted_file = base + '.mp3'

        print("Converting to mp3...")
        audio = AudioSegment.from_file(downloaded_file)
        audio.export(converted_file, format="mp3", bitrate="192k")

        print(f"Conversion finished: {converted_file}")

        # Download the thumbnail and embed it in the MP3
        cover_path = download_image(thumbnail_url, base + '.jpg')
        if cover_path:
            add_cover_to_mp3(converted_file, cover_path)
            os.remove(cover_path)  # Clean up cover image file after embedding

        os.remove(downloaded_file)  # Clean up the original downloaded file

        print(f"Successfully downloaded and converted: {converted_file}")

    except Exception as e:
        print(f"Failed to download or convert video: {str(e)}")


def get_download_folder():
    system = platform.system()
    if system == "Windows":
        download_folder = os.path.join(os.environ['USERPROFILE'], 'Downloads')
    else:
        download_folder = os.path.expanduser('~/Downloads')
    return download_folder


default_download_folder = get_download_folder()


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Download and convert YouTube videos to MP3.")

    # Add arguments
    parser.add_argument('url',
                        help="The URL of the YouTube video to download.")
    parser.add_argument('--destination',
                        default=default_download_folder,
                        help="The destination folder for the downloaded and converted file. "
                             "Default is the download directory.")

    # Parse arguments
    args = parser.parse_args()

    # Call the download and convert function with parsed arguments
    download_and_convert(args.url, args.destination)


if __name__ == "__main__":
    main()
