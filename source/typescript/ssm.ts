export class Verify {
    private static readonly SKEY = "SEQKEY"

    /**
     * セッション情報の更新
     * @param data セッション情報
     */
    static update = (data: Verify.SessionInfo) => {
        sessionStorage.setItem(Verify.SKEY, JSON.stringify(data))
    }

    /**
     * セッション情報の取得
     * @returns セッション情報（取得失敗時はnull）
     */
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

    /**
     * ハッシュ値生成処理
     * @param magic マジックナンバ
     * @param upass パスワード
     * @returns 生成したハッシュ値
     */
    static calc_hash = (magic: number, upass: string): string => {
        const combined = `${upass}${magic}`
        const crc = Verify.generateCRC32(combined)
        return crc.toString(16).padStart(8, '0')
    }

    /** 内部処理 */
    private static readonly table: number[] = (() => {
        let c: number
        const table = []
        for (let n = 0; n < 256; n++) {
            c = n
            for (let k = 0; k < 8; k++) {
                c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1
            }
            table[n] = c
        }
        return table
    })()

    /** 内部処理 */
    static generateCRC32 = (str: string): number => {
        let crc = 0 ^ (-1)
        for (let i = 0; i < str.length; i++) {
            crc = (crc >>> 8) ^ Verify.table[(crc ^ str.charCodeAt(i)) & 0xff]
        }
        return (crc ^ (-1)) >>> 0
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
