export default function CliColors() {

	this.colors = {
		NC           : "\x1b[0m",
		Black        : "\x1b[0;30m",
		Red          : "\x1b[0;31m",
		Green        : "\x1b[0;32m",
		Brown        : "\x1b[0;33m",
		Blue         : "\x1b[0;34m",
		Purple       : "\x1b[0;35m",
		Cyan         : "\x1b[0;36m",
		LightGray    : "\x1b[0;37m",
		DarkGray     : "\x1b[1;30m",
		LightRed     : "\x1b[1;31m",
		LightGreen   : "\x1b[1;32m",
		Yellow       : "\x1b[1;33m",
		LightBlue    : "\x1b[1;34m",
		LightPurple  : "\x1b[1;35m",
		LightCyan    : "\x1b[1;36m",
		White        : "\x1b[1;37m",	
	}

	this.colorsGame = {
		NC		: this.colors.NC,
		water	: this.colors.Blue,
		miss	: this.colors.LightCyan,
		hit		: this.colors.LightRed,
		ship	: "\x1b[1;32;45m",
		shoot	: "\x1b[1;30;103m",
		c_water	: "\x1b[5;30;103m",
		c_miss	: "\x1b[5;30;46m",
		c_hit	: "\x1b[5;31;46m",
		ilbl	: this.colors.DarkGray,
		grid	: this.colors.White,
	}

	this.colorsLogo = {
		NC: "\x1b[40m",
		a0 : "\x1b[0;34;40m",
		a1 : "\x1b[1;37;40m",
		a2 : "\x1b[1;31;40m",
		a3 : "\x1b[1;30;40m",
		a4 : "\x1b[0;36;40m",
		a5 : "\x1b[0;37;40m",
		a6 : "\x1b[0;35;40m",
		a7 : "\x1b[1;32;40m",
		a8 : "\x1b[1;30;103m",
	}
	
}
