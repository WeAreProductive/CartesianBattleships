const HARDHAT_DEFAULT_MNEMONIC = "test test test test test test test test test test test junk";

export interface UserWallet {
	name: string;
    network: string;
    mnemonic: string;
	path: string;
}

export const defaultWallets: UserWallet[] = [
	{
		name: "player1",
		network: "localhost",
		mnemonic: HARDHAT_DEFAULT_MNEMONIC,
		path: "m/44'/60'/0'/0/0"
	},
	{
		name: "player2",
		network: "localhost",
		mnemonic: HARDHAT_DEFAULT_MNEMONIC,
		path: "m/44'/60'/0'/0/1"
	}
];
