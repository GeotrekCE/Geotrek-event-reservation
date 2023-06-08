

CREATE SCHEMA IF NOT EXISTS animations;

DROP TABLE  IF EXISTS animations.t_reservations ;

CREATE TABLE animations.t_reservations (
    id_reservation serial4 NOT NULL,
    nom varchar(250) NULL,
    prenom varchar(250) NULL,
    email varchar(250) NULL,
    tel varchar(100) NULL,
    commentaire varchar(1000) NULL,
    nb_adultes int4 NOT NULL DEFAULT 0,
    nb_moins_6_ans int4 NOT NULL DEFAULT 0,
    nb_6_8_ans int4 NOT NULL DEFAULT 0,
    nb_9_12_ans int4 NOT NULL DEFAULT 0,
    nb_plus_12_ans int4 NOT NULL DEFAULT 0,
    num_departement varchar(250) NULL,
    id_event int4,
    liste_attente boolean default(null),
    meta_create_date timestamp without time zone DEFAULT now(),
    meta_update_date timestamp without time zone,
    token varchar(50),
    confirmed boolean default(false),
    CONSTRAINT t_reservations_pkey PRIMARY KEY (id_reservation),
    CONSTRAINT fk_id_event FOREIGN KEY(id_event)
      REFERENCES tourism_touristicevent(id)
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
    CONSTRAINT t_animations_bilans_pkey PRIMARY KEY (id_bilan),
    CONSTRAINT fk_id_event FOREIGN KEY(id_event)
      REFERENCES tourism_touristicevent(id)
);

DROP TABLE  IF EXISTS animations.t_tokens;

CREATE TABLE animations.t_tokens (
    id serial4 NOT NULL,
    email varchar(250) NOT NULL,
    token varchar(50) NOT NULL,
    used boolean default(false),
    created_at timestamp without time zone DEFAULT now(),
    CONSTRAINT t_tokens_pkey PRIMARY KEY (id)
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


CREATE OR REPLACE VIEW animations.v_export_bilans_global AS
WITH event AS (
  SELECT a.id,
    a.published,
    f.zoning_city,
    g.zoning_district,
    a.name_fr,
    b.type,
    a.begin_date,
    a.end_date,
    a.capacity,
    a.target_audience
  FROM tourism_touristicevent a
  LEFT JOIN tourism_touristiceventtype b ON a.type_id = b.id
  LEFT JOIN ( SELECT array_to_string(array_agg(b_1.name), ', '::text, '*'::text) AS zoning_city,
        a_1.id
        FROM tourism_touristicevent a_1
          JOIN zoning_city b_1 ON st_intersects(a_1.geom, b_1.geom)
      GROUP BY a_1.id) f ON a.id = f.id
  LEFT JOIN ( SELECT array_to_string(array_agg(b_1.name), ', '::text, '*'::text) AS zoning_district,
        a_1.id
        FROM tourism_touristicevent a_1
          JOIN zoning_district b_1 ON st_intersects(a_1.geom, b_1.geom)
      GROUP BY a_1.id) g ON a.id = g.id
  WHERE a.deleted IS FALSE
) , resa AS (
    SELECT
        tr.id_event,
        COALESCE(sum(tr.nb_adultes) FILTER (WHERE NOT tr.liste_attente IS TRUE), 0) AS nb_adultes,
        COALESCE(sum(tr.nb_moins_6_ans) FILTER (WHERE NOT tr.liste_attente IS TRUE), 0) AS nb_moins_6_ans,
        COALESCE(sum(tr.nb_6_8_ans) FILTER (WHERE NOT tr.liste_attente IS TRUE), 0) AS nb_6_8_ans,
        COALESCE(sum(tr.nb_9_12_ans) FILTER (WHERE NOT tr.liste_attente IS TRUE), 0) AS nb_9_12_ans,
        COALESCE(sum(tr.nb_plus_12_ans) FILTER (WHERE NOT tr.liste_attente IS TRUE), 0) AS nb_plus_12_ans,
        COALESCE(sum(tr.nb_adultes + tr.nb_moins_6_ans + tr.nb_6_8_ans + tr.nb_9_12_ans + tr.nb_plus_12_ans) FILTER (WHERE NOT tr.liste_attente IS TRUE), 0) AS nb_total,
        COALESCE(sum(tr.nb_adultes) FILTER (WHERE tr.liste_attente IS TRUE), 0) AS nb_adultes_attente,
        COALESCE(sum(tr.nb_moins_6_ans) FILTER (WHERE tr.liste_attente IS TRUE), 0) AS nb_moins_6_ans_attente,
        COALESCE(sum(tr.nb_6_8_ans) FILTER (WHERE tr.liste_attente IS TRUE), 0) AS nb_6_8_ans_attente,
        COALESCE(sum(tr.nb_9_12_ans) FILTER (WHERE tr.liste_attente IS TRUE), 0) AS nb_9_12_ans_attente,
        COALESCE(sum(tr.nb_plus_12_ans) FILTER (WHERE tr.liste_attente IS TRUE), 0) AS nb_plus_12_ans_attente,
        COALESCE(sum(tr.nb_adultes + tr.nb_moins_6_ans + tr.nb_6_8_ans + tr.nb_9_12_ans + tr.nb_plus_12_ans) FILTER (WHERE tr.liste_attente IS TRUE), 0) AS nb_total_attente
    FROM animations.t_reservations AS tr
    GROUP BY tr.id_event
)
SELECT
    EVENT.*,
    r.nb_total as resa_nb_total,
    r.nb_total_attente as resa_nb_total_attente,
    COALESCE(b.annulation, FALSE) AS annulation,
    -- b.categorie_annulation,  -- mdu: n'existe pas dans la table t_animations_bilan
    b.raison_annulation,
    b.nb_adultes as bilan_nb_adultes,
    b.nb_moins_6_ans as bilan_nb_moins_6_ans,
    b.nb_6_8_ans as bilan_nb_6_8_ans,
    b.nb_9_12_ans as bilan_nb_9_12_ans,
    b.nb_plus_12_ans as bilan_nb_plus_12_ans,
    b.commentaire AS bilan_commentaire,
    r.nb_adultes as resa_nb_adultes,
    r.nb_moins_6_ans as resa_nb_moins_6_ans,
    r.nb_6_8_ans as resa_nb_6_8_ans,
    r.nb_9_12_ans as resa_nb_nb_9_12_ans,
    r.nb_plus_12_ans as resa_nb_plus_12_ans,
    r.nb_adultes_attente as resa_nb_adultes_attente,
    r.nb_moins_6_ans_attente as resa_nb_moins_6_ans_attente,
    r.nb_6_8_ans_attente as resa_nb_6_8_ans_attente,
    r.nb_9_12_ans_attente as resa_nb_9_12_ans_attente,
    r.nb_plus_12_ans_attente as resa_nb_plus_12_ans_attente
FROM EVENT
LEFT OUTER JOIN resa r
ON r.id_event = EVENT.id
LEFT JOIN animations.t_animations_bilans AS b
ON b.id_event = EVENT.id
ORDER BY begin_date DESC;


