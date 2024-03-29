export interface ResaBilan {
  id_event: number

  annulation?: boolean
  raison_annulation?: string

  commentaire: string
  nb_adultes: number
  nb_moins_6_ans: number
  nb_6_8_ans: number
  nb_9_12_ans: number
  nb_plus_12_ans: number

  // id_numerisateur: number
  // email_numerisateur: string
}

/**
 * Réservation d'un événement
 *
 * Correspond au retoure de l'API,
 * peut disposer d'un bilan avec quelques sous propriété
 * ainsi qu'un type d'événement.
 */
export interface ResaEvent {
  id: string
  name: string
  bilan: ResaBilan
  description_teaser: string
  type: {
    type: string
  }
  massif: string
  begin_date: string
  end_date: string
  published: boolean
  cancelled: boolean
  bookable: boolean

  sum_participants: number
  sum_participants_liste_attente: number
  sum_participants_adultes: number
  sum_participants_moins_6_ans: number
  sum_participants_6_8_ans: number
  sum_participants_9_12_ans: number
  sum_participants_plus_12_ans: number

}

export interface ResaField {
  name: string,
  label: string,
  class: string,
  type: 'number' | 'date' | 'paragraph' | 'string' | 'boolean'
}

/**
 * Information d'un événement
 * Données issues du endpoint events/{id}/info
 */
export interface ResaEventInfo {
  info_rdv: string
}

/**
 * Statistiques utilisées dans la page BilanStats
 */
export interface Statistics {
  nb_animations?: number
  nb_annulation?: number
  taux_remplissage?: number
  taux_remplissage_passe?: number
}

/**
 * Réservation définie dans le backend Flask
 *
 * La notion de numérisateur tend à disparaître,
 * le parc de la Guadeloupe n'en ayant pas besoin
 * vu que les participants pourront s'inscrire directement.
 */
export interface Resa {
  id_reservation: number
  nom: string
  prenom: string
  tel: string
  email: string
  commentaire: string
  nb_adultes: number
  nb_moins_6_ans: number
  nb_6_8_ans: number
  nb_9_12_ans: number
  nb_plus_12_ans: number
  num_departement: string
  id_event: number
  liste_attente: boolean
  confirmed: boolean
  // id_numerisateur?: number
  // numerisateur?: {
  //   identifiant: string
  // }
  id_bilan?: number
}

export interface ResaEventFilters {
  begin_date: string
  end_date: string
  search_name?: string
  cancelled?: boolean
  published?: boolean
  type_id: string[]
  massif: string[]
}