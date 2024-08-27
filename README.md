# Boki Downloader

### Version
0.3.0a

I advise you to change the location in the script as it is hardcoded, 
and I'm too tired to make it dynamic right now. 
For now, you need to have ffmpeg because the script need to use another audio codec to be usable anywhere.

How to use the script `BokiLoader.py`:
* Launch the script via a terminal
  * ~~~~
    ../BokiDownloader/python BokiLoader.py
* Enter the YouTube video link when asked
* Enjoy

How to use the CLI `bokiloader_cli.py`:
* Launch the script via python and put the url of the YouTube video 
and the file will be downloaded into your `C:/Users/{User}/Download/`
  ~~~~
  python bokiloader_cli.py [url]
* Launch the script via python and put the url of the YouTube video
and add the destination folder were you want the mp3 to get downloaded
  ~~~~
  python bokiloader_cli.py [url] --dest [destination_folder]

### Basic Spec

1. [x] Can download a single link
2. [x] Add correctly name and author
3. [x] Add cover, title and artist to mp3 tags
4. [x] Make the main script into a CLI `bokiloader.py`

### Work in progress (just to not say I won't probably make them)
1. [ ] Can download into a mp4
2. [ ] Can download a playlist
3. [ ] Is linked to an API so it works from _**BOKIVY**_

### Requirement
1. [x] Python 3.12
2. [x] Ffmpeg installed
3. [ ] Knows how to launch a fucking python script
4. [ ] Knows how to modify this script as it's not a release 1.0 local change must be made
5. [x] (Optional) Don't be a retard

### Change log
| Version |                                                                                               Change                                                                                               |
|:-------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| 0.3.0a  | Metadata tags such as the cover, title and artist are added onto the mp3 file <br/> Retrieve Author and Title improved, Compiled by tag added, audio quality from pytube up from 48kbps to 160kbps |
| 0.2.0a  |                                                   Initial commit version were the main script do everything I want for now plus the CLI version                                                    |
| 0.1.0a  |                                                                Local change where I remake the previous shitty script I made before                                                                |
