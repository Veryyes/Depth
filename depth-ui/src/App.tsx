import * as React from 'react';
import logo from './karaoke_logo.jpg';
import './App.css';
import SongPlayer from './components/SongPlayer';
import SongList from './components/SongList';

export default function App() {
  const [currSongJson, setCurrSongJson] = React.useState({});

  function renderPlayer() {
    if (Object.keys(currSongJson).length > 0) {
      return <SongPlayer songJson={currSongJson} />;
    }
    return <h3>Please select a song to sing &lt;3</h3>;
  }

  return (
    <div className="App">
      <header className="App-header">
        <div style={{ display: 'flex', alignItems: 'right' }}>
          <img src={logo} className="App-logo" alt="logo" />
          <SongList loadSongData={setCurrSongJson} />
        </div>
        {renderPlayer()}
      </header>
    </div>
  );
}
