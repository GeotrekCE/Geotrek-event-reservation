import type { ResaEvent } from '@/declaration';
import { getApiData, postApiData, deleteApiData } from './api';

const getEvents = (params: any) => {
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

const getOneEvent = (id: any): Promise<ResaEvent> => getApiData(CONFIGURATION.URL_APPLICATION, `events/${id}`);

const deleteOneReservation = (id: any) => deleteApiData(CONFIGURATION.URL_APPLICATION, `reservations/${id}`);

const postOneReservation = (data: any) => postApiData(CONFIGURATION.URL_APPLICATION, 'reservations', data);

export interface DataConfirmReservation {
  resa_token: string;
}
export const confirmReservation = (data: DataConfirmReservation) => postApiData(CONFIGURATION.URL_APPLICATION, 'reservations/confirm', data)

const postLogin = (data: any) => postApiData(CONFIGURATION.URL_APPLICATION, 'auth/login', data, false);

const postOneBilan = (data: any) => postApiData(CONFIGURATION.URL_APPLICATION, 'bilans', data);

const getGlobalStats = (data: any) => getApiData(CONFIGURATION.URL_APPLICATION, 'stats/global', data);

const getGraphStats = (url: string, data: any) => getApiData(CONFIGURATION.URL_APPLICATION, url, data);

export {
  postLogin,
  getEvents,
  getOneEvent,
  deleteOneReservation,
  postOneReservation,
  postOneBilan,
  getGlobalStats,
  getGraphStats
};
