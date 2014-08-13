-- Table: multiplephoto

-- DROP TABLE multiplephoto;

CREATE TABLE multiplephoto
(
  id serial NOT NULL, -- PK
  image_datetime timestamp without time zone,
  exif_datetimeoriginal timestamp without time zone,
  exif_datetimedigitized timestamp without time zone,
  image_model character varying,
  CONSTRAINT "Primary_Key_multiplephoto" PRIMARY KEY (id )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE multiplephoto
  OWNER TO imageindexer;
COMMENT ON COLUMN multiplephoto.id IS 'PK';
