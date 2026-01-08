# -*- coding: utf-8 -*-

import sys
import warnings

sys.dont_write_bytecode = True
warnings.filterwarnings('ignore')

from expense import Expense
from datetime import datetime as dtm

# insert into auth.users ( uname, upass ) values ( 'y-toyama', 'bdntspa7' );

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
    test_user: str = "y-toyama"

    print("=== 口座作成 ===")
    result = e.create_account(test_user, "現金")
    print(f"create_account: {result}")

    result = e.create_account(test_user, "北陸銀行")
    print(f"create_account: {result}")
    result = e.create_account(test_user, "北海道銀行")
    print(f"create_account: {result}")
    result = e.create_account(test_user, "楽天銀行")
    print(f"create_account: {result}")
    result = e.create_account(test_user, "auじぶん銀行")
    print(f"create_account: {result}")
    result = e.create_account(test_user, "三井住友銀行(京橋)")
    print(f"create_account: {result}")
    result = e.create_account(test_user, "三井住友銀行(三田通)")
    print(f"create_account: {result}")

    result = e.create_account(test_user, "SUICA")
    print(f"create_account: {result}")
    result = e.create_account(test_user, "MODACA")
    print(f"create_account: {result}")


    print("\n=== 当日払い支払い方法作成 ===")
    result = e.create_immediate_payment(test_user, "現金", "現金")
    print(f"create_immediate_payment: {result}")
    result = e.create_immediate_payment(test_user, "SUICA", "SUICA")
    print(f"create_immediate_payment: {result}")
    result = e.create_immediate_payment(test_user, "MODACA", "MODACA")
    print(f"create_immediate_payment: {result}")
    result = e.create_immediate_payment(test_user, "北陸銀行", "北陸銀行")
    print(f"create_immediate_payment: {result}")
    result = e.create_immediate_payment(test_user, "北海道銀行", "北海道銀行")
    print(f"create_immediate_payment: {result}")
    result = e.create_immediate_payment(test_user, "楽天銀行", "楽天銀行")
    print(f"create_immediate_payment: {result}")
    result = e.create_immediate_payment(test_user, "auじぶん銀行", "auじぶん銀行")
    print(f"create_immediate_payment: {result}")
    result = e.create_immediate_payment(test_user, "三井住友銀行(京橋)", "三井住友銀行(京橋)")
    print(f"create_immediate_payment: {result}")
    result = e.create_immediate_payment(test_user, "三井住友銀行(三田通)", "三井住友銀行(三田通)")
    print(f"create_immediate_payment: {result}")

    print("\n=== 後日払いの支払い方法 ===")
    result = e.create_deferred_payment(test_user, "PayPay", "楽天銀行", 29, 1, 27)
    print(f"create_deferred_payment: {result}")
    result = e.create_deferred_payment(test_user, "auPay", "auじぶん銀行", 15, 1, 10)
    print(f"create_deferred_payment: {result}")

    print("\n=== テスト完了 ===")
    return


if __name__ == '__main__':
    main()
