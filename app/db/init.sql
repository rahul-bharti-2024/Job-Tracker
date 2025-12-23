CREATE TABLE users (
    user_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE companies (
    company_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    website_url TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE job_applications (
    application_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id BIGINT NOT NULL,
    company_id BIGINT NOT NULL,
    external_job_id TEXT NOT NULL,
    job_posting_url TEXT,
    role_title TEXT,
    status TEXT NOT NULL,
    date_applied DATE,
    expected_next_action_date DATE,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now(),
    UNIQUE (user_id, company_id, external_job_id)
);

CREATE INDEX idx_job_applications_user_id
ON job_applications (user_id);

CREATE INDEX idx_job_applications_user_status
ON job_applications (user_id, status);

CREATE INDEX idx_job_applications_user_updated_at
ON job_applications (user_id, updated_at DESC);

