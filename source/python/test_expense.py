# -*- coding: utf-8 -*-

import sys
import warnings

sys.dont_write_bytecode = True
warnings.filterwarnings('ignore')

from expense import Expense
from datetime import datetime as dtm


def main():
    test1()
    return


def test1():
    """
    基本的なテスト
    """
    # DB接続情報（環境に合わせて変更してください）
    e: Expense = Expense("127.0.0.1", 5432, "dbportal", "pusr", "pppp")

    # テスト用ユーザ名（既存のユーザを使用）
    test_user: str = "admin"

    print("=== 口座作成テスト ===")
    result = e.create_account(test_user, "テスト口座1")
    print(f"create_account: {result}")

    print("\n=== 口座削除テスト ===")
    result = e.delete_account(test_user, "テスト口座1")
    print(f"delete_account: {result}")

    print("\n=== 口座作成（削除テスト用） ===")
    result = e.create_account(test_user, "テスト口座2")
    print(f"create_account: {result}")

    print("\n=== 当日払いの支払い方法作成テスト ===")
    result = e.create_immediate_payment(test_user, "現金", "テスト口座2")
    print(f"create_immediate_payment: {result}")

    print("\n=== 後日払いの支払い方法作成テスト ===")
    result = e.create_deferred_payment(test_user, "クレジットカード", "テスト口座2", 25, 1, 10)
    print(f"create_deferred_payment: {result}")

    print("\n=== 支払い方法削除テスト ===")
    result = e.delete_payment(test_user, "現金")
    print(f"delete_payment: {result}")

    print("\n=== 取引追加テスト（支出のみ） ===")
    result = e.add_transaction(
        uname=test_user,
        tdate=dtm(2024, 1, 15, 10, 0, 0),
        purpose="テスト支出",
        memo="テストメモ",
        pname="クレジットカード",
        amount_spent=1000,
        aname=None,
        amount_received=0
    )
    print(f"add_transaction (支出): {result}")

    print("\n=== 取引追加テスト（収入のみ） ===")
    result = e.add_transaction(
        uname=test_user,
        tdate=dtm(2024, 1, 16, 10, 0, 0),
        purpose="テスト収入",
        memo=None,
        pname=None,
        amount_spent=0,
        aname="テスト口座2",
        amount_received=5000
    )
    print(f"add_transaction (収入): {result}")

    print("\n=== 取引追加テスト（支出と収入） ===")
    result = e.add_transaction(
        uname=test_user,
        tdate=dtm(2024, 1, 17, 10, 0, 0),
        purpose="テスト取引",
        memo="支出と収入",
        pname="クレジットカード",
        amount_spent=2000,
        aname="テスト口座2",
        amount_received=3000
    )
    print(f"add_transaction (支出と収入): {result}")

    print("\n=== 取引削除テスト ===")
    result = e.delete_transaction(
        uname=test_user,
        tdate=dtm(2024, 1, 17, 10, 0, 0),
        dorder=1
    )
    print(f"delete_transaction: {result}")

    print("\n=== テスト完了 ===")
    return


if __name__ == '__main__':
    main()
