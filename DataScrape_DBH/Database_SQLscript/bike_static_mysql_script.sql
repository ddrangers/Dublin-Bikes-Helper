create table DBH_schema.bike_static
(
    id           binary(16) default (uuid_to_bin(uuid())) not null
        primary key,
    indexNumber  int                                      not null,
    name         varchar(40)                              not null,
    address      varchar(40)                              null,
    location_lat float                                    not null,
    location_lon float                                    not null,
    creat_time   timestamp  default CURRENT_TIMESTAMP     null comment 'set the creat time',
    delete_flag  int        default 0                     not null comment 'check if the row is deleted'
);


