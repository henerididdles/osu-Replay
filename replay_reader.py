import sys
import lzma
from pprint import pprint

import parser

def parseMouseData(mouse_data):
	action_buffer = mouse_data.split(',')

	mouse_actions = []

	for action in action_buffer[:-1]:
		w, x, y, z = action.split('|')

		w = int(w)
		x = float(x)
		y = float(y)

		click = '{0:04b}'.format(int(z))
		keys = ['M1', 'M2', 'K1', 'K2']
		presses = [int(x) for x in click]
		z = {key: value for (key, value) in zip(keys, presses)}

		mouse_actions.append({
			'time': w,
			'x': x,
			'y': y,
			'input': z
		})

	return mouse_actions

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
	data['mouse_data'] = parseMouseData(mouse_data)

	data['unk'] = parser.parseLong(osrStream)

	return data

def run():
	file = sys.argv[1]
	with open(file, 'rb') as f:
		replay_data = parseReplay(f)

	pprint(replay_data['mouse_data'])

run()