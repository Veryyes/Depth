import * as React from 'react';
import { fetchAllSongs, fetchSongLyrics } from '../api';
import { Song } from '../types.d';

export default function SongList({ loadSongData }: { loadSongData: (lyrics: any) => void }) {
  const [songList, setSongList] = React.useState([]);

  async function loadSong(e: React.MouseEvent, songDetails: Song) {
    e.preventDefault();
    const lyrics = await fetchSongLyrics(songDetails.lyrics_path);
    loadSongData(lyrics);
  }

  React.useEffect(() => {
    const fetchData = async () => {
      const songs = await fetchAllSongs();
      setSongList(songs);
    };
    fetchData();
  }, []);

  return (
    <div>
      {songList?.map((songInfo: any) => (
        <>
          <button onClick={e => loadSong(e, songInfo)}>{songInfo.title}</button>
          <br />
        </>
      ))}
    </div>
  );
}
