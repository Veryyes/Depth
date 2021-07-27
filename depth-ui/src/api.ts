import axios from 'axios';

export async function fetchAllSongs() {
  try {
    const response = await axios.get('/api/songs');
    return response.data;
  } catch (error) {
    console.log(error);
  }
}

export async function downloadMp3(songFilePath: string) {
  try {
    const response = await axios.get('/api/songs/mp3/' + songFilePath);
    return response.data;
  } catch (error) {
    console.log(error);
  }
}

export async function fetchSongLyrics(lyricsFilePath: string) {
  try {
    const response = await axios.get('/api/songs/lyrics/' + lyricsFilePath);
    return response.data;
  } catch (error) {
    console.log(error);
  }
}
