import { getApiData } from './api';

const URL_GT_API = `${CONFIGURATION.URL_GTA}/api/v2`

const getDistricts = () => getApiData(URL_GT_API, 'district/', { fields: 'id,name' })

const getTouristiceventType = () => getApiData(URL_GT_API, 'touristicevent_type/', {})

const getTouristicEventDetail = (id: number) => getApiData(URL_GT_API, `touristicevent/${id}/`, {})

export { getDistricts, getTouristiceventType, getTouristicEventDetail };
