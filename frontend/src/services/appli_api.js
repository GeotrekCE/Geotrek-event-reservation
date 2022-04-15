import { config } from '@/config/config';
import { getApiData, postApiData, deleteApiData } from '@/services/api';

const getEvents = (params) => getApiData(config.URL_APPLICATION, 'events', params);

const getOneEvent = (id) => getApiData(config.URL_APPLICATION, `events/${id}`);

const deleteOneReservation = (id) => deleteApiData(config.URL_APPLICATION, `reservations/${id}`);

const postOneReservation = (data) => postApiData(config.URL_APPLICATION, 'reservations', data);

export {
  getEvents, getOneEvent, deleteOneReservation, postOneReservation
};
