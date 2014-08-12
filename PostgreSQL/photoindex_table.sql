-- Table: photoindex

-- DROP TABLE photoindex;

CREATE TABLE photoindex
(
  id serial NOT NULL, -- PK
  Image_DateTime timestamp without time zone,
  EXIF_DateTimeOriginal timestamp without time zone,
  EXIF_DateTimeDigitized timestamp without time zone,
  Image_ExifOffset integer,
  EXIF_SubjectDistanceRange integer,
  EXIF_FlashPixVersion integer,
  EXIF_ExifVersion integer,
  EXIF_FocalLengthIn35mmFilm integer,
  EXIF_InteroperabilityOffset integer,
  Thumbnail_JPEGInterchangeFormat integer,
  EXIF_ExifImageLength integer,
  EXIF_CompressedBitsPerPixel integer,
  EXIF_ExposureBiasValue integer,
  Image_GPSInfo integer,
  Thumbnail_JPEGInterchangeFormatLength integer,
  EXIF_ExifImageWidth integer,
  GPS_GPSAltitudeRef integer,
  EXIF_FocalLength integer,
  Image_XResolution integer,
  EXIF_ISOSpeedRatings integer,
  Image_YResolution integer,
  Thumbnail_XResolution integer,
  Thumbnail_YResolution integer,
  CONSTRAINT "Primary_Key_photoindex" PRIMARY KEY (id )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE photoindex
  OWNER TO imageindexer;
COMMENT ON COLUMN photoindex.id IS 'PK';
