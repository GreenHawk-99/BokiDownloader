import os
import requests
from pytube import YouTube
from pydub import AudioSegment
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error

# https://www.youtube.com/watch?v=kdIK-aw5jLk
# Test Data from which info comment come from
# https://www.youtube.com/watch?v=oCbKbXEFY0k

destination = "C:/Users/green/Music/YTDownloaderV2/"


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


def add_or_replace_cover_in_mp3(mp3_path, cover_path):
    print("[INFO] Entering add_or_replace_cover_in_mp3")
    audio = MP3(mp3_path, ID3=ID3)

    # Ensure ID3 tags are present
    if not audio.tags:
        audio.add_tags()

    # Remove any existing cover image
    audio.tags.delall("APIC")

    # Add the new cover image
    with open(cover_path, 'rb') as img_file:
        audio.tags.add(APIC(
            encoding=3,  # UTF-8
            mime='image/jpeg',  # MIME type of the image
            type=3,  # Cover front
            desc=u'Cover',
            data=img_file.read()
        ))

    # Save the changes to the file
    audio.save(v2_version=3)  # Explicitly saving ID3v2.3 for compatibility
    print(f"[SUCCESS] Added or replaced cover in MP3: {mp3_path}")
    print("[INFO] Exiting add_or_replace_cover_in_mp3")


def get_audio():
    print("[INFO] Entering get_audio")
    try:
        yt = YouTube(link)
        stream = yt.streams.filter(only_audio=True).first()

        video_title = yt.title
        video_chanel = yt.author
        thumbnail_url = yt.thumbnail_url

        if "-" in video_title:
            music_name = video_title.title().replace(" ", "")
            music_info = video_title.split("-")
            music_artist = music_info[0]
            music_title = music_info[1]
        else:
            music_name = f"{video_chanel}-{video_title.title().replace(' ', '')}"
            music_artist = video_chanel
            music_title = video_title.title().replace(" ", "")

        def download_and_convert():
            print("[INFO] Entering download_and_convert")
            downloaded_file = stream.download(output_path=destination, filename=music_name)
            base, ext = os.path.splitext(downloaded_file)
            converted_file = base + '.mp3'

            try:
                print("[INFO] Converting to mp3")
                audio = AudioSegment.from_file(downloaded_file)
                audio.export(converted_file, format="mp3", bitrate="192k")
                print(f"[SUCCESS] Conversion finished: {converted_file}")

                # Download and add the cover
                cover_path = download_image(thumbnail_url, base + '.jpg')
                if cover_path:
                    add_or_replace_cover_in_mp3(converted_file, cover_path)
                    os.remove(cover_path)  # Clean up the cover image
                    print(f"[DELETE] Cleaned up cover image file: {cover_path}")
            except Exception as ex:
                print(f"[ERROR] An error occurred during conversion: {str(ex)}")
                if os.path.exists(downloaded_file):
                    os.remove(downloaded_file)
                    print(f"[DELETE] Removed unconverted file: {downloaded_file}")
                if os.path.exists(converted_file):
                    os.remove(converted_file)
                    print(f"[DELETE] Removed partial MP3 file: {converted_file}")
            else:
                # Clean up the downloaded file after successful conversion
                try:
                    os.remove(downloaded_file)
                    print(f"[DELETE] Removed original downloaded file: {downloaded_file}")
                except Exception as cleanup_ex:
                    print(f"[ERROR] Error while removing original file: {cleanup_ex}")
            print(f"[SUCCESS] {music_name} has been downloaded successfully into: {converted_file}")
            print("[INFO] Exiting download_and_convert")

        download_and_convert()
    except Exception as e:
        print("[ERROR] Error downloading video")
        if e.args[0].__contains__("regex_search"):
            print("[ERROR] The url provided is invalid")

    finally:
        print("[INFO] Exiting get_audio")


if __name__ == "__main__":
    # Input of the video url
    link = input("Enter the link of the video: ")
    # Start the download event
    get_audio()
