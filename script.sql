create table photo
(
    ID        int auto_increment
        primary key,
    file_path text null,
    name      text null,
    UID       int  null
);

create table users_data
(
    ID                   int auto_increment
        primary key,
    username             varchar(20) not null,
    password             varchar(20) not null,
    phone_number         text        null,
    user_img             text        null,
    user_road_video_path text        null
);

create table video
(
    ID        int auto_increment
        primary key,
    file_path text                               null,
    name      text                               not null,
    UID       int                                null,
    datetime  datetime default CURRENT_TIMESTAMP null
);


