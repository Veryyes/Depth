import logo from './logo.svg';
import './App.css';
import SongPlayer from './components/SongPlayer';

function App() {

    return (
		<div className = "App" >
        <header className = "App-header" >
        	<img src = { logo } className = "App-logo" alt = "logo" / >
        	<SongPlayer / >
        </header>
        </div>
    );
}

export default App;
