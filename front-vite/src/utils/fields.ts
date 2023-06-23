import type { ResaField } from '../declaration'

export const fieldsClasseAge = {
  nb_adultes: 'Adultes',
  nb_moins_6_ans: 'Moins de 6 ans',
  nb_6_8_ans: 'Entre 6 et 8 ans',
  nb_9_12_ans: 'Entre 9 et 12 ans',
  nb_plus_12_ans: 'Plus de 12 ans',
}

export type API_FIELDS = Record<string, { label: string, main: boolean, type?: 'html' }>
export const gtApiFields: API_FIELDS = {
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
  capacity: { label: 'Nb participants', main: false },
  'practical_info.fr': { label: 'Info pratique publique', main: true },
  'practical_info.en': { label: 'Info pratique privé', main: true },
  speaker: { label: 'Intervenant', main: true },
  target_audience: { label: 'Public visé', main: true },
}

export const rulesFct = {
  required: (value: any) => !!value || 'Champ obligatoire.',
  integer: (value: any) => (!Number.isNaN(Number(value)) && value !== '') || 'Uniquement des chiffres',
  email: (value: any) => {
    const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    return pattern.test(value) || 'e-mail invalide.'
  },
}

export const expandedFields: ResaField[] = [{
  name: 'nb_adultes',
  label: fieldsClasseAge.nb_adultes,
  class: 'col-span-1 sm:col-span-2',
  type: 'number'
}, {
  name: 'nb_moins_6_ans',
  label: fieldsClasseAge.nb_moins_6_ans,
  class: 'col-span-1 sm:col-span-2',
  type: 'number'
}, {
  name: 'nb_6_8_ans',
  label: fieldsClasseAge.nb_6_8_ans,
  class: 'col-span-1 sm:col-span-2',
  type: 'number'
}, {
  name: 'nb_9_12_ans',
  label: fieldsClasseAge.nb_9_12_ans,
  class: 'col-span-1 sm:col-span-2',
  type: 'number'
}, {
  name: 'nb_plus_12_ans',
  label: fieldsClasseAge.nb_plus_12_ans,
  class: 'col-span-1 sm:col-span-2',
  type: 'number'
}, {
  name: 'confirmed',
  label: 'Confirmé',
  class: 'col-span-1 sm:col-span-2',
  type: 'boolean'
}, {
  name: 'num_departement',
  label: 'Lieu d\'origine',
  class: 'col-span-1 sm:col-span-2',
  type: 'string'
}, {
  name: 'cancelled',
  label: 'Annulée',
  class: 'col-span-1 sm:col-span-2',
  type: 'boolean'
}, {
  name: 'cancel_by',
  label: 'Annulée par',
  class: 'col-span-1 sm:col-span-2',
  type: 'string'
}, {
  name: 'cancel_date',
  label: 'Annulée le',
  class: 'col-span-1 sm:col-span-2',
  type: 'date'
}, {
  name: 'liste_attente',
  label: 'Sur liste d\'attente',
  class: 'col-span-1 sm:col-span-2',
  type: 'boolean'
}, {
  name: 'commentaire',
  label: 'Commentaire',
  class: 'col-span-full mb-8',
  type: 'paragraph'
}, {
  name: 'meta_create_date',
  label: 'Date de création',
  class: 'col-span-1 sm:col-span-5',
  type: 'date'
}, {
  name: 'meta_update_date',
  label: 'Date de mise à jour',
  class: 'col-span-1 sm:col-span-5',
  type: 'date'
}]
