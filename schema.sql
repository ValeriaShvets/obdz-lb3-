drop table if exists entries;
create table entries (
  id serial primary key not null,
  date timestamp with time zone not null default now(),
  title varchar(80) not null,
  content text not null
);

insert into entries values(1, default, 'l.r.3', 'This is flask app was written by Valeria Shvets KID-21');