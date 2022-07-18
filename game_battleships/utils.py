def convertToInt(val, defaultVal = 0):
	try:
		return int(val)
	except:
		return defaultVal

def convertHexBytesToString(text):
	return bytes.fromhex(text[2:]).decode("utf-8")
	#return bytearray.fromhex(str(text).replace("0x", "")).decode()

def convertStringToHexBytes(text):
	return "0x" + str(text).encode("utf-8").hex()
	#return "0x" + bytearray(text, "ascii").hex()

# get element from dictionary without errors
# key can be string to access the item directly
# or a list of strings to access the item if nested in structure of inner dictionaries
# if item not found then defaultVal will be returned
def getKeySafe(data, key, defaultVal = None):
	if isinstance(key, list):
		if len(key) > 1:
			data = getKeySafe(data, key[0], defaultVal)
			del key[0]
		else:
			key = key[0]
		return getKeySafe(data, key, defaultVal)
	return data[key] if not data is None and key in data else defaultVal

def ensureKey(data, key, defaultVal = None):
	if not data is None and not key in data:
		data[key] = defaultVal
