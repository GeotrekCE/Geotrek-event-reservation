import { config } from '@/config/config';
import { getApiData } from '@/services/api';

const getDistricts = () => getApiData(config.URL_GT_API, 'district/', { fields: 'id,name' })

const getTouristiceventType = () => getApiData(config.URL_GT_API, 'touristicevent_type/', {})

const getTouristicEventDetail = (id) => getApiData(config.URL_GT_API, `touristicevent/${id}`, {})

export { getDistricts, getTouristiceventType, getTouristicEventDetail };
