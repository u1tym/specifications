
### シーケンス

```mermaid
sequenceDiagram
  actor HM as operator
  participant FR as Frontend

  box UI
    participant LG as UI(login)
    participant MN as UI(menu)
    participant JB as UI(job)
  end

  box Backend
    participant BA as /auth
    participant BM as /jobmenu
    participant BJ as /jobhoge
  end

  box Class
    participant CA as Ahthorize
  end

  box Database
    participant DA as DB(auth)
    participant DJ as DB(job)
  end

  FR ->>+ LG: ログインページ
  LG --)- FR:

  HM ->>+ FR: ログイン
  FR ->>+ BA: プレ要求(USER)
  BA ->>+ CA: マジックナンバー取得処理
  CA ->>+ DA:
  DA --)- CA:
  CA --)- BA:
  BA --)- FR: プレ応答(MAGIC_NUMBER)

  FR ->>+ BA: 開錠要求(USER, MAGIC_NUMBER, HASH_PASS)
  BA ->>+ CA: 認証処理
  CA ->>+ DA:
  DA --)- CA:
  CA --)- BA:
  BA --)- FR: 開錠応答(RESULT, SEQ_NUMBER)
  note over FR: 更新 session storage<br>USER, SEQ_NUMBER

  FR ->>+ MN: メニューページ
  MN --)- FR:
  note over FR: 取得 session storage<br>USER, SEQ_NUMBER
  FR ->>+ BM: JOB一覧要求(USER, SEQ_NUMBER)
  BM ->>+ CA: 認証延長処理
  CA ->>+ DA:
  DA --)- CA:
  CA --)- BM:
  BM ->>+ CA: 機能一覧取得
  CA ->>+ DA:
  DA --)- CA:
  CA --)- BM:
  BM --)- FR: JOB一覧応答(RESULT, SEQ_NUMBER, JOB一覧)
  note over FR: 更新 session storage<br>USER, SEQ_NUMBER
  FR --)- HM: メニュー表示

  HM ->>+ FR: メニュー選択
  FR ->>+ JB: 遷移
  JB --)- FR:
  note over FR: 取得 session storage<br>USER, SEQ_NUMBER
  FR ->>+ BJ: 要求
  BJ ->>+ CA: 認証延長処理
  CA ->>+ DA:
  DA --)- CA:
  CA --)- BJ:
  BJ ->>+ DJ: 業務処理
  DJ --)- BJ:
  BJ --)- FR: 応答(RESULT, SEQ_NUMBER, 業務の結果)
  note over FR: 更新 session storage<br>USER, SEQ_NUMBER
  FR --)- HM: 結果表示
```

### インタフェース

#### プレ要求
| No. | 項目名 | 型 | 説明 |
|:---:|--- |--- | --- |
| 1 | USER | string | 試行ユーザ名 |

#### プレ応答
| No. | 項目名 | 型 | 説明 |
|:---:|--- |--- | --- |
| 1 | RESULT | boolean | 結果(True/False) |
| 2 | DETAIL | string | 結果がFalseだった場合に詳細情報を設定 |
| 3 | MAGIC_NUMBER | number | マジックナンバ |

#### 開錠要求
| No. | 項目名 | 型 | 説明 |
|:---:|--- |--- | --- |
| 1 | USER | string | 試行ユーザ名 |
| 2 | MAGIC_NUMBER | number | マジックナンバ |
| 3 | HASH_PASS | string | ハッシュ化パスワード |

#### 開錠応答
| No. | 項目名 | 型 | 説明 |
|:---:|--- |--- | --- |
| 1 | RESULT | boolean | 結果(True/False) |
| 2 | DETAIL | string | 結果がFalseだった場合に詳細情報を設定 |
| 3 | SEQ_NUMBER | number | シーケンス管理ナンバ |

#### 要求（一般系）
| No. | 項目名 | 型 | 説明 |
|:---:|--- |--- | --- |
| 1 | USER | string | 試行ユーザ名 |
| 2 | SEQ_NUMBER | number | シーケンス管理ナンバ |
| : | <div align="center">:</div> | <div align="center">:</div> | 以降、業務データ |

#### 応答（一般系）
| No. | 項目名 | 型 | 説明 |
|:---:|--- |--- | --- |
| 1 | RESULT | boolean | 結果(True/False) |
| 2 | DETAIL | string | 結果がFalseだった場合に詳細情報を設定 |
| 3 | SEQ_NUMBER | number | シーケンス管理ナンバ |
| : | <div align="center">:</div> | <div align="center">:</div> | 以降、業務応答 |
