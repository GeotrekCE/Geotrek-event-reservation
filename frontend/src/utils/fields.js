const fieldsClasseAge = {
  nb_adultes: 'Adultes',
  nb_moins_6_ans: 'Moins de 6 ans',
  nb_6_8_ans: 'Entre 6 et 8 ans',
  nb_9_12_ans: 'Entre 9 et 12 ans',
  nb_plus_12_ans: 'Plus de 12 ans',
}

const rulesFct = {
  required: (value) => !!value || 'Champ obligatoire.',
  integer: (value) => (!Number.isNaN(Number(value)) && value !== '') || 'Uniquement des chiffres',
  email: (value) => {
    const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    return pattern.test(value) || 'Invalid e-mail.'
  },
}

export { fieldsClasseAge, rulesFct }
