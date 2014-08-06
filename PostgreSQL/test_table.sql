-- Table: test

-- DROP TABLE test;

CREATE TABLE test
(
  id serial NOT NULL, -- PK
  name character varying,
  path character varying,
  datetime timestamp without time zone,
  imagemodel character varying,
  CONSTRAINT "Primary_Key" PRIMARY KEY (id )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE test
  OWNER TO imageindexer;
COMMENT ON COLUMN test.id IS 'PK';
