-- Table: photoindex

-- DROP TABLE photoindex;

CREATE TABLE photoindex
(
  id serial NOT NULL, -- PK
  image_datetime timestamp without time zone,
  exif_datetimeoriginal timestamp without time zone,
  exif_datetimedigitized timestamp without time zone,
  image_exifoffset integer,
  exif_subjectdistancerange integer,
  exif_flashpixversion integer,
  exif_exifversion integer,
  exif_focallengthin35mmfilm integer,
  exif_interoperabilityoffset integer,
  thumbnail_jpeginterchangeformat integer,
  exif_exifimagelength integer,
  exif_compressedbitsperpixel integer,
  exif_exposurebiasvalue integer,
  image_gpsinfo integer,
  thumbnail_jpeginterchangeformatlength integer,
  exif_exifimagewidth integer,
  gps_gpsaltituderef integer,
  exif_focallength integer,
  image_xresolution integer,
  exif_isospeedratings integer,
  image_yresolution integer,
  thumbnail_xresolution integer,
  thumbnail_yresolution integer,
  CONSTRAINT "Primary_Key_photoindex" PRIMARY KEY (id )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE photoindex
  OWNER TO imageindexer;
COMMENT ON COLUMN photoindex.id IS 'PK';
