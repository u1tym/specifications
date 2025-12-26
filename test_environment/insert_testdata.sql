
insert into auth.users ( uname, upass )
values
 ('admin', 'admin')
,('sample', 'sample');

insert into auth.features (fname, feature_url )
values
 ('ユーザ管理', '/manage')
,('テスト-1', '/test1')
,('テスト-2', '/test2');

insert into auth.user_features ( uid, fid, display_order )
values
 (1, 1, 1)
,(2, 1, 1)
,(2, 2, 2);
