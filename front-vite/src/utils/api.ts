import { pinia } from '@/plugins/pinia'
import { useAppStore } from '@/stores/app'

const appStore = useAppStore(pinia)

function buildGetUrl (baseUrl: string, urlRelative: string, params: Record<string, any> = {}): URL {
  const url = new URL(`${baseUrl}/${urlRelative}`);
  Object.keys(params)
    .filter((key) => ![null, undefined].includes(params[key]))
    .forEach(
      (key) => { url.searchParams.append(key, params[key]) }
    );
  return url;
}

async function callFetchApi (
  method: 'GET' | 'POST' | 'DELETE',
  url: URL | RequestInfo,
  optionsHeaders = {},
  snackMessage?: boolean | string
) {
  const baseParams = { method }
  const fetchParams = { ...baseParams, ...optionsHeaders }


  try {
    const response = await fetch(url, fetchParams)
    if (response.status === 500) {
      throw Error(response.statusText);
    }
    let data = { msg: '' }
    try {
      data = await response.json()
    } catch {
      // we have an error with API server, sometimes the response is not JSON
    }

    if (response.status === 200) {
      if (method !== 'GET' && snackMessage) {
        appStore.snackbarInfo = {
          message: data.msg || snackMessage,
          color: 'success',
          show: true
        };
      }
      return data;
    } else {
      appStore.snackbarInfo = {
        message: data.msg,
        color: 'error',
        show: true
      }
      return {
        status: response.status,
        data,
        error: response.statusText
      }
    }
  } catch (error: any) {
    console.error('There was an error!', error);
    appStore.snackbarInfo = {
      message: error,
      color: 'error',
      show: true
    }
    throw new Error(error as string)
  }

}

export function getApiData (baseUrl: string, route: string, params?: any) {
  const url = buildGetUrl(baseUrl, route, params);
  let optionsHeaders = {}
  if (baseUrl === CONFIGURATION.URL_APPLICATION) {
    optionsHeaders = {
      credentials: 'include'
    }
  }
  return callFetchApi('GET', url, optionsHeaders);
}

export function postApiData (baseUrl: string, route: string, postData: any, message = true) {
  const fetchParams = {
    method: 'POST',
    credentials: 'include',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(postData),
  }

  const url = buildGetUrl(baseUrl, route);
  let snackMessage: boolean | string = false
  if (message) {
    snackMessage = 'Données sauvegardées';
  }
  return callFetchApi('POST', url, fetchParams, snackMessage);
}

export function deleteApiData (baseUrl: string, route: string) {
  const url = buildGetUrl(baseUrl, route);
  return callFetchApi('DELETE', url, { credentials: 'include' });
}
