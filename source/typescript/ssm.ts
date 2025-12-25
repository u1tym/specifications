export class Verify {
    private static readonly SKEY = "SEQKEY"

    /**
     *
     * @param data
     */
    static update = (data: Verify.SessionInfo) => {
        sessionStorage.setItem(Verify.SKEY, JSON.stringify(data))
    }

    static select = (): Verify.SessionInfo | null => {
        const result = sessionStorage.getItem(Verify.SKEY)
        if (result) {
            try {
                const parsed = JSON.parse(result)
                if (typeof parsed.user === "string" && typeof parsed.sequence === "number") {
                    return parsed as Verify.SessionInfo
                }
            } catch (e) {
                console.error("セッションデータの解析に失敗しました:", e)
            }
        }
        return null
    }
}

/**
 * ユーザのセッション情報
 */
export namespace Verify {
    export type SessionInfo = {
        user: string
        sequence: number
    }
}
