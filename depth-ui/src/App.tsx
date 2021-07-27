import * as React from 'react';
import logo from './karaoke_logo.jpg';
import './App.css';
import SongPlayer from './components/SongPlayer';
import SongList from './components/SongList';
import allStar from './songs/all-star.json';

// TODO: PULL SONG TEMPO TO CHANGE HOW FAST REACT LOGO SPINS
export default function App() {
  const [currSongJson, setCurrSongJson] = React.useState(allStar);

  return (
    <div className="App">
      <header className="App-header">
        <div style={{ display: 'flex', alignItems: 'right' }}>
          <img src={logo} className="App-logo" alt="logo" />
          <SongList loadSongData={setCurrSongJson} />
        </div>

        <SongPlayer songJson={currSongJson} />
      </header>
    </div>
  );
}
