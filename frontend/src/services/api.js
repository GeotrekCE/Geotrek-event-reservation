import { config } from '@/config/config';

const buildGetUrl = (urlRelative, params = {}) => {
  const url = new URL(`${config.URL_APPLICATION}/${urlRelative}`);
  Object.keys(params)
    .filter((key) => ![null, undefined].includes(params[key]))
    .forEach(
      (key) => { url.searchParams.append(key, params[key]) }
    );
  return url;
}

const callFetchApi = (methode, url, optionsHeaders = {}) => {
  const baseParams = {
    method: methode,
    credentials: 'include',
  }
  const fetchParams = { ...baseParams, ...optionsHeaders }

  return new Promise((resolve, reject) => {
    fetch(url, fetchParams).then((response) => response.json())
      .then((data) => {
        resolve(data);
      })
      .catch((error) => {
        console.error('There was an error!', error);
        reject(error);
      });
  })
}

const getApiData = (route, params) => {
  const url = buildGetUrl(route, params);

  return callFetchApi('GET', url);
}

const deleteApiData = (route) => {
  const url = buildGetUrl(route);
  return callFetchApi('DELETE', url);
}

const postApiData = (route, postData) => {
  const fetchParams = {
    method: 'POST',
    headers: {
      Accept: 'application/json, text/plain, */*',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(postData),
  }

  const url = buildGetUrl(route);
  return callFetchApi('POST', url, fetchParams);
}

export { getApiData, postApiData, deleteApiData };
