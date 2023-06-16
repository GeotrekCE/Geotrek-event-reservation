declare let CONFIGURATION: {
  // URL de l'application Backend résa
  URL_APPLICATION: string,
  // URL GeoTrek Admin
  URL_GTA: string,
  // URL GeoTrek public
  URL_GTR: string,
  // Nombre de jours avant date de début de l'animation
  // ou l'inscription est encore possible
  // (si -1 aucune limitation de date)
  DAY_BEFORE_RESA: number,
  // Nombre de participants surnuméraire accepté
  // en plus du nombre de participants spécifiés dans GeoTrek
  RESA_NB_DELTA: number

  // Date à partir de laquelle les réservations sont ouvertes (PNG)
  RESA_BEGINNING_DATE: Date
}