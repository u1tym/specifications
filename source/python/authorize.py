# -*- coding: utf-8 -*-

import sys
import warnings

sys.dont_write_bytecode = True
warnings.filterwarnings('ignore')

import psycopg2
import random
import zlib
from datetime import datetime

from typing import Self
from typing import TypedDict, List, Optional

class FeatureInfo(TypedDict):
    fid: int
    fname: str
    feature_url: str
    icon_data: Optional[bytes]
    icon_mime_type: Optional[str]

class Authorize:

    _dsn: str = ""

    def __init__(self: Self, dbhost: str, dbport: int, dbname: str, dbuser: str, dbpass: str) -> None:
        self._dsn = f"host={dbhost} port={dbport} dbname={dbname} user={dbuser} password={dbpass}"
        return

    def get_magic_number(self: Self, user: str) -> int:
        """
        マジックナンバー取得処理

        Parameters:
            user: ユーザ名称

        Returns:
            number: 正数: マジックナンバー
                    -1:   該当ユーザが存在しない
                    -2:   認証不正
                    -9:   処理異常
        """

        try:
            with psycopg2.connect(self._dsn) as conn:
                with conn.cursor() as cur:
                    # ユーザIDを取得
                    cur.execute("SELECT uid FROM users WHERE uname = %s", (user,))
                    row = cur.fetchone()

                    if row is None:
                        return -1  # 該当なし

                    uid = row[0]

                    # マジックナンバー生成（例：100000〜999999のランダムな整数）
                    mnum = random.randint(100000, 999999)

                    # ユーザ情報を更新
                    cur.execute("""
                        UPDATE users
                        SET magic_number = %s,
                            sequence_number = NULL,
                            last_access_at = %s
                        WHERE uid = %s
                    """, (mnum, datetime.now(), uid))

                    if cur.rowcount == 0:
                        return -9  # 更新されなかった場合

                    conn.commit()
                    return mnum

        except Exception as e:
            print(f"エラーが発生しました: {e}")
            return -9


    def try_unlock(self: Self, user: str, magic: int, pass_hash: str) -> int:
        """
        認証処理

        Parameters:
            user: ユーザ名称
            magic: マジックナンバー
            pass_hash: ハッシュ化パスワード

        Returns:
            number: 正数: シーケンス管理用番号
                    -1:   該当ユーザが存在しない
                    -2:   認証不正
                    -9:   処理異常
        """

        try:
            with psycopg2.connect(self._dsn) as conn:
                with conn.cursor() as cur:
                    # ユーザ情報の取得
                    cur.execute("SELECT uid, upass FROM users WHERE uname = %s and magic_number = %s", (user, magic,))
                    row = cur.fetchone()

                    if row is None:
                        return -1  # 該当ユーザなし

                    uid, upass = row

                    # マジックナンバーを使ってハッシュを生成
                    combined = f"{upass}{magic}"
                    generated_hash = format(zlib.crc32(combined.encode()) & 0xFFFFFFFF, '08x')

                    if generated_hash != pass_hash:
                        return -2  # 認証失敗

                    # シーケンス番号を生成
                    snum = random.randint(100000, 999999)

                    # ユーザ情報を更新
                    cur.execute("""
                        UPDATE users
                        SET magic_number = NULL,
                            sequence_number = %s,
                            last_access_at = %s
                        WHERE uid = %s
                    """, (snum, datetime.now(), uid))

                    if cur.rowcount == 0:
                        return -1  # 更新失敗

                    conn.commit()
                    return snum

        except Exception as e:
            print(f"DB接続エラー: {e}")
            return -9



    def try_unlock_extend(self: Self, user: str, sequence: int) -> int:
        """
        認証延長処理

        Parameters:
            user: ユーザ名称（ユニーク）
            sequence: シーケンス管理用番号

        Returns:
            number or None: シーケンス管理用番号
        """

        try:
            with psycopg2.connect(self._dsn) as conn:
                with conn.cursor() as cur:
                    # ユーザ確認
                    cur.execute("""
                        SELECT uid FROM users
                        WHERE uname = %s AND sequence_number = %s
                    """, (user, sequence))
                    row = cur.fetchone()

                    if row is None:
                        return -2  # 該当なし

                    uid = row[0]

                    # 新しいシーケンス番号を生成
                    snum = random.randint(100000, 999999)

                    # 更新処理
                    cur.execute("""
                        UPDATE users
                        SET magic_number = NULL,
                            sequence_number = %s,
                            last_access_at = %s
                        WHERE uid = %s
                    """, (snum, datetime.now(), uid))

                    if cur.rowcount == 0:
                        return -2  # 更新されなかった

                    conn.commit()
                    return snum

        except Exception as e:
            print(f"DB接続エラー: {e}")
            return -9


    def get_feature_list(self: Self, user: str) -> List[FeatureInfo]:
        """
        機能一覧取得

        Parameter:
            user: ユーザ名称
        """
        try:
            with psycopg2.connect(self._dsn) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT f.fid, f.fname, f.feature_url, f.icon_data, f.icon_mime_type
                        FROM users u
                        JOIN user_features uf ON u.uid = uf.uid
                        JOIN features f ON uf.fid = f.fid
                        WHERE u.uname = %s AND (f.is_deleted = false OR f.is_deleted IS NULL)
                        ORDER BY uf.display_order
                    """, (user,))
                    rows = cur.fetchall()

                    return [
                        FeatureInfo(
                            fid=row[0],
                            fname=row[1],
                            feature_url=row[2],
                            icon_data=row[3],
                            icon_mime_type=row[4]
                        )
                        for row in rows
                    ]

        except Exception as e:
            print(f"DBエラー: {e}")
            return []
