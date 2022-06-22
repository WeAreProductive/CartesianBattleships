import { ethers } from "ethers";
import { networks } from "./networks";
import { connect } from "./connect";
import { UserWallet } from "./wallets"
import { getNotices, PartialNotice } from "./notices";
import { NoticeKeys } from "../../generated-src/graphql";

const INTERVAL_LISTEN = 1000;

class MessageIndex {
	epoch_index: number = 0;
	input_index: number = 0;
	
	fromNotice(n: PartialNotice) {
		if (n != undefined) {
			this.epoch_index = parseInt(n.epoch_index);
			this.input_index = parseInt(n.input_index);
		}
		return this;
	}

	compare(m: MessageIndex) {
		if (this.epoch_index < m.epoch_index) return -1;
		if (this.epoch_index > m.epoch_index) return 1;
		if (this.input_index < m.input_index) return -1;
		if (this.input_index > m.input_index) return 1;
		return 0;
	}
}

const decodePayload = (payload: string) => ethers.utils.toUtf8String("0x" + payload);
const payloadAsJson = (payload: string) => JSON.parse(decodePayload(payload));

export class Receiver {

	private userWallet: UserWallet;
	private intListen: any = null;
	private lastMessageIndex: MessageIndex = new MessageIndex();
	private fn_onReceive: Function = () => {};
	private fn_filterCustom: Function = () => {};
	private noticeKeys: NoticeKeys = {};
	

	constructor(userWallet: UserWallet) {
		this.userWallet = userWallet;
	}

	private sortMsg = (a: PartialNotice, b: PartialNotice) => {
		let sort_epoch = parseInt(a.epoch_index) - parseInt(b.epoch_index);
		return (sort_epoch != 0) ? sort_epoch : parseInt(a.input_index) - parseInt(b.input_index);
	}

	private filterRecent = (n: PartialNotice) => {
		return this.lastMessageIndex.compare(new MessageIndex().fromNotice(n)) < 0;
	}

	private async readMessages() {
		let { chain } = await connect(this.userWallet.network);

		let notices = await getNotices(chain.reader, this.noticeKeys);
	
		let messages = notices
			.filter(this.filterRecent)
			.filter((n) => this.fn_filterCustom(payloadAsJson(n.payload)))
			.sort(this.sortMsg);
			//.map((n) => {epoch_index: n.epoch_index, input_index: n.input_index, payload: ethers.utils.toUtf8String("0x" + n.payload)});

		this.lastMessageIndex.fromNotice(<PartialNotice>messages.at(-1));
		
		if (messages.length > 0) {
			//this.fn_onReceive(messages.map((n) => { return {epoch_index: n.epoch_index, input_index: n.input_index, payload: ethers.utils.toUtf8String("0x" + n.payload)}}));
			this.fn_onReceive(messages.map((n) => JSON.parse(decodePayload(n.payload))));
		}
	}

	targetNoticeAll() {
		this.noticeKeys = {};
		return this;
	}

	targetNoticeEpoch(epoch_index: string) {
		this.noticeKeys = { epoch_index: epoch_index };
		return this;
	}

	targetNoticeExact(epoch_index: string, input_index: string) {
		this.noticeKeys = { epoch_index: epoch_index, input_index: input_index };
		return this;
	}

	targetNoticeRecent(since_epoch_index: string, since_input_index: string) {
		// TODO: implement gre (greater than or equal) condition in GraphQL
		return this;
	}

	filter(fn_filterCustom: Function) {
		this.fn_filterCustom = fn_filterCustom;
		return this;
	}
	
	filterClear() {
		this.fn_filterCustom = () => {};
		return this;
	}
	
	onReceive(fn_onReceive: Function) {
		this.fn_onReceive = fn_onReceive;
		return this;
	}
	
	startListen() {
		this.intListen = setInterval(() => this.readMessages(), INTERVAL_LISTEN);
		return this;
	}

	stopListen() {
		clearInterval(this.intListen);
		this.intListen = null;
		return this;
	}
	

}