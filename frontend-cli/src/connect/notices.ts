import { createClient, defaultExchanges } from "@urql/core";
import fetch from "cross-fetch";
import {
    GetNoticeDocument,
    Notice,
    NoticeKeys,
} from "../../generated-src/graphql";

export type PartialNotice = Pick<
    Notice,
    | "__typename"
    | "session_id"
    | "epoch_index"
    | "input_index"
    | "notice_index"
    | "payload"
>;

const isPartialNotice = (n: PartialNotice | null): n is PartialNotice =>
    n !== null;

/**
 * Queries a GraphQL server looking for the notices of an input
 * @param url URL of the GraphQL server
 * @param input Blockchain event of input added or the notice keys to be queried
 * @param timeout How long to wait for notice to be detected
 * @returns List of notices
 */
export const getNotices = async (
    url: string,
    noticeKeys: NoticeKeys
): Promise<PartialNotice[]> => {
	// create GraphQL client to reader server
	const client = createClient({ url, exchanges: defaultExchanges, fetch });

	//let noticeKeys: NoticeKeys = { input_index: "3" };

	const { data, error } = await client
		.query(GetNoticeDocument, { query: noticeKeys })
		.toPromise();

	if (data?.GetNotice) {
		return data.GetNotice.filter<PartialNotice>(isPartialNotice);
	} else {
		throw new Error(error?.message);
	}	
}
