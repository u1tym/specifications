-- postgres で実行
create user pusr;
alter role pusr with password 'pppp';

create database dbauth encoding 'UTF8' owner pusr;
