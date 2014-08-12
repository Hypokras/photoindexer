-- Table: multiplephoto

-- DROP TABLE multiplephoto;

CREATE TABLE multiplephoto
(
  id serial NOT NULL, -- PK
  Image_DateTime timestamp without time zone,
  EXIF_DateTimeOriginal timestamp without time zone,
  EXIF_DateTimeDigitized timestamp without time zone,
  Image_Model character varying,
  CONSTRAINT "Primary_Key_multiplephoto" PRIMARY KEY (id )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE multiplephoto
  OWNER TO imageindexer;
COMMENT ON COLUMN multiplephoto.id IS 'PK';
