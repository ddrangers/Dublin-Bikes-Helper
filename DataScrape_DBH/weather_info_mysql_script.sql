create table DBH_schema.weather_info
(
    id           binary(16) default (uuid_to_bin(uuid())) not null
        primary key,
    coord_lon    varchar(20)                              not null,
    coord_lat    varchar(20)                              not null,
    weather_id   int                                      not null,
    weather_main varchar(20)                              not null,
    temp         float                                    not null,
    temp_feel    float                                    null,
    wind_speed   float                                    not null,
    clouds       int                                      null,
    sunrise      datetime                                 null,
    sunset       datetime                                 null,
    creat_time   timestamp  default CURRENT_TIMESTAMP     null comment 'set the creat time',
    delete_flag  int        default 0                     not null comment 'check if the row is deleted'
);


