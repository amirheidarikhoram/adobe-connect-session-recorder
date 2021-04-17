# Adobe Connect Session Downloader
------------------------------------
Download Adobe Connect session video and sound in merged state as a single file easily.

## How It Works
-----------------

This script uses traditional way of downloading sounds and videos of a session by adding **/output/file_name.zip** to end of a session hyperlink. There is a special case that presenter shares the document to attendees instead of sharing his/her own screen while displaying the document, therefore there will be no video stream file(s) inside the **file_name.zip** downloaded before. The way I handled it here is first script downloads the zip file, extracts flv sounds and then puts them together so we can save the entire session sound as a single sound stream file.

Next step is to put video streams together and make a single video file of multiple parts. As I mentioned in some cases there is no video file available. The solution isto render the class session inside a sellenium browser and get screen shots of the **body** element page periodically so we can put all shots together and make video file with a specific frame rate.

## Notes And Maybe Some Todos
----------------------------

This way is highly depended on ffmpeg, sellenium and system resources so I think if I could create a webapp with a backend server on a virtual server to help students make session files wihtout relying on their own system resources would be great help but have'nt decided on that yet. Feel free to do this Todo if you can.