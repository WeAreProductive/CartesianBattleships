import { ethers, ContractReceipt } from "ethers";
import { connect } from "./connect";
import { UserWallet } from "./wallets"
import { NoticeKeys } from "../../generated-src/graphql";
import { InputAddedEvent } from "../../generated-src/rollups/Input";

const findNoticeKeys = (receipt: ContractReceipt): NoticeKeys => {
    // get InputAddedEvent from transaction receipt
    const event = receipt.events?.find((e) => e.event === "InputAdded");

    if (!event) {
		return { epoch_index: "", input_index: "" };
        //throw new Error(`InputAdded event not found in receipt of transaction ${receipt.transactionHash}`);
    }

    const inputAdded = event as InputAddedEvent;
    return {
        epoch_index: inputAdded.args._epochNumber.toString(),
		input_index: event !=null && event.args != null ? event.args._inputIndex.toString() : undefined,
        // XXX: input_index: event.args._inputIndex.toString(),
    };
};

export const sendCommand = async (userWallet: UserWallet, message: string) => {
	const { chain, inputContract } = await connect(userWallet.network, userWallet.mnemonic, userWallet.path);
	const input = ethers.utils.toUtf8Bytes(message);

	const tx = await inputContract.addInput(input);
	const receipt = await tx.wait(1);
	const noticeKeys = findNoticeKeys(receipt);

	return noticeKeys;
}

export const getWalletAddress = (userWallet: UserWallet): string => {
	const wallet = ethers.Wallet.fromMnemonic(userWallet.mnemonic, userWallet.path);
	return wallet.address;
}
