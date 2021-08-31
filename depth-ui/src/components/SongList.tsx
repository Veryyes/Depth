import * as React from 'react';
import QueueIcon from '@material-ui/icons/Queue';
import { fetchAllSongs, fetchSongLyrics } from '../api';
import { Song } from '../types.d';
import './component.css';

export default function SongList({ loadSongData }: { loadSongData: (lyrics: any) => void }) {
  const dev = false;
  const [songList, setSongList] = React.useState(dev ? ([{ title: 'bro', artist: 'broski' }] as Song[]) : ([] as Song[]));
  const [showMenuFor, setShowMenuFor] = React.useState(-1);

  React.useEffect(() => {
    const fetchData = async () => {
      const songsResponse = await fetchAllSongs();
      setSongList([songsResponse.data]);
    };
    if (!dev) fetchData();
  }, []);

  async function loadSong(e: React.MouseEvent, songDetails: Song) {
    e.preventDefault();
    // const lyrics = await fetchSongLyrics(songDetails.lyrics_path);
    loadSongData(songDetails.lyrics_data);
  }

  async function addToQueue(e: React.MouseEvent) {
    e.stopPropagation();
    console.log('TODO: API request to add to queue');
  }

  return (
    <div className="song-list">
      {songList?.map((songInfo: Song, index: number) => (
        <button
          key={index}
          className="song-button"
          onClick={e => loadSong(e, songInfo)}
          onMouseEnter={() => setShowMenuFor(index)}
          onMouseLeave={() => setShowMenuFor(-1)}
        >
          "{songInfo.title}" - {songInfo.artist}
          {showMenuFor === index ? (
            <button onClick={e => addToQueue(e)} className="add-to-queue">
              <QueueIcon />
            </button>
          ) : null}
        </button>
      ))}
    </div>
  );
}
