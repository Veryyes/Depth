import * as React from 'react';
import lyricsJson from '../songs/all-star.json';

export default function SongPlayer() {
  const audioRef = React.useRef<HTMLAudioElement>(null);
  const [timeElapsed, setTimeElapsed] = React.useState(0);
  const [showLyrics, setShowLyrics] = React.useState('...');
  const [showNextLine, setShowNextLine] = React.useState('...');

  const lyricsMap = JSON.parse(JSON.stringify(lyricsJson))['mapping'];

  function updateTime() {
    if (audioRef && audioRef.current) {
      setTimeElapsed(Math.round(audioRef.current.currentTime * 1000));
    }
  }

  React.useEffect(() => {
    for (const [i, lyricObj] of lyricsMap.entries()) {
      if (timeElapsed >= lyricObj.start && timeElapsed < lyricObj.end) {
        setShowLyrics(lyricObj.lyrics);
        setShowNextLine(lyricsMap[i + 1]?.lyrics ?? '...');
        break;
      } else {
        setShowLyrics('...');
      }
    }
  }, [lyricsMap, timeElapsed]);

  return (
    <div>
      <h3>{timeElapsed}</h3>
      <audio ref={audioRef} controls onTimeUpdate={updateTime}>
        <source src={`${process.env.PUBLIC_URL}/all-star.mp3`} type="audio/mpeg" />
        Your browser does not support the audio element.
      </audio>
      <h2>{showLyrics}</h2>
      <h4>{showNextLine}</h4>
    </div>
  );
}
