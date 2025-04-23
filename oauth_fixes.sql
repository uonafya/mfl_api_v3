--- Alter tables - Default oauth

alter table oauth2_provider_accesstoken
add column created timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
add column updated timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
add column source_refresh_token_id int8 NULL,
add column id_token_id int8 NULL,
add CONSTRAINT oauth2_provider_accesstoken_id_token_id_key UNIQUE (id_token_id);


alter table oauth2_provider_application
add column created timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
add column updated timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
add column algorithm varchar(5) NOT NULL DEFAULT '',
add column post_logout_redirect_uris text NOT NULL DEFAULT '';


alter table oauth2_provider_grant
add column created timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
add column updated timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
add column code_challenge varchar(128) NOT NULL DEFAULT '',
add column code_challenge_method varchar(10) NOT NULL DEFAULT '',
add column nonce varchar(255) NOT NULL DEFAULT '',
add column claims text NOT NULL DEFAULT '';

alter table oauth2_provider_refreshtoken
add column created timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
add column updated timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
add column revoked timestamptz NULL;


--- Alter tables - Custom oauth

alter table users_mfloauthapplication
add column created timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
add column updated timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
add column algorithm varchar(5) NOT NULL DEFAULT '',
add column post_logout_redirect_uris text NOT NULL DEFAULT '';


--- create missing table
CREATE TABLE oauth2_provider_idtoken (
    id BIGSERIAL PRIMARY KEY,
    jti UUID UNIQUE DEFAULT gen_random_uuid() NOT NULL,
    expires TIMESTAMP NOT NULL,
    scope TEXT DEFAULT '',
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    application_id INTEGER REFERENCES users_mfloauthapplication(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users_mfluser(id) ON DELETE CASCADE,
    CONSTRAINT fk_oauth2_provider_idtoken_application FOREIGN KEY (application_id) REFERENCES users_mfloauthapplication(id) ON DELETE CASCADE,
    CONSTRAINT fk_oauth2_provider_idtoken_user FOREIGN KEY (user_id) REFERENCES users_mfluser(id) ON DELETE CASCADE
);

