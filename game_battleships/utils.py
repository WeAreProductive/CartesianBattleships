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

def getKeySafe(data, key, defaultVal):
	return data[key] if not data is None and key in data else defaultVal

def ensureKey(data, key, defaultVal):
	if not data is None and not key in data:
		data[key] = defaultVal
