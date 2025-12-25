export class Telegram {

    static get = async (
        url: string,
        request: { [k: string]: string | number | boolean } | null,
        success: ((reply: string) => void) | null,
        error: ((reply: string) => void) | null
    ) => {
        const opt = {
            method: 'GET',
            mode: 'cors' as RequestMode,
            credentials: 'include' as RequestCredentials,
            headers: {
                'Content-Type': 'application/json; charset=UTF-8',
            },
        }

        let sendUrl = url
        if (request !== null) {
            const params = Object.entries(request)
                .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(String(v))}`)
                .join('&')
            sendUrl += '?' + params
        }

        try {
            const res = await fetch(sendUrl, opt)
            const status = Math.floor(res.status / 100)
            if (status === 2) {
                if (typeof success === "function") {
                    const reply = JSON.stringify(await res.json())
                    success(reply)
                }
            } else {
                if (typeof error === "function") {
                    const reply = await res.text()
                    error(reply)
                }
            }
        } catch (e) {
            if (typeof error === "function") {
                error(`通信エラー: ${e}`)
            }
        }
    }

    static post = async (
        url: string,
        request: { [k: string]: string | number | boolean },
        success: ((reply: string) => void) | null,
        error: ((reply: string) => void) | null
    ) => {
        const body = JSON.stringify(request)
        const opt = {
            method: 'POST',
            mode: 'cors' as RequestMode,
            credentials: 'include' as RequestCredentials,
            body,
            headers: {
                'Content-Type': 'application/json; charset=UTF-8',
            },
        }

        try {
            const res = await fetch(url, opt)
            const status = Math.floor(res.status / 100)
            if (status === 2) {
                if (typeof success === "function") {
                    const reply = JSON.stringify(await res.json())
                    success(reply)
                }
            } else {
                if (typeof error === "function") {
                    const reply = await res.text()
                    error(reply)
                }
            }
        } catch (e) {
            if (typeof error === "function") {
                error(`通信エラー: ${e}`)
            }
        }
    }
}
