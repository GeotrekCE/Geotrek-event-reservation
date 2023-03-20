CREATE EXTENSION postgres_fdw;

CREATE SERVER usershubdb
    FOREIGN DATA WRAPPER postgres_fdw
    OPTIONS (host '${MON_HOTE}', dbname '${MA_BASE_UH}');


CREATE USER MAPPING FOR ${GEOTREK_USER}
    SERVER usershubdb
    OPTIONS (user '${MON_USER}', password '${MON_PASS');


CREATE SCHEMA utilisateurs;
IMPORT FOREIGN SCHEMA utilisateurs
FROM SERVER usershubdb INTO utilisateurs;
