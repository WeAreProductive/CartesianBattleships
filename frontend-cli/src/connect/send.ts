import { ethers } from "ethers";
import { connect } from "./connect";

const HARDHAT_DEFAULT_MNEMONIC = "test test test test test test test test test test test junk";

interface Args {
    network: string;
    mnemonic: string;
    message: string;
}

export const sendCommand = async (args: Args) => {
	const { chain, inputContract } = await connect(args.network, HARDHAT_DEFAULT_MNEMONIC);
	const input = ethers.utils.toUtf8Bytes(args.message);

	const tx = await inputContract.addInput(input);
	const receipt = await tx.wait(1);
}	
