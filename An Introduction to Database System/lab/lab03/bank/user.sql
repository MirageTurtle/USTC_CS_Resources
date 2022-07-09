drop table if exists User;
create table User
(
    Username varchar(50) not null,
    Password varchar(50) not null,
    primary key (Username)
);