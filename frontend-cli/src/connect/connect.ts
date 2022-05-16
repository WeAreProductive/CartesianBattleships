import { JsonRpcProvider } from "@ethersproject/providers";
import { ethers } from "ethers";
import {
    InputImpl,
    InputImpl__factory,
    OutputImpl,
    OutputImpl__factory,
    RollupsImpl,
    RollupsImpl__factory,
} from "../../generated-src/rollups";
import { Chain, networks } from "./networks";

interface Contracts {
    chain: Chain;
    rollupsContract: RollupsImpl;
    inputContract: InputImpl;
    outputContract: OutputImpl;
}

export const connect = async (
    chainName: string,
    mnemonic?: string
): Promise<Contracts> => {
    const chain = networks.find((n) => n.name === chainName);
    if (!chain) {
        throw new Error(`Unknown network: ${chainName}`);
    }
    // connect to JSON-RPC provider
    const provider = new JsonRpcProvider(chain.rpc);

    // check network chainId
    const network = await provider.getNetwork();
    if (network.chainId !== chain.chainId) {
        throw new Error(`Mismatched chainId: ${network.chainId}`);
    }

    // load contract address
    const deploy = await import(chain.abi);
    const address = deploy.contracts?.RollupsImpl?.address;
    if (!address) {
        throw new Error(`contract RollupsImpl not found at ${chain.abi}`);
    }

    // create signer to be used to send transactions
    const signer = mnemonic
        ? ethers.Wallet.fromMnemonic(mnemonic).connect(provider)
        : new ethers.VoidSigner(address).connect(provider);

    // connect to contracts
    const rollupsContract = RollupsImpl__factory.connect(address, signer);
    const inputContract = InputImpl__factory.connect(
        await rollupsContract.getInputAddress(),
        signer
    );
    const outputContract = OutputImpl__factory.connect(
        await rollupsContract.getOutputAddress(),
        signer
    );
    return {
        chain,
        rollupsContract,
        inputContract,
        outputContract,
    };
};
