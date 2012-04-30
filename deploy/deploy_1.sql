CREATE TABLE event_eventtype (
    id int(20) NOT NULL PRIMARY KEY,
    type_name varchar(30) NOT NULL,
    type_image varchar2(100) NOT NULL,
    create_date datetime NOT NULL
)
alter table lesson_course  add column event_type int(20);
INSERT INTO django_content_type (name,app_label,model) values ("eventtype","event","eventtype");
INSERT INTO auth_permission(name,content_type_id,codename) values("Can add event type",11,"add_eventtype");
INSERT INTO auth_permission(name,content_type_id,codename) values("Can change event type",11,"change_eventtype");
INSERT INTO auth_permission(name,content_type_id,codename) values("Can delete event type",11,"delete_eventtype");