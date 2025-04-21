create table if not exists users(
    id bigint auto_increment primary key,
    name varchar(255) not null,
    date_of_birth date not null,
    gender varchar(10) not null,  -- Updated to match the schema
    phone_number varchar(20) not null,  -- Updated to match the schema
    email varchar(255) not null unique,  -- Added unique constraint for email
    password varchar(255) not null,
    city varchar(255) not null,
    state varchar(255) not null,
    country varchar(255) not null
);




