import * as React from 'react';
import { fetchAllSongs, fetchSongLyrics } from '../api';
import allStar from '../songs/all-star.json';
import hero from '../songs/holding-out-for-a-hero.json';

// TODO: UNCOMMENT AXIOS CALLS WHEN API CODE IS DONE
export default function SongList({ loadSongData }: { loadSongData: (lyrics: any) => void }) {
  const [songList, setSongList] = React.useState(['All Star', 'Holding Out For A Hero']);

  async function loadSong(e: React.MouseEvent, title: string) {
    e.preventDefault();
    // const lyrics = await fetchSongLyrics(title);
    const lyrics = title === 'All Star' ? allStar : hero;
    loadSongData(lyrics);
  }

  // React.useEffect(() => {
  //   const fetchData = async () => {
  //     const songs = await fetchAllSongs();
  //     setSongList(songs);
  //   };
  //   fetchData();
  // }, []);

  return (
    <div>
      {songList.map((songTitle: string) => (
        <>
          <button onClick={e => loadSong(e, songTitle)}>{songTitle}</button>
          <br />
        </>
      ))}
    </div>
  );
}
