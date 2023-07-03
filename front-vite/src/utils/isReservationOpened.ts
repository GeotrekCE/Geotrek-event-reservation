import type { ResaEvent } from "@/declaration"
import { formatDateTime } from "./formatDate"

interface ReservationOpened {
  /**
   * Précise si c'est ouvert ou non
   */
  value: boolean

  /**
   * Texte détaillant le pourquoi
   * si la réservation n'est pas ouverte
   */
  text?: string
}

/**
 * Est ce que la réservation est ouverte
 * pour l'événement courant ?
 *
 * Si événement / animation annulée => non
 *
 * Si événement / animation passée => non
 *
 * Si période de réservation trop courte => non
 *
 * Cela dépend s'il est passé => non
 * et s'il on est dans une période correcte
 *
 * ATTENTION: changement au niveau de l'algo pour le PNG,
 * le PNG préfère utiliser une date à partir de laquelle toutes les résas sont possibles,
 * et pas sur une période glissante... => les 2 sont possibles.
 */
export function isReservationOpened(event: ResaEvent): ReservationOpened {

  // Si l'événement est annulé
  if (event.cancelled) return {
    value: false,
    text: 'L\'animation a été annulée.'
  }
  // Si l'événement n'est pas réservable
  if (!event.bookable) return {
    value: false,
    text: 'L\'animation n\'est pas ouverte à la réservation.'
  }

  // Si l'événement est dans le passé
  if (new Date().setHours(0, 0, 0, 0) > new Date(event.begin_date).setHours(0, 0, 0, 0)) {
    return {
      value: false,
      text: 'L\'animation s\'est déjà déroulée.'
    }
  }

  // Si DAY_BEFORE_RESA est renseigné
  if (CONFIGURATION.DAY_BEFORE_RESA !== null) {
    // S'il est à -1 => c'est ouvert
    if (CONFIGURATION.DAY_BEFORE_RESA === -1) return {
      value: true
    }

    // Si la date du jour est avant la période de réservation => pas possible
    const resaBeginDate = new Date(event.begin_date);
    resaBeginDate.setDate(resaBeginDate.getDate() - CONFIGURATION.DAY_BEFORE_RESA);
    if (new Date().setHours(0, 0, 0, 0) < resaBeginDate.setHours(0, 0, 0, 0)) {
      return {
        text: 'L\'animation ne peut pas encore être réservée. (à partir du ' + formatDateTime(resaBeginDate) + ')',
        value: false
      }
    }

  // Si RESA_BEGINNING_DATE est renseigné
  } else if (CONFIGURATION.RESA_BEGINNING_DATE !== null) {
    // Si la date du jour est avant la date d'ouverture des réservations => pas possible
    if (new Date().setHours(0, 0, 0, 0) < CONFIGURATION.RESA_BEGINNING_DATE.valueOf()) {
      console.log(CONFIGURATION.RESA_BEGINNING_DATE)
      return {
        text: 'L\'animation ne peut pas encore être réservée. (à partir du ' + formatDateTime(CONFIGURATION.RESA_BEGINNING_DATE) + ')',
        value: false
      }
    }
  }

  // Dans tous les autres cas, c'est possible
  return {
    value: true
  }
}

/**
 * Est ce que les résas sont "globalement" ouvertes ?
 *
 * Deux cas sont possbiles :
 * * CONFIGURATION.DAY_BEFORE_RESA est = à -1
 * * la date CONFIGURATION.RESA_BEGINNING_DATE est dépassée
 */
export function isReservationGloballyOpened(): ReservationOpened {
  if (CONFIGURATION.DAY_BEFORE_RESA === -1) return { value: true }

  if (CONFIGURATION.RESA_BEGINNING_DATE !== null && new Date().setHours(0, 0, 0, 0) >= CONFIGURATION.RESA_BEGINNING_DATE.valueOf()) {
    return { value: true }
  }

  return {
    value: false
  }
}