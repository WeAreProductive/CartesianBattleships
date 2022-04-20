class ConsoleColors:
	NC           = "\033[0m"
	Black        = "\033[0;30m"
	Red          = "\033[0;31m"
	Green        = "\033[0;32m"
	Brown        = "\033[0;33m"
	Blue         = "\033[0;34m"
	Purple       = "\033[0;35m"
	Cyan         = "\033[0;36m"
	LightGray    = "\033[0;37m"
	DarkGray     = "\033[1;30m"
	LightRed     = "\033[1;31m"
	LightGreen   = "\033[1;32m"
	Yellow       = "\033[1;33m"
	LightBlue    = "\033[1;34m"
	LightPurple  = "\033[1;35m"
	LightCyan    = "\033[1;36m"
	White        = "\033[1;37m"
	# game specific
	rups_msg = "\033[0;37;44m"
	rups_val = "\033[1;97;44m"
	test = "\033[0;97;46m"
	sep = "\033[0;37;45m"
	exception = "\033[0;30;41m"
	sep_verify = "\033[0;90;103m"
	verify_msg = Yellow
	verify_ok = LightGreen
	id = LightPurple
	data = LightGray
	secret = DarkGray
	sender = LightBlue
	msg_req = LightGreen
	res_error = "\033[0;91m"
	res_ok = Yellow
	action = Brown
	p_win = LightCyan
	p_defeat = LightRed
	water = Blue
	miss = LightCyan
	hit = LightRed
	shoot = "\033[1;30;103m"

cc = ConsoleColors()
