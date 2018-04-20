import sys
import lzma

import parser

def parseReplay(osrStream):
	data = {}
	data['mode'] = parser.parseByte(osrStream)
	data['version'] = parser.parseInt(osrStream)
	data['beatmap_md5'] = parser.parseString(osrStream)
	data['player_name'] = parser.parseString(osrStream)
	data['replay_md5'] = parser.parseString(osrStream)
	data['300s'] = parser.parseShort(osrStream)
	data['100s'] = parser.parseShort(osrStream)
	data['50s'] = parser.parseShort(osrStream)
	data['geki'] = parser.parseShort(osrStream)
	data['katu'] = parser.parseShort(osrStream)
	data['misses'] = parser.parseShort(osrStream)
	data['score'] = parser.parseInt(osrStream)
	data['combo'] = parser.parseShort(osrStream)
	data['fc'] = parser.parseByte(osrStream)
	data['mods'] = parser.parseInt(osrStream)
	data['lifebar'] = parser.parseString(osrStream)
	data['timestamp'] = parser.parseLong(osrStream)
	
	data_length = parser.parseInt(osrStream)
	data_buffer = osrStream.read(data_length)
	mouse_data = str(lzma.decompress(data_buffer), 'utf-8')

	data['unk'] = parser.parseLong(osrStream)

	return data

def run():
	file = sys.argv[1]
	with open(file, 'rb') as f:
		replay_data = parseReplay(f)

	print(replay_data)

run()