# RekordboxFlacToMp3
Simple script to convert FLAC files to MP3 while maintaining their Rekordbox metadata

**Dependencies**
Python 3.8
ffmpeg

**Background**

When I first began DJ-ing last year, I would always purchase FLAC files instead of MP3s whenever they were available. This worked out fine when I was learning the ropes at home on my DDJ-400. However, when I went to an open decks event and got the opportunity to use CDJ-2000s, I learned that they did not support FLAC format. I wanted to be able to use CDJ's, however if I simply converted all of my tracks then I would lose the metadata that I had spent months generating in Rekordbox. I use cue points and track comments extensively, and I wanted a way to convert my tracks to MP3s while maintaining their metadata. So I made this script.

**Usage**

Simply run the python script, and it will process any FLAC tracks that are part of a playlist in the xml located at REKORDBOX_XML. It will create a new entry for the track in NEW_XML, convert the FLAC file associated with the entry to a 320 kbps MP3, and add the track to a playlist in NEW_XML that has "\_MP3" appended to the old playlist name. All of your old metadata associated with your tracks will be copied to your new xml. Once you have your new xml, you can change your rekorbox preferences to use that xml, or you can change the filename to the one that rekordbox is already looking for. The script should be able to get to the vast majority of your tracks, but you might still have to clean up a few by hand after the fact. Still, the script greatly reduced the amount of manual conversion I had to do, and I hope it helps you as well if you find yourself in the same situation.
