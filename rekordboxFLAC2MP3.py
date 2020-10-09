import xml.etree.ElementTree as ET
import os
import copy

REKORDBOX_XML = 'C:\\Users\\Scott\\Music\\PioneerDJ\\rekordbox_old.xml'
NEW_XML = 'C:\\Users\\Scott\\Music\\PioneerDJ\\rekordbox.xml'

def main():
	xmlTree = ET.parse(REKORDBOX_XML)
	root = xmlTree.getroot()
	# parse the playlists into a dict with playlist names as keys and lists of track ids as values
	playlists = root[2][0]
	origPlaylistNames = []
	origPlaylistIdLists = []
	for node in playlists:
		pname = node.get('Name')
		origPlaylistNames.append(pname)
		pids = []
		for track in node:
			pids.append(track.get('Key'))
		origPlaylistIdLists.append(pids)

	pdict = dict(zip(origPlaylistNames, origPlaylistIdLists))
	print(pdict)
	
	# make a new playlist with '_MP3' appended to the playlist name if it does not exist
	for pname in origPlaylistNames:
		# if this is already an mp3 playlist do nothing
		if pname.endswith('_MP3'):
			continue
		mp3name = pname + '_MP3'
		# if mp3 version of this playlist exists do nothing
		if mp3name in origPlaylistNames:
			continue
		searchStr = "*/[@Name='" + pname + "']"
		origPL = playlists.find(searchStr)
		# add this playlist (NODE in rekordbox notation) to the element tree with an empty tracklist
		mp3list = ET.SubElement(playlists, 'NODE')
		mp3list.set('Name', mp3name)
		mp3list.set('Entries', str(origPL.get('Entries')))
		mp3list.set('Key', str(origPL.get('Key')))
		mp3list.set('Type', str(origPL.get('Type')))

	# navigate to the COLLECTIONS tag and iterate through tracks of the collection
	# the root will be DJ_PLAYLISTS
	# the second child will be collection
	collection = root[1]
	# get the playlist nodes in a list for convenience
	pNodes = root[2][0].findall('*')

	# track id at which to add a new track. Amount of existing entries +1. Incremented every new track created
	currId = int(collection.get('Entries')) + 1
	for track in collection:
		rawPath = track.get('Location')

		# skip file if not a flac
		if not rawPath.lower().endswith('.flac'):
			continue
		# get path in python parseable format
		flacPath = rawPath.replace('%20', ' ').replace('%26', '&').replace('%27', "'")
		if flacPath.startswith('file://localhost/'):
			flacPath = flacPath[17:]
		# get the original track id to figure out what playlists the new mp3 will need to be added to
		# don't convert if it isn't in any playlists to save time
		inPlaylist = False
		origId = track.get('TrackID')
		for pl in pNodes:
			searchStr = "*/[@Key='" + origId + "']"
			result = pl.findall(searchStr)
			if result == []:
				continue
			inPlaylist = True
			pname = pl.get('Name')
			print('Found track {} in playlist {}'.format(origId, pname))
			# find the mp3 version of the playlist and append the new mp3 id to it
			mp3listName = pname + '_MP3'
			searchStr = "*/[@Name='" + mp3listName + "']"
			mp3list = playlists.find(searchStr)
			newTrack = ET.SubElement(mp3list, 'TRACK')
			newTrack.set('Key', str(currId))
		if not inPlaylist:
			continue
		# at this point, the file was found in at least one playlist
		# convert the file if mp3 doesn't exist already
		mp3Path = flacPath[:-5] + '.mp3'
		# if not os.path.exists(mp3Path):
		# 	# convert the flac to a 320 kpbs mp3
		ffmpegFLAC2MP3(flacPath, mp3Path)
		# else:
		# 	continue
		# copy the old xml track entry and modify the necessary fields
		newTrack = copy.deepcopy(track)
		newTrack.set('TrackID', str(currId))
		newTrack.set('Location', 'file://localhost/' + mp3Path.replace(' ', '%20').replace('&', '%26').replace(",", "%27"))
		newTrack.set('Kind', "MP3 File")
		newTrack.set('BitRate', "320")
		collection.append(newTrack)
		# increment the current song id number
		currId += 1
	collection.set('Entries', str(currId-1))
	xmlTree.write(NEW_XML)
		

# convert FLAC at inFlac path to 320 kpbs mp3 at outmp3 path
def ffmpegFLAC2MP3(inFlac, outmp3):
	print(inFlac)
	print(outmp3)
	os.system('ffmpeg -i "{}" -ab 320k -map_metadata 0 -id3v2_version 3 "{}" -nostdin'.format(inFlac, outmp3))



if __name__ == '__main__':
	main()