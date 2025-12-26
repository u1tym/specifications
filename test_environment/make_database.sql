-- postgres で実行
create user pusr;
alter role pusr with password 'pppp';

create database dbportal encoding 'UTF8' owner pusr;
