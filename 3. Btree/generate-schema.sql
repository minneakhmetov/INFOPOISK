create table site
(
    url      text      not null,
    id       bigserial not null
        constraint site_pk
            primary key,
    filename text
);

create unique index site_id_uindex
    on site (id);

create table word
(
    site_id bigint not null,
    word    text   not null
);

create index word_index
    on word (word);
