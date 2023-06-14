export interface ResaBilan {
  annulation: boolean
  raison_annulation: string
  id_event: number
  email_numerisateur: string
  commentaire: string
  nb_adultes: number
  nb_moins_6_ans: number
  nb_6_8_ans: number
  nb_9_12_ans: number
  nb_plus_12_ans: number

  // id_numerisateur: number
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
}

/**
 * Statistiques utilisées dans la page BilanStats
 */
export interface Statistics {
  nb_animations: number
  nb_annulation: number 
  taux_remplissage: number
  taux_remplissage_passe: number
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
  id_numerisateur?: number
  numerisateur?: {
    identifiant: string
  }
  id_bilan?: number
}

export interface ResaEventFilters {
  begin_date: string 
  end_date: string 
  search_name?: string 
  'bilan.annulation'?: string 
  published?: boolean
  type_id: string[]
  massif: string[]
}