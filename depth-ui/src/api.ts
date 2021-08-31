import axios, { AxiosRequestConfig, Method } from 'axios';

async function doBasicRequest(verb: Method, url: string) {
  const config: AxiosRequestConfig = {
    method: verb,
    url: url
  };

  try {
    const response = await axios.request(config);
    return response.data;
  } catch (error) {
    console.log(error);
  }
}

export async function createLobby() {
  return doBasicRequest('post', '/api/lobby');
}

// TODO: This will be obsolete once we implement searching
export async function fetchAllSongs() {
  return doBasicRequest('get', 'api/songs/1/metadata');
}

export async function downloadAudio(songId: number) {
  const config: AxiosRequestConfig = {
    method: 'GET',
    headers: {
      'Content-Type': 'audio/mpeg'
    },
    responseType: 'blob'
  };

  try {
    const response = await axios.get(`/api/songs/${songId}/data`, config);
    const blob = new Blob([response.data]);
    const stream: ReadableStream = blob.stream();
    const reader = stream.getReader();
    return reader.read().then(({ done, value }) => {
      while (!done) {
        console.log(value.length);
      }
    });
  } catch (error) {
    console.log(error);
  }
}

export async function fetchSongLyrics(lyricsFilePath: string) {
  return doBasicRequest('get', '/api/songs/lyrics/' + lyricsFilePath);
}
