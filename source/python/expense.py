# -*- coding: utf-8 -*-

import sys
import warnings

sys.dont_write_bytecode = True
warnings.filterwarnings('ignore')

from datetime import datetime as dtm
from typing import Self
from typing import Optional

class Expense:

    _dsn: str = ""

    def __init__(self: Self, dbhost: str, dbport: int, dbname: str, dbuser: str, dbpass: str) -> None:
        self._dsn = f"host={dbhost} port={dbport} dbname={dbname} user={dbuser} password={dbpass}"
        return

    def create_account(self: Self, uname: str, aname: str) -> bool:
        """
        口座作成処理

        parameters
            uname: ユーザ名
            aname: 口座名称

        returns
            True: 正常終了
            False: 異常終了
        """
        res: bool = False
        return res

    def delete_account(self: Self, uname: str, aname: str) -> bool:
        """
        口座削除処理

        parameters
            uname: ユーザ名
            aname: 口座名称

        returns
            True: 正常終了
            False: 異常終了
        """
        res: bool = False
        return res

    def create_immediate_payment(self: Self, uname: str, pname: str, aname: str) -> bool:
        """
        支払い方法作成（当日払い）

        parameters
            uname: ユーザ名
            pname: 支払い方法名称
            aname: 支払い対象の口座名称

        returns
            True: 正常終了
            False: 異常終了
        """
        res: bool = False
        return res

    def create_deferred_payment(self: Self, uname: str, pname: str, aname: str, close_day: int, payment_offset_month: int, payment_day: int) -> bool:
        """
        支払い方法作成（後日払い）

        parameters
            uname: ユーザ名
            pname: 支払い方法名称
            aname: 支払い対象の口座名称
            close_day: 締め日
            payment_offset_month: 支払い月ズレ
            payment_day: 支払い日

        returns
            True: 正常終了
            False: 異常終了
        """
        res: bool = False
        return res

    def delete_payment(self: Self, uname: str, pname: str) -> bool:
        """
        支払い方法削除

        parameters
            uname: ユーザ名
            pname: 支払い方法名称

        returns
            True: 正常終了
            False: 異常終了
        """
        res: bool = False
        return res

    def add_transaction(self: Self, uname: str, tdate: dtm, purpose: str, memo: Optional[str], pname: Optional[str], amount_spent: int, aname: Optional[str], amount_received: int) -> bool:
        """
        取引追加

        parameters
            uname: ユーザ名
            tdate: 取引日
            purpose: 用途
            memo: メモ
            pname: 支払い方法名称
            amount_spent: 出金の金額
            aname: 入金の口座名称
            amount_received: 入金の金額

        returns
            True: 正常終了
            False: 異常終了
        """
        res: bool = False
        return res

    def delete_transaction(self: Self, uname: str, tdate: dtm, dorder: int) -> bool:
        """
        取引削除

        parameters
            uname: ユーザ名
            tdate: 取引日
            dorder: 表示順

        returns
            True: 正常終了
            False: 異常終了
        """
        res: bool = False
        return res
