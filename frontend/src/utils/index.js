/*
  getColorRemplissage Fonction qui retourne un code couleur en fonction du taux de remplissage
*/

const getColorRemplissage = (reservationNb, praticipantNb) => {
  const intPraticipantNb = parseInt(praticipantNb, 0);
  if (Number.isNaN(intPraticipantNb)) return 'gray';
  if (reservationNb / intPraticipantNb > 1) return 'red';
  if (reservationNb / intPraticipantNb === 1) return 'orange';
  if (reservationNb / intPraticipantNb > 0.5) return 'indigo';
  return 'green';
}

export { getColorRemplissage };
