

CREATE SCHEMA IF NOT EXISTS animations;

DROP TABLE  IF EXISTS animations.t_reservations ;

CREATE TABLE animations.t_reservations (
    id_reservation serial4 NOT NULL,
    nom varchar(250) NULL,
    prenom varchar(250) NULL,
    tel varchar(100) NULL,
    commentaire varchar(1000) NULL,
    nb_adultes int4 NOT NULL DEFAULT 0,
    nb_moins_6_ans int4 NOT NULL DEFAULT 0,
    nb_6_8_ans int4 NOT NULL DEFAULT 0,
    nb_9_12_ans int4 NOT NULL DEFAULT 0,
    nb_plus_12_ans int4 NOT NULL DEFAULT 0,
    num_departement varchar(250) NULL,
    id_event int4 NULL,
    id_numerisateur int4 NULL,
    commentaire_numerisateur varchar(250) NULL,
    liste_attente boolean default(null),
    meta_create_date timestamp without time zone DEFAULT now(),
    meta_update_date timestamp without time zone,
    CONSTRAINT t_reservations_pkey PRIMARY KEY (id_reservation)
);

DROP TABLE  IF EXISTS animations.t_animations_bilans ;

CREATE TABLE animations.t_animations_bilans (
    id_bilan serial4 NOT NULL,
    annulation BOOLEAN NOT NULL DEFAULT(FALSE),
    raison_annulation varchar(1000) NULL,
    nb_adultes int4 NOT NULL DEFAULT 0,
    nb_moins_6_ans int4 NOT NULL DEFAULT 0,
    nb_6_8_ans int4 NOT NULL DEFAULT 0,
    nb_9_12_ans int4 NOT NULL DEFAULT 0,
    nb_plus_12_ans int4 NOT NULL DEFAULT 0,
    id_event int4 NULL,
    id_numerisateur int4 NULL,
    commentaire varchar(1000) NULL,
    meta_create_date timestamp without time zone DEFAULT now(),
    meta_update_date timestamp without time zone,
    CONSTRAINT t_animations_bilans_pkey PRIMARY KEY (id_bilan)
);

CREATE OR REPLACE FUNCTION animations.get_secteur_name(id_event integer)
 RETURNS character varying
 LANGUAGE sql
AS $function$
    SELECT zd."name"
        FROM public.tourism_touristicevent AS tt
        JOIN public.zoning_district AS zd
        ON st_intersects(zd.Geom, tt.geom)
        WHERE tt.id = id_event
        LIMIT 1;
$function$
;

CREATE OR REPLACE FUNCTION animations.fct_trg_meta_dates_change()
    RETURNS trigger AS
    $BODY$
        BEGIN
            IF(TG_OP = 'INSERT') THEN
                    NEW.meta_create_date = NOW();
            ELSIF(TG_OP = 'UPDATE') THEN
                    NEW.meta_update_date = NOW();
                    IF(NEW.meta_create_date IS NULL) THEN
                            NEW.meta_create_date = NOW();
                    END IF;
            END IF;
            RETURN NEW;
        END;
    $BODY$
LANGUAGE plpgsql VOLATILE
COST 100;


CREATE TRIGGER tri_meta_dates_change_t_reservations
  BEFORE INSERT OR UPDATE
  ON animations.t_reservations
  FOR EACH ROW
  EXECUTE PROCEDURE animations.fct_trg_meta_dates_change();

CREATE TRIGGER tri_meta_dates_change_t_animations_bilans
  BEFORE INSERT OR UPDATE
  ON animations.t_animations_bilans
  FOR EACH ROW
  EXECUTE PROCEDURE animations.fct_trg_meta_dates_change();