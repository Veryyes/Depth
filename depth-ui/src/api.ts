import axios from 'axios';

// TODO: UPDATE URLs ONCE BACKEND CODE IS DONE
export async function fetchAllSongs() {
  try {
    const response = await axios.get('/api/songs');
    return response.data;
  } catch (error) {
    console.log(error);
  }
}

export async function fetchSongLyrics(songTitle: string) {
  try {
    const response = await axios.get('/api/songs/' + songTitle);
    return response.data;
  } catch (error) {
    console.log(error);
  }
}
