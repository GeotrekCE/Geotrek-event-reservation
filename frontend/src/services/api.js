import { config } from '@/config/config'

import store from '../store'

const buildGetUrl = (baseUrl, urlRelative, params = {}) => {
  const url = new URL(`${baseUrl}/${urlRelative}`);
  Object.keys(params)
    .filter((key) => ![null, undefined].includes(params[key]))
    .forEach(
      (key) => { url.searchParams.append(key, params[key]) }
    );
  return url;
}

const handleErrors = (response) => {
  if (response.status === 500) {
    throw Error(response.statusText);
  }

  return response.json().then((data) => ({
    status: response.status,
    data,
    error: response.statusText
  }))
}

const callFetchApi = (methode, url, optionsHeaders = {}, message = undefined) => {
  const baseParams = {
    method: methode
  }
  const fetchParams = { ...baseParams, ...optionsHeaders }

  return new Promise((resolve, reject) => {
    fetch(url, fetchParams).then(
      handleErrors
    ).then((response) => {
      const { status, data, error } = response;
      if (status === 200) {
        if (methode !== 'GET' && message) {
          store.dispatch('snackbarSaveInfo', {
            message: data.msg || message,
            color: 'success',
            show: true
          });
        }
        resolve(data);
      } else {
        store.dispatch('snackbarSaveInfo', {
          message: data.msg,
          color: 'error',
          show: true
        });
        reject(response);
      }
      resolve(data);
    }).catch((error) => {
      console.error('There was an error!', error);
      store.dispatch('snackbarSaveInfo', {
        message: error,
        color: 'error',
        show: true
      });
      reject(error);
    });
  })
}

const getApiData = (baseUrl, route, params) => {
  const url = buildGetUrl(baseUrl, route, params);
  let optionsHeaders = {}
  if (baseUrl === config.URL_APPLICATION) {
    optionsHeaders = {
      credentials: 'include'
    }
  }
  return callFetchApi('GET', url, optionsHeaders);
}

const deleteApiData = (baseUrl, route) => {
  const url = buildGetUrl(baseUrl, route);
  return callFetchApi('DELETE', url, { credentials: 'include' });
}

const postApiData = (baseUrl, route, postData, message = true) => {
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
  let snackMessage = false
  if (message) {
    snackMessage = 'Données sauvegardées';
  }
  return callFetchApi('POST', url, fetchParams, snackMessage);
}

export { getApiData, postApiData, deleteApiData };
