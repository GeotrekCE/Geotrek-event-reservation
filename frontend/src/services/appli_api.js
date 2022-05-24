import { config } from '@/config/config';
import { getApiData, postApiData, deleteApiData } from '@/services/api';

const getEvents = (params) => {
  const getparams = {
    ...params,
    ...{
      fields: [
        'id',
        'begin_date',
        'sum_participants',
        'participant_number',
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
  return getApiData(config.URL_APPLICATION, 'events', getparams);
}

const getOneEvent = (id) => getApiData(config.URL_APPLICATION, `events/${id}`);

const deleteOneReservation = (id) => deleteApiData(config.URL_APPLICATION, `reservations/${id}`);

const postOneReservation = (data) => postApiData(config.URL_APPLICATION, 'reservations', data);

const postLogin = (data) => postApiData(config.URL_APPLICATION, 'auth/login', data, false);

const postOneBilan = (data) => postApiData(config.URL_APPLICATION, 'bilans', data);

export {
  postLogin,
  getEvents,
  getOneEvent,
  deleteOneReservation,
  postOneReservation,
  postOneBilan
};
