const fieldsClasseAge = {
  nb_adultes: 'Adultes',
  nb_moins_6_ans: 'Moins de 6 ans',
  nb_6_8_ans: 'Entre 6 et 8 ans',
  nb_9_12_ans: 'Entre 9 et 12 ans',
  nb_plus_12_ans: 'Plus de 12 ans',
}

const gtApiFields = {
  booking: { label: 'Reservation', main: false },
  contact: { label: 'Contact', main: false },
  'name.fr': { label: 'Nom', main: false },
  'description_teaser.fr': { label: 'Description courte', type: 'html', main: false },
  'description.fr': { label: 'Description', type: 'html', main: false },
  'accessibility.fr': { label: 'Accessibilité', type: 'html', main: false },
  duration: { label: 'Durée', main: true },
  email: { label: 'Email', main: false },
  begin_date: { label: 'Date début', main: false },
  end_date: { label: 'Date fin', main: false },
  meeting_point: { label: 'Lieu de RDV', main: true },
  meeting_time: { label: 'Heure de RDV', main: true },
  organizer: { label: 'Organisateur', main: false },
  participant_number: { label: 'Nb participants', main: false },
  'practical_info.fr': { label: 'Info pratique publique', main: true },
  'practical_info.en': { label: 'Info pratique privé', main: true },
  speaker: { label: 'Intervenant', main: true },
  target_audience: { label: 'Public visé', main: true },
}

const rulesFct = {
  required: (value) => !!value || 'Champ obligatoire.',
  integer: (value) => (!Number.isNaN(Number(value)) && value !== '') || 'Uniquement des chiffres',
  email: (value) => {
    const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    return pattern.test(value) || 'Invalid e-mail.'
  },
}

export { fieldsClasseAge, rulesFct, gtApiFields }
