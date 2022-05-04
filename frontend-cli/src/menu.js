import TerminalMenu from "simple-terminal-menu";
import inquirer from "inquirer";
import CliColors from "./cli-colors.js";

export default function Menu() {

	var linesLogo = [];

	var printLogo = () => {
		const cl = new CliColors().colorsLogo;
		var addLine = (line) => {
			for (var key in cl) {
				var ph = "{cc." + key + "}";
				line = line.replaceAll(ph, cl[key]);
			}
			linesLogo.push(line);		
		}

		linesLogo = [];
		addLine("");
		addLine("");
		addLine("  {cc.a8}   Cartesi   {cc.NC}                         {cc.a5}.) {cc.a3}|{cc.NC}");
		addLine("  {cc.a8} Battleships {cc.NC}                      {cc.a3}____|_|_{cc.a5}(.{cc.NC}");
		addLine("                                     {cc.a3}_\\______|{cc.NC}");
		addLine("                                   {cc.a3}_/________|_{cc.a4}//{cc.a3}_{cc.NC}");
		addLine("               {cc.a3}_______            /   {cc.a6}<<<{cc.a3}         |{cc.NC}");
		addLine("               {cc.a3}\\ {cc.a5}...  {cc.a3}\\___{cc.a4}[\\\\\\]{cc.a3}__/_________{cc.a4}[///]{cc.a3}__|___{cc.a7}F{cc.NC}");
		addLine("   {cc.a1}__{cc.a2}4{cc.a1}__        {cc.a3}\\                                     |{cc.NC}");
		addLine("   {cc.a1}\\   /{cc.NC}         {cc.a3}\\   V            {cc.a6}<<<      <<<        {cc.a3}/{cc.NC}");
		addLine("{cc.a0}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{cc.NC}");
		addLine("{cc.a0}~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~{cc.NC}");
		addLine("{cc.a0} ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ {cc.NC}");
		addLine("");
		addLine("");
	}

	printLogo();

	this.showMainMenu = (fn_CreateGame, fn_JoinGame) => {
		var menu = new TerminalMenu({
			width: 60,
			fg: "yellow",
			bg: "black",
			padding: { left: 4, right: 4, top: 1, bottom: 2 },
		});
		for (const line of linesLogo) {
			menu.writeLine(line);
		}
		menu.writeSeparator();
		menu.add("Create game", (label, marker) => fn_CreateGame(label, marker));
		menu.add("Join game", (label, marker) => fn_JoinGame(label, marker));
		menu.writeSeparator();
		menu.add("Exit", menu.close);
	}

}
