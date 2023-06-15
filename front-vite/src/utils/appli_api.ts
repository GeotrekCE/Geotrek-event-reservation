import type { ResaEvent } from '@/declaration';
import { getApiData, postApiData, deleteApiData, putApiData } from './api';


/**
 * Réservations
 */
export interface DataConfirmReservation {
  resa_token: string;
}
export const confirmReservation = (data: DataConfirmReservation) => postApiData(CONFIGURATION.URL_APPLICATION, 'reservations/confirm', data)

export async function getReservations (params: Record<string, any> = {}) {
  return getApiData(CONFIGURATION.URL_APPLICATION, 'reservations', {
    page: 1,
    limit: 10,
    ...params
  })
}

export const deleteReservation = (id: any) => deleteApiData(CONFIGURATION.URL_APPLICATION, `reservations/${id}`);

export const postReservation = (data: any) => postApiData(CONFIGURATION.URL_APPLICATION, 'reservations', data);

export const updateReservation = (id: number, data: any) => putApiData(CONFIGURATION.URL_APPLICATION, `reservations/${id}`, data);



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
        'bilan'
      ]
    }
  }
  return getApiData(CONFIGURATION.URL_APPLICATION, 'events', getparams);
}

export const getEvent = (id: any): Promise<ResaEvent> => getApiData(CONFIGURATION.URL_APPLICATION, `events/${id}`);

export const postBilan = (data: any) => postApiData(CONFIGURATION.URL_APPLICATION, 'bilans', data);

/**
 * Statistiques
 */
export const getGlobalStats = (data: any) => getApiData(CONFIGURATION.URL_APPLICATION, 'stats/global', data);

export const getGraphStats = (url: string, data: any) => getApiData(CONFIGURATION.URL_APPLICATION, url, data);
