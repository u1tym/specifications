CREATE TABLE users (
    uid               SERIAL      PRIMARY KEY,             -- ユーザID（自動採番）
    uname             VARCHAR(50) NOT NULL UNIQUE,         -- ユーザ名称（ユニーク）
    upass             TEXT        NOT NULL,                -- パスワード
    magic_number      INTEGER,                 -- マジックナンバー（パスワード処理用ランダム数値）
    sequence_number   BIGINT,                  -- シーケンス管理用番号（大きな値も扱えるように）
    last_access_at    TIMESTAMP WITH TIME ZONE -- 最終アクセス日時
);

--- 機能を管理するテーブル
CREATE TABLE features (
    fid               SERIAL       PRIMARY KEY,     -- 機能ID
    fname             VARCHAR(100) NOT NULL UNIQUE, -- 機能名称
    feature_url       TEXT         NOT NULL,        -- 機能URL
    icon_data         BYTEA,                        -- アイコン画像のバイナリデータ
    icon_mime_type    VARCHAR(50),                  -- 例: 'image/png'
    is_deleted        BOOLEAN      DEFAULT FALSE    -- 削除フラグ
);

--- 使用可能機能を管理するテーブル
CREATE TABLE user_features (
    uid               INTEGER NOT NULL,    -- ユーザID（users.uid）
    fid               INTEGER NOT NULL,    -- 機能ID（features.feature_id）
    display_order     INTEGER DEFAULT 0,   -- 表示順（小さいほど上に表示）
    PRIMARY KEY (uid, fid),                -- 複合主キーで重複を防ぐ
    FOREIGN KEY (uid) REFERENCES users(uid)    ON DELETE CASCADE,
    FOREIGN KEY (fid) REFERENCES features(fid) ON DELETE CASCADE
);
