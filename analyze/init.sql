CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Table: public.messages

-- DROP TABLE public.messages;

CREATE TABLE public.experiments
(
    id uuid NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    CONSTRAINT experiments_pkey PRIMARY KEY (id)
);

CREATE TABLE public.results
(
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    experiment_id uuid NOT NULL,
    result_name character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT results_pkey PRIMARY KEY (id),
    CONSTRAINT experiment_id_fkey FOREIGN KEY (experiment_id)
    REFERENCES experiments(id) ON DELETE CASCADE
);

TABLESPACE pg_default;

ALTER TABLE public.experiments
    OWNER to admin;

ALTER TABLE public.results
    OWNER to admin;