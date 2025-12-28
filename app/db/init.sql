CREATE TABLE users (
    user_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);
CREATE TABLE companies (
    company_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    website_url TEXT,
    location TEXT,
    industry TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);
CREATE TABLE resume_versions (
    resume_version_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INT NOT NULL,
    external_link TEXT NOT NULL,
    version_name TEXT NOT NULL,
    uploaded_at TIMESTAMP NOT NULL DEFAULT now()
);
CREATE TABLE job_applications (
    application_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    user_id INT NOT NULL,
    company_id INT NOT NULL,

    role_title TEXT NOT NULL,
    source TEXT NOT NULL,              -- portal | referral | career_page
    current_status TEXT NOT NULL,      -- validated via Pydantic enum

    applied_date DATE,
    deadline_date DATE,

    resume_version_id INT,

    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now(),

    UNIQUE (user_id, company_id, role_title)
);
CREATE TABLE status_history (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    application_id INT NOT NULL,
    status TEXT NOT NULL,
    changed_at TIMESTAMP NOT NULL DEFAULT now()
);
CREATE TABLE tags (
    tag_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
CREATE TABLE application_tags (
    application_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (application_id, tag_id)
);
CREATE TABLE notes (
    note_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INT NOT NULL,
    application_id INT,
    company_id INT,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);
CREATE TABLE reminders (
    reminder_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INT NOT NULL,
    application_id INT NOT NULL,
    type TEXT NOT NULL,               -- deadline | interview | follow-up
    scheduled_time TIMESTAMP NOT NULL,
    message TEXT NOT NULL,
    sent BOOLEAN NOT NULL DEFAULT FALSE
);
CREATE INDEX idx_applications_user
ON job_applications (user_id);

CREATE INDEX idx_applications_status
ON job_applications (current_status);

CREATE INDEX idx_applications_updated
ON job_applications (updated_at DESC);

CREATE INDEX idx_status_history_application
ON status_history (application_id);

CREATE INDEX idx_reminders_scheduled
ON reminders (scheduled_time);
