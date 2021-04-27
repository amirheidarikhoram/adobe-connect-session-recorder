# Adobe Connect Session Recorder

Record Adobe Connect session video and merge it with session sound stream to a single file.

## Why and How

Not every adobe connect classroom is downloadable and sometimes there are some restrictions by the service provider. But always there is at least one solution for every problem. In this case if you add **/output/file.zip?download.zip** to end of the link of adobe connect session you can download sound and video streams but they are not merged and you have to work with ffmpeg and merge them together.
To give an example if your classroom link is something similar to *https://example.com/pt9pbrisgt0a/?session=breezbreezo8pdyckwkeus4dg5&proto=true* the download link will be *https://example.com/pt9pbrisgt0a/output/file.zip?download=zip* .

Sometimes presenter decides to share document instead of sharing his/her own screen while displaying document and that causes some problems with the file downloaded before; it just contains sound stream(s) of class but no video will be available.  

The way this script solves this problem is to get screenshots of the adobe connect browser player (rendered on selenium driver) and then putting frames (screenshots) together to produce a single video stream. Frames count varies based on resources of computer but the average frame rate is about 5.8 .

There are some issues with this solution. First issue is with internet connection. If your browser lose the internet connection, script can not sense and catch this event and stop recording process (precisely "doesn't catch it", not implemented yet)  so if it gets disconnected too many times player may exit the session. Another similar case is when player is in a "Loading" state, this case is not implemented yet too.
Second issue is about the frame rate, it takes some time for selenium to save screenshot of **body** element and this is the reason why frame rate is about 5.8 .

## How to
First install `ffmpeg`, `python` and firefox `geckodriver` and make sure they are all in **$PATH**.
Then install dependencies:
```bash
python -m pip install -r requirements.txt
```
or
```bash
pip install -r requirements.txt
```

After downloading class files extract all and move sound stream to scripts directory.
Setup execution permission for `start.sh`:
```bash
sudo chmod 755 start.sh
```
Run this command to start the process:
```bash
./start.sh <session_link> <sound_stream>
