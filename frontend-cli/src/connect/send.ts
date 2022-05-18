import { ethers } from "ethers";
import { connect } from "./connect";
import { UserWallet } from "./wallets"

export const sendCommand = async (userWallet: UserWallet, message: string) => {
	const { chain, inputContract } = await connect(userWallet.network, userWallet.mnemonic, userWallet.path);
	const input = ethers.utils.toUtf8Bytes(message);

	const tx = await inputContract.addInput(input);
	const receipt = await tx.wait(1);
}	
