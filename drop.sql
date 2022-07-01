SET FOREIGN_KEY_CHECKS=0;

drop table auth_group
, auth_group_permissions
, auth_permission
, auth_user
, auth_user_groups
, auth_user_user_permissions
, django_admin_log
, django_content_type
, django_migrations
, django_session
, jokerauth_sshkey
, oauth2_provider_accesstoken
, oauth2_provider_application
, oauth2_provider_grant
, oauth2_provider_idtoken
, oauth2_provider_refreshtoken
, projects_project
, projects_project_users
, users_systemuser
, users_userdetail             
, users_userdetail_systemuser
;