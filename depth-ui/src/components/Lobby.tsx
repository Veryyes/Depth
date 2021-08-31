import * as React from 'react';
import logo from '../karaoke_logo.jpg';
import SongPlayer from './SongPlayer';
import SongList from './SongList';

export default function Lobby() {
  const [currSongJson, setCurrSongJson] = React.useState({});

  function renderPlayer() {
    if (Object.keys(currSongJson).length > 0) {
      return <SongPlayer songJson={currSongJson} />;
    }
    return <h3>Please select a song to sing &lt;3</h3>;
  }

  return (
    <>
      <div className="lobby-top-content">
        <img src={logo} className="App-logo" alt="logo" />
        <SongList loadSongData={setCurrSongJson} />
      </div>
      <div className="lobby-bottom-content">{renderPlayer()}</div>
    </>
  );
}
