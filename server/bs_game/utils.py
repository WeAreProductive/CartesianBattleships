def convertToInt(val, defaultVal = 0):
	try:
		return int(val)
	except:
		return defaultVal

def convertAsciiByteTextToString(text):
	 return bytearray.fromhex(str(text).replace("0x", "")).decode()
	 
def convertStringToAsciiByteText(text):
	return "0x" + bytearray(text, "ascii").hex()
