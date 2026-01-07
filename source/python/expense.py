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

        notes:
            DBに接続。self._dsnを使う
            auth.usersから、引数のunameを条件に、uidを取得
            expense.accountsにレコードを追加。is_deletedはFALSE
            すべて正常に処理できた場合にはcommitする。処理異常が発生した場合には、rollbackする。
            正常に処理できたらTrue、できなかったらFalseを返す。
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

        notes:
            DBに接続。self._dsnを使う
            auth.usersから、引数のunameを条件に、uidを取得
            expense.accountsから、uid、account_name=引数のanameを条件にaidを特定する。
            aidをキーに、account_nameの末尾に’(削除済み)’を追加した値で更新するが、
            uid+account_nameで同名が存在する場合には、’(削除済みN)’ Nは連番で更新し、
            is_deletedはTrueで更新する。
            すべて正常に処理できた場合にはcommitする。処理異常が発生した場合には、rollbackする。
            正常に処理できたらTrue、できなかったらFalseを返す。
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

        notes:
            DBに接続。self._dsnを使う
            auth.usersから、引数のunameを条件に、uidを取得
            expense.accountsから、uid、account_name=引数のaname、is_deleted=Falseを条件にaidを特定する。
            expense.paymentsに以下の値でレコードを1件追加する。
            ・pid 自動採番
            ・uid 取得したuid
            ・payment_name 引数のpname
            ・closing_day 0を設定
            ・payment_offset_month 0を設定
            ・payment_day 0を設定
            ・aid 取得したaid
            ・deleted_at NULLを設定
            すべて正常に処理できた場合にはcommitする。処理異常が発生した場合には、rollbackする。
            正常に処理できたらTrue、できなかったらFalseを返す。
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

        notes:
            DBに接続。self._dsnを使う
            auth.usersから、引数のunameを条件に、uidを取得
            expense.accountsから、uid、account_name=引数のaname、is_deleted=Falseを条件にaidを特定する。
            expense.paymentsに以下の値でレコードを1件追加する。
            ・pid 自動採番
            ・uid 取得したuid
            ・payment_name 引数のpname
            ・closing_day 引数のclose_day
            ・payment_offset_month 引数のpayment_offset_month
            ・payment_day 引数のpayment_day
            ・aid 取得したaid
            ・deleted_at NULLを設定
            すべて正常に処理できた場合にはcommitする。処理異常が発生した場合には、rollbackする。
            正常に処理できたらTrue、できなかったらFalseを返す。
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

        notes:
            DBに接続。self._dsnを使う
            auth.usersから、引数のunameを条件に、uidを取得
            expense.paymentsから、uid、payment_name=引数のpname、deleted_at=NULLを条件にpidを特定する。
            pidをキーに、expense.paymentsを以下の値で更新
            ・payment_name 末尾に’(削除済み)’を追加。UNIQUE制約違反となる場合には、’(削除済みN)’ Nは連番 で更新
            ・deleted_at 現在日で更新
            すべて正常に処理できた場合にはcommitする。処理異常が発生した場合には、rollbackする。
            正常に処理できたらTrue、できなかったらFalseを返す。
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

        notes:
            DBに接続。self._dsnを使う
            auth.usersから、引数のunameを条件に、uidを取得
            引数のpnameがNone以外の場合には、expense.paymentsから、uid、payment_name=引数のpname、deleted_at=NULLを条件にpidを取得し、以降、支出pidと呼称する。
            引数のpnameがNoneの場合には、支出pid=NULLとする。
            引数のanameがNone以外の場合には、expense.accountsから、uis、account_ame=引数のaname、is_deleted=NULLを条件にaidを取得し、以降、収入aidと呼称する。
            引数のanameがNoneの場合には、収入aid=NULLとする。
            expense.transactionsに以下の値でレコードを追加する。
            ・tid 自動採番
            ・uid 取得したuidの値
            ・transaction_date 引数のtdateの日付
            ・dorder トリガーにより自動的に付与
            ・purpose 引数のpurposeの値
            ・memo 引数のmemoの値。Noneの場合にはNULLを設定
            ・pid 支出pidを設定
            ・amount_spent 引数のamount_spent
            ・aid 収入aidを設定
            ・amount_received 引数のamount_received
            ・is_deleted Falseを設定

            支出の処理（支出pidがNULL以外の場合に実行する。NULLの場合は実行しない）
            expense.paymentsから、uid、pid=支出pid、deleted_at=NULLを条件に、aid、closing_day、payment_offset_month、payment_dayを取得する。以降、aidを支出aidと呼称する。
            支出日を以下のルールで決める。
            closing_day=0の場合、支出日=引数のtdateの日付
            closing_day>0の場合、支出日の「年月」は、「引数のtdate」+「payment_offset_month」、支出日の「日」は、payment_day

            以下の条件で、expense.account_historiesのamountの値を取得し、以降、「支出残額」と呼称する。
            aid=支出aid、is_deleted=False、payment_date<=支出日で、payment_date(昇順)+dorder(昇順)でソートした際の一番最後のレコードのamountの値
            レコードが1件も存在しない場合には、支出残額=0とする。

            expense.account_historiesに以下の値でレコードを追加する。
            ・hid 自動採番
            ・aid 支出aid
            ・payment_date 支出日
            ・dorder トリガーにより自動的に付与
            ・tid expense.transactionsにレコード追加した際のtid
            ・amount 支出残額 - 引数のamount_spent の値
            ・is_deleted Falseを設定

            以下の条件で、expense.account_historiesのamountの値を更新する。
            条件 aid=支出aid、is_deleted=False、payment_date>支出日
            更新値 amount = amount - 引数のamount_spent
            支出の処理 ここまで

            収入の処理（収入aidがNULL以外の場合に実行する。NULLの場合は実行しない）
            収入日=引数のtdateの日付
            とする。

            以下の条件で、expense.account_historiesのamountの値を取得し、以降、「収入残額」と呼称する。
            aid=収入aid、is_deleted=False、payment_date<=収入日で、payment_date(昇順)+dorder(昇順)でソートした際の一番最後のレコードのamountの値
            レコードが1件も存在しない場合には、収入残額=0とする。

            expense.account_historiesに以下の値でレコードを追加する。
            ・hid 自動採番
            ・aid 収入aid
            ・payment_date 収入日
            ・dorder トリガーにより自動的に付与
            ・tid expense.transactionsにレコード追加した際のtid
            ・amount 輸入残額 + 引数のamount_received の値
            ・is_deleted Falseを設定

            以下の条件で、expense.account_historiesのamountの値を更新する。
            条件 aid=収入aid、is_deleted=False、payment_date>収入日
            更新値 amount = amount * 引数のamount_received
            収入の処理 ここまで

            すべて正常に処理できた場合にはcommitする。処理異常が発生した場合には、rollbackする。
            正常に処理できたらTrue、できなかったらFalseを返す。
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

        notes:
            DBに接続。self._dsnを使う
            auth.usersから、引数のunameを条件に、uidを取得

            expense.transactionsから、uid、transaction_date=引数のtdateの日付、dorder=引数のdorder、is_deleted=Falseを条件に、tid、pid、aid、amount_spent、amount_receivedを取得する。以降、tidを支出tid、aidを収入aidと呼称する。

            expense.transactionsを以下の条件で更新する
            条件 tid = 取得したtid
            更新値 is_deleted True

            支出取り消し処理（支出pidがNULL以外の場合に実行する。NULLの場合は実行しない）
            expense.paymentsから、uid、pid=支出pid、deleted_at=NULLを条件に、aidを取得する。以降、aidを支出aidと呼称する。
            expense.account_historiesから、aid=支出aid、tid=取得したtid、is_deleted=Falseを条件に、payment_date、dorderを取得する。以降、支出payment_date、支出dorderと呼称する。

            以下の条件で、expense.account_historiesを更新する。
            条件 aid=支出aid、tid=取得したtid、is_deleted=False
            更新値 is_deleted True

            以下の条件で、expense.account_historiesを更新する。
            条件 aid=支出aid、payment_date（昇順）+ dorder（昇順）でソートした際に、支出payment_date + 支出dorder 以降のレコード
            更新値 amount = amount + amount_spent
            支出取り消し処理 ここまで

            収入取り消し処理（収入aidがNULL以外の場合に実行する。NULLの場合は実行しない）
            expense.account_historiesから、aid=収入aid、tid=取得したtid、is_deleted=Falseを条件に、payment_date、dorderを取得する。以降、収入payment_date、収入dorderと呼称する。

            以下の条件で、expense.account_historiesを更新する。
            条件 aid=収入aid、tid=取得したtid、is_deleted=False
            更新値 is_deleted True

            以下の条件で、expense.account_historiesを更新する。
            条件 aid=収入aid、payment_date（昇順）+ dorder（昇順）でソートした際に、収入payment_date + 収入dorder 以降のレコード
            更新値 amount = amount - amount_received
            収入取り消し処理 ここまで

            すべて正常に処理できた場合にはcommitする。処理異常が発生した場合には、rollbackする。
            正常に処理できたらTrue、できなかったらFalseを返す。
        """
        res: bool = False
        return res
