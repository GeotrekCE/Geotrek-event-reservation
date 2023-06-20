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
  method: 'GET' | 'POST' | 'DELETE' | 'PUT',
  url: URL | RequestInfo,
  optionsHeaders = {},
  // snackMessage?: boolean | string
): Promise<any> {
  const baseParams = { method }
  const fetchParams = { ...baseParams, ...optionsHeaders }

  const response = await fetch(url, fetchParams)

  let data = { msg: '', error: '' }
  try {
    data = await response.json()
  } catch {
    // we have an error with API server, sometimes the response is not JSON
    // but we don't throw error, just we pass it silently
  }

  if (response.status >= 400) {
    throw Error(response.statusText + '\n' + data?.error);
  }

  return data
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

export function postApiData (baseUrl: string, route: string, postData?: any /*, message = true */) {
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
  // let snackMessage: boolean | string = false
  // if (message) {
  //   snackMessage = 'Données sauvegardées';
  // }
  return callFetchApi('POST', url, fetchParams /*, snackMessage */);
}

export function putApiData (baseUrl: string, route: string, putData: any) {
  const fetchParams = {
    method: 'PUT',
    credentials: 'include',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(putData),
  }

  const url = buildGetUrl(baseUrl, route);
  // let snackMessage: boolean | string = false
  // if (message) {
  //   snackMessage = 'Données sauvegardées';
  // }
  return callFetchApi('PUT', url, fetchParams /*, snackMessage */);
}

export function deleteApiData (baseUrl: string, route: string) {
  const url = buildGetUrl(baseUrl, route);
  return callFetchApi('DELETE', url, { credentials: 'include' });
}
