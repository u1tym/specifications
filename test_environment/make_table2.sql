create schema expense;

create table expense.accounts (
    aid          SERIAL PRIMARY KEY,
    uid          INTEGER                      NOT NULL,
    account_name TEXT                         NOT NULL,
    is_deleted   BOOLEAN                      DEFAULT FALSE,
    FOREIGN KEY (uid) REFERENCES auth.users(uid) ON DELETE CASCADE,
    UNIQUE(uid, account_name)
);

create table expense.payments (
    pid                  SERIAL PRIMARY KEY,
    uid                  INTEGER                      NOT NULL,
    payment_name         TEXT                         NOT NULL,
    closing_day          INTEGER,
    payment_offset_month INTEGER,
    payment_day          INTEGER,
    aid                  INTEGER,
    deleted_at           DATE,
    FOREIGN KEY (uid) REFERENCES auth.users(uid) ON DELETE CASCADE,
    FOREIGN KEY (aid) REFERENCES expense.accounts(aid),
    UNIQUE(uid, payment_name)
);


create table expense.transactions (
    tid                  SERIAL PRIMARY KEY,
    uid                  INTEGER                      NOT NULL,
    transaction_date     DATE                         NOT NULL, -- 利用日
    dorder               INTEGER                      NOT NULL, -- transaction_date毎のユニークな連番
    purpose              TEXT                         NOT NULL, -- 用途
    memo                 TEXT,
    pid                  INTEGER,
    amount_spent         INTEGER                      NOT NULL DEFAULT 0,
    aid                  INTEGER,
    amount_received      INTEGER                      NOT NULL DEFAULT 0,
    is_deleted           BOOLEAN                      NOT NULL DEFAULT FALSE,
    FOREIGN KEY (uid) REFERENCES auth.users(uid) ON DELETE CASCADE,
    FOREIGN KEY (pid) REFERENCES expense.payments(pid),
    FOREIGN KEY (aid) REFERENCES expense.accounts(aid),
    UNIQUE(uid, transaction_date, dorder)
);

create or replace function expense.set_transactions_dorder()
returns trigger as $$
begin
  NEW.dorder := (
      select coalesce(max(dorder), 0) + 1
      from expense.transactions
      where uid = NEW.uid and transaction_date = NEW.transaction_date
  );
  return NEW;
end;
$$ LANGUAGE plpgsql;

create trigger trg_set_transaction_dorder
before insert on expense.transactions
for each row
execute function expense.set_transactions_dorder();


create table expense.account_histories (
    hid          SERIAL PRIMARY KEY,
    aid          INTEGER                      NOT NULL,
    payment_date DATE                         NOT NULL,
    dorder       INTEGER                      NOT NULL, -- payment_date毎の連番
    tid          INTEGER                      NOT NULL,
    amount       INTEGER                      NOT NULL DEFAULT 0,
    is_deleted   BOOLEAN                      NOT NULL DEFAULT FALSE,
    FOREIGN KEY (aid) REFERENCES expense.accounts(aid),
    FOREIGN KEY (tid) REFERENCES expense.transactions(tid),
    UNIQUE(aid, payment_date, dorder)
);

create or replace function expense.set_account_histories_dorder()
returns trigger as $$
begin
  NEW.dorder := (
      select coalesce(max(dorder), 0) + 1
      from expense.account_histories
      where aid = NEW.aid and payment_date = NEW.payment_date
  );
  return NEW;
end;
$$ LANGUAGE plpgsql;

create trigger trg_set_account_histories_dorder
before insert on expense.account_histories
for each row
execute function expense.set_account_histories_dorder();



---
drop table expense.accounts cascade;
drop table expense.payments cascade;
drop table expense.transactions cascade;
drop table expense.account_histories cascade;
drop function expense.set_transactions_dorder;
drop function expense.set_account_histories_dorder;