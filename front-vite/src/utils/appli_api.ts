import type { ResaEvent } from '@/declaration';
import { getApiData, postApiData, deleteApiData } from './api';


/**
 * Réservations
 */
export interface DataConfirmReservation {
  resa_token: string;
}
export const confirmReservation = (data: DataConfirmReservation) => postApiData(CONFIGURATION.URL_APPLICATION, 'reservations/confirm', data)

export async function getReservations (page = 1, limit = 10, sortField = null, sortOrder = null) {
  return getApiData(CONFIGURATION.URL_APPLICATION, 'reservations', {
    page,
    limit,
    sortBy: sortField,
    sortDesc: sortOrder === -1
  })
}

export const deleteReservation = (id: any) => deleteApiData(CONFIGURATION.URL_APPLICATION, `reservations/${id}`);

export const postReservation = (data: any) => postApiData(CONFIGURATION.URL_APPLICATION, 'reservations', data);


/**
 * Authentification
 */
export const postLogin = (data: any) => postApiData(CONFIGURATION.URL_APPLICATION, 'auth/login', data, false);

/**
 * Événements / Animations
 */
export const getEvents = (params: any) => {
  const getparams = {
    ...params,
    ...{
      fields: [
        'id',
        'begin_date',
        'sum_participants',
        'capacity',
        'sum_participants_liste_attente',
        'type',
        'name',
        'massif',
        'end_date',
        'published',
        'bilan.annulation'
      ]
    }
  }
  return getApiData(CONFIGURATION.URL_APPLICATION, 'events', getparams);
}

export const getOneEvent = (id: any): Promise<ResaEvent> => getApiData(CONFIGURATION.URL_APPLICATION, `events/${id}`);

export const postOneBilan = (data: any) => postApiData(CONFIGURATION.URL_APPLICATION, 'bilans', data);

/**
 * Statistiques
 */
export const getGlobalStats = (data: any) => getApiData(CONFIGURATION.URL_APPLICATION, 'stats/global', data);

export const getGraphStats = (url: string, data: any) => getApiData(CONFIGURATION.URL_APPLICATION, url, data);
