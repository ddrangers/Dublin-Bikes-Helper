create table DBH_schema.bike_info
(
    id                   binary(16) default (uuid_to_bin(uuid())) not null
        primary key,
    number               int                                      not null,
    name                 varchar(40)                              not null,
    address              varchar(40)                              null,
    bike_stand           int                                      not null,
    bike_stand_available int                                      not null,
    bike_available       int                                      not null,
    status               varchar(20)                              not null,
    last_update          timestamp                                null,
    creat_time           timestamp  default CURRENT_TIMESTAMP     null comment 'set the creat time',
    delete_flag          int        default 0                     not null comment 'check if the row is deleted'
);


