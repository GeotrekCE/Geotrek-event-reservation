import { config } from '@/config/config'

const buildGetUrl = (baseUrl, urlRelative, params = {}) => {
  const url = new URL(`${baseUrl}/${urlRelative}`);
  Object.keys(params)
    .filter((key) => ![null, undefined].includes(params[key]))
    .forEach(
      (key) => { url.searchParams.append(key, params[key]) }
    );
  return url;
}

const callFetchApi = (methode, url, optionsHeaders = {}) => {
  const baseParams = {
    method: methode
  }
  const fetchParams = { ...baseParams, ...optionsHeaders }

  return new Promise((resolve, reject) => {
    fetch(url, fetchParams).then(
      (response) => {
        if (response.status === 404) {
          return [];
        }
        return response.json();
      }
    )
      .then((data) => {
        resolve(data);
      })
      .catch((error) => {
        console.error('There was an error!', error);
        reject(error);
      });
  })
}

const getApiData = (baseUrl, route, params) => {
  const url = buildGetUrl(baseUrl, route, params);
  let optionsHeaders = {}
  if (baseUrl === config.URL_APPLICATION) {
    optionsHeaders = { credentials: 'include' }
  }
  return callFetchApi('GET', url, optionsHeaders);
}

const deleteApiData = (baseUrl, route) => {
  const url = buildGetUrl(baseUrl, route);
  return callFetchApi('DELETE', url, { credentials: 'include' });
}

const postApiData = (baseUrl, route, postData) => {
  const fetchParams = {
    method: 'POST',
    credentials: 'include',
    headers: {
      Accept: 'application/json, text/plain, */*',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(postData),
  }

  const url = buildGetUrl(baseUrl, route);
  return callFetchApi('POST', url, fetchParams);
}

export { getApiData, postApiData, deleteApiData };
