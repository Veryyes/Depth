import * as React from 'react';
import logo from './karaoke_logo.jpg';
import './App.css';
import Lobby from './components/Lobby';
import { createLobby } from './api';

export default function App() {
  const [inLobby, setInLobby] = React.useState(false);

  async function handleCreateLobby() {
    await createLobby();
    setInLobby(true);
  }

  return (
    <div className="App">
      {inLobby ? (
        <Lobby />
      ) : (
        <>
        <div className="App-top-content">
          <img src={logo} className="App-logo" alt="logo" />
          </div>
          <div className="App-bottom-content">
          <button className="lobby-button" onClick={handleCreateLobby}>Create lobby</button>
          <br/>
          <button className="lobby-button">Join lobby</button>
        </div>
        </>
      )}
    </div>
  );
}
