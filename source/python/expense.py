# -*- coding: utf-8 -*-

import sys
import warnings

sys.dont_write_bytecode = True
warnings.filterwarnings('ignore')

import psycopg2
from datetime import datetime as dtm
from datetime import date
from calendar import monthrange
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
        try:
            with psycopg2.connect(self._dsn) as conn:
                with conn.cursor() as cur:
                    # ユーザIDを取得
                    cur.execute("SELECT uid FROM auth.users WHERE uname = %s", (uname,))
                    row = cur.fetchone()
                    if row is None:
                        return False
                    uid: int = row[0]

                    # 口座を追加
                    cur.execute("""
                        INSERT INTO expense.accounts (uid, account_name, is_deleted)
                        VALUES (%s, %s, FALSE)
                    """, (uid, aname))

                    conn.commit()
                    return True
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            return False

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
            aidをキーに、account_nameの末尾に'(削除済み)'を追加した値で更新するが、
            uid+account_nameで同名が存在する場合には、'(削除済みN)' Nは連番で更新し、
            is_deletedはTrueで更新する。
            すべて正常に処理できた場合にはcommitする。処理異常が発生した場合には、rollbackする。
            正常に処理できたらTrue、できなかったらFalseを返す。
        """
        try:
            with psycopg2.connect(self._dsn) as conn:
                with conn.cursor() as cur:
                    # ユーザIDを取得
                    cur.execute("SELECT uid FROM auth.users WHERE uname = %s", (uname,))
                    row = cur.fetchone()
                    if row is None:
                        return False
                    uid: int = row[0]

                    # 口座IDを取得
                    cur.execute("""
                        SELECT aid FROM expense.accounts
                        WHERE uid = %s AND account_name = %s AND is_deleted = FALSE
                    """, (uid, aname))
                    row = cur.fetchone()
                    if row is None:
                        return False
                    aid: int = row[0]

                    # 削除済みマークを付ける（同名が存在する場合は連番を付ける）
                    new_name: str = f"{aname}(削除済み)"
                    counter: int = 1
                    while True:
                        cur.execute("""
                            SELECT COUNT(*) FROM expense.accounts
                            WHERE uid = %s AND account_name = %s
                        """, (uid, new_name))
                        if cur.fetchone()[0] == 0:
                            break
                        new_name = f"{aname}(削除済み{counter})"
                        counter += 1

                    # 口座を更新
                    cur.execute("""
                        UPDATE expense.accounts
                        SET account_name = %s, is_deleted = TRUE
                        WHERE aid = %s
                    """, (new_name, aid))

                    conn.commit()
                    return True
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            return False

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
        try:
            with psycopg2.connect(self._dsn) as conn:
                with conn.cursor() as cur:
                    # ユーザIDを取得
                    cur.execute("SELECT uid FROM auth.users WHERE uname = %s", (uname,))
                    row = cur.fetchone()
                    if row is None:
                        return False
                    uid: int = row[0]

                    # 口座IDを取得
                    cur.execute("""
                        SELECT aid FROM expense.accounts
                        WHERE uid = %s AND account_name = %s AND is_deleted = FALSE
                    """, (uid, aname))
                    row = cur.fetchone()
                    if row is None:
                        return False
                    aid: int = row[0]

                    # 支払い方法を追加
                    cur.execute("""
                        INSERT INTO expense.payments (uid, payment_name, closing_day, payment_offset_month, payment_day, aid, deleted_at)
                        VALUES (%s, %s, 0, 0, 0, %s, NULL)
                    """, (uid, pname, aid))

                    conn.commit()
                    return True
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            return False

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
        try:
            with psycopg2.connect(self._dsn) as conn:
                with conn.cursor() as cur:
                    # ユーザIDを取得
                    cur.execute("SELECT uid FROM auth.users WHERE uname = %s", (uname,))
                    row = cur.fetchone()
                    if row is None:
                        return False
                    uid: int = row[0]

                    # 口座IDを取得
                    cur.execute("""
                        SELECT aid FROM expense.accounts
                        WHERE uid = %s AND account_name = %s AND is_deleted = FALSE
                    """, (uid, aname))
                    row = cur.fetchone()
                    if row is None:
                        return False
                    aid: int = row[0]

                    # 支払い方法を追加
                    cur.execute("""
                        INSERT INTO expense.payments (uid, payment_name, closing_day, payment_offset_month, payment_day, aid, deleted_at)
                        VALUES (%s, %s, %s, %s, %s, %s, NULL)
                    """, (uid, pname, close_day, payment_offset_month, payment_day, aid))

                    conn.commit()
                    return True
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            return False

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
            ・payment_name 末尾に'(削除済み)'を追加。UNIQUE制約違反となる場合には、'(削除済みN)' Nは連番 で更新
            ・deleted_at 現在日で更新
            すべて正常に処理できた場合にはcommitする。処理異常が発生した場合には、rollbackする。
            正常に処理できたらTrue、できなかったらFalseを返す。
        """
        try:
            with psycopg2.connect(self._dsn) as conn:
                with conn.cursor() as cur:
                    # ユーザIDを取得
                    cur.execute("SELECT uid FROM auth.users WHERE uname = %s", (uname,))
                    row = cur.fetchone()
                    if row is None:
                        return False
                    uid: int = row[0]

                    # 支払い方法IDを取得
                    cur.execute("""
                        SELECT pid FROM expense.payments
                        WHERE uid = %s AND payment_name = %s AND deleted_at IS NULL
                    """, (uid, pname))
                    row = cur.fetchone()
                    if row is None:
                        return False
                    pid: int = row[0]

                    # 削除済みマークを付ける（同名が存在する場合は連番を付ける）
                    new_name: str = f"{pname}(削除済み)"
                    counter: int = 1
                    while True:
                        cur.execute("""
                            SELECT COUNT(*) FROM expense.payments
                            WHERE uid = %s AND payment_name = %s
                        """, (uid, new_name))
                        if cur.fetchone()[0] == 0:
                            break
                        new_name = f"{pname}(削除済み{counter})"
                        counter += 1

                    # 支払い方法を更新
                    cur.execute("""
                        UPDATE expense.payments
                        SET payment_name = %s, deleted_at = CURRENT_DATE
                        WHERE pid = %s
                    """, (new_name, pid))

                    conn.commit()
                    return True
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            return False

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
            引数のanameがNone以外の場合には、expense.accountsから、uid、account_name=引数のaname、is_deleted=Falseを条件にaidを取得し、以降、収入aidと呼称する。
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
            ・amount 収入残額 + 引数のamount_received の値
            ・is_deleted Falseを設定

            以下の条件で、expense.account_historiesのamountの値を更新する。
            条件 aid=収入aid、is_deleted=False、payment_date>収入日
            更新値 amount = amount + 引数のamount_received
            収入の処理 ここまで

            すべて正常に処理できた場合にはcommitする。処理異常が発生した場合には、rollbackする。
            正常に処理できたらTrue、できなかったらFalseを返す。
        """
        try:
            with psycopg2.connect(self._dsn) as conn:
                with conn.cursor() as cur:
                    # ユーザIDを取得
                    cur.execute("SELECT uid FROM auth.users WHERE uname = %s", (uname,))
                    row = cur.fetchone()
                    if row is None:
                        return False
                    uid: int = row[0]

                    # 支出pidを取得
                    expense_pid: Optional[int] = None
                    if pname is not None:
                        cur.execute("""
                            SELECT pid FROM expense.payments
                            WHERE uid = %s AND payment_name = %s AND deleted_at IS NULL
                        """, (uid, pname))
                        row = cur.fetchone()
                        if row is not None:
                            expense_pid = row[0]

                    # 収入aidを取得
                    income_aid: Optional[int] = None
                    if aname is not None:
                        cur.execute("""
                            SELECT aid FROM expense.accounts
                            WHERE uid = %s AND account_name = %s AND is_deleted = FALSE
                        """, (uid, aname))
                        row = cur.fetchone()
                        if row is not None:
                            income_aid = row[0]

                    # 取引日をdate型に変換
                    transaction_date: date = tdate.date()

                    # 取引を追加
                    cur.execute("""
                        INSERT INTO expense.transactions (uid, transaction_date, purpose, memo, pid, amount_spent, aid, amount_received, is_deleted)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                        RETURNING tid
                    """, (uid, transaction_date, purpose, memo, expense_pid, amount_spent, income_aid, amount_received))
                    row = cur.fetchone()
                    if row is None:
                        return False
                    tid: int = row[0]

                    # 支出の処理
                    if expense_pid is not None:
                        # 支払い方法情報を取得
                        cur.execute("""
                            SELECT aid, closing_day, payment_offset_month, payment_day
                            FROM expense.payments
                            WHERE uid = %s AND pid = %s AND deleted_at IS NULL
                        """, (uid, expense_pid))
                        row = cur.fetchone()
                        if row is None:
                            return False
                        expense_aid: int = row[0]
                        closing_day: int = row[1]
                        payment_offset_month: int = row[2]
                        payment_day: int = row[3]

                        # 支出日を決定
                        if closing_day == 0:
                            payment_date: date = transaction_date
                        else:
                            # 年月を計算（payment_offset_monthを加算）
                            year: int = transaction_date.year
                            month: int = transaction_date.month
                            month += payment_offset_month
                            while month > 12:
                                month -= 12
                                year += 1
                            while month < 1:
                                month += 12
                                year -= 1
                            # 日付の妥当性を確認
                            max_day: int = monthrange(year, month)[1]
                            day: int = min(payment_day, max_day)
                            payment_date = date(year, month, day)

                        # 支出残額を取得
                        cur.execute("""
                            SELECT amount FROM expense.account_histories
                            WHERE aid = %s AND is_deleted = FALSE AND payment_date <= %s
                            ORDER BY payment_date DESC, dorder DESC
                            LIMIT 1
                        """, (expense_aid, payment_date))
                        row = cur.fetchone()
                        expense_balance: int = row[0] if row is not None else 0

                        # 口座履歴を追加
                        cur.execute("""
                            INSERT INTO expense.account_histories (aid, payment_date, tid, amount, is_deleted)
                            VALUES (%s, %s, %s, %s, FALSE)
                        """, (expense_aid, payment_date, tid, expense_balance - amount_spent))

                        # 以降の残高を更新
                        cur.execute("""
                            UPDATE expense.account_histories
                            SET amount = amount - %s
                            WHERE aid = %s AND is_deleted = FALSE AND payment_date > %s
                        """, (amount_spent, expense_aid, payment_date))

                    # 収入の処理
                    if income_aid is not None:
                        income_date: date = transaction_date

                        # 収入残額を取得
                        cur.execute("""
                            SELECT amount FROM expense.account_histories
                            WHERE aid = %s AND is_deleted = FALSE AND payment_date <= %s
                            ORDER BY payment_date DESC, dorder DESC
                            LIMIT 1
                        """, (income_aid, income_date))
                        row = cur.fetchone()
                        income_balance: int = row[0] if row is not None else 0

                        # 口座履歴を追加
                        cur.execute("""
                            INSERT INTO expense.account_histories (aid, payment_date, tid, amount, is_deleted)
                            VALUES (%s, %s, %s, %s, FALSE)
                        """, (income_aid, income_date, tid, income_balance + amount_received))

                        # 以降の残高を更新
                        cur.execute("""
                            UPDATE expense.account_histories
                            SET amount = amount + %s
                            WHERE aid = %s AND is_deleted = FALSE AND payment_date > %s
                        """, (amount_received, income_aid, income_date))

                    conn.commit()
                    return True
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            return False

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
        try:
            with psycopg2.connect(self._dsn) as conn:
                with conn.cursor() as cur:
                    # ユーザIDを取得
                    cur.execute("SELECT uid FROM auth.users WHERE uname = %s", (uname,))
                    row = cur.fetchone()
                    if row is None:
                        return False
                    uid: int = row[0]

                    # 取引日をdate型に変換
                    transaction_date: date = tdate.date()

                    # 取引情報を取得
                    cur.execute("""
                        SELECT tid, pid, aid, amount_spent, amount_received
                        FROM expense.transactions
                        WHERE uid = %s AND transaction_date = %s AND dorder = %s AND is_deleted = FALSE
                    """, (uid, transaction_date, dorder))
                    row = cur.fetchone()
                    if row is None:
                        return False
                    tid: int = row[0]
                    expense_pid: Optional[int] = row[1]
                    income_aid: Optional[int] = row[2]
                    amount_spent: int = row[3]
                    amount_received: int = row[4]

                    # 取引を削除マーク
                    cur.execute("""
                        UPDATE expense.transactions
                        SET is_deleted = TRUE
                        WHERE tid = %s
                    """, (tid,))

                    # 支出取り消し処理
                    if expense_pid is not None:
                        # 支払い方法から口座IDを取得
                        cur.execute("""
                            SELECT aid FROM expense.payments
                            WHERE uid = %s AND pid = %s AND deleted_at IS NULL
                        """, (uid, expense_pid))
                        row = cur.fetchone()
                        if row is not None:
                            expense_aid: int = row[0]

                            # 口座履歴からpayment_dateとdorderを取得
                            cur.execute("""
                                SELECT payment_date, dorder
                                FROM expense.account_histories
                                WHERE aid = %s AND tid = %s AND is_deleted = FALSE
                            """, (expense_aid, tid))
                            row = cur.fetchone()
                            if row is not None:
                                expense_payment_date: date = row[0]
                                expense_dorder: int = row[1]

                                # 口座履歴を削除マーク
                                cur.execute("""
                                    UPDATE expense.account_histories
                                    SET is_deleted = TRUE
                                    WHERE aid = %s AND tid = %s AND is_deleted = FALSE
                                """, (expense_aid, tid))

                                # 以降の残高を更新（支出を取り消すので加算）
                                cur.execute("""
                                    UPDATE expense.account_histories
                                    SET amount = amount + %s
                                    WHERE aid = %s AND is_deleted = FALSE
                                    AND (payment_date > %s OR (payment_date = %s AND dorder > %s))
                                """, (amount_spent, expense_aid, expense_payment_date, expense_payment_date, expense_dorder))

                    # 収入取り消し処理
                    if income_aid is not None:
                        # 口座履歴からpayment_dateとdorderを取得
                        cur.execute("""
                            SELECT payment_date, dorder
                            FROM expense.account_histories
                            WHERE aid = %s AND tid = %s AND is_deleted = FALSE
                        """, (income_aid, tid))
                        row = cur.fetchone()
                        if row is not None:
                            income_payment_date: date = row[0]
                            income_dorder: int = row[1]

                            # 口座履歴を削除マーク
                            cur.execute("""
                                UPDATE expense.account_histories
                                SET is_deleted = TRUE
                                WHERE aid = %s AND tid = %s AND is_deleted = FALSE
                            """, (income_aid, tid))

                            # 以降の残高を更新（収入を取り消すので減算）
                            cur.execute("""
                                UPDATE expense.account_histories
                                SET amount = amount - %s
                                WHERE aid = %s AND is_deleted = FALSE
                                AND (payment_date > %s OR (payment_date = %s AND dorder > %s))
                            """, (amount_received, income_aid, income_payment_date, income_payment_date, income_dorder))

                    conn.commit()
                    return True
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            return False
