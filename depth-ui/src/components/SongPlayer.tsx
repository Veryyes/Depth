import * as React from 'react';

export default function SongPlayer({ songJson }: { songJson: Record<string, any> }) {
  const audioRef = React.useRef<HTMLAudioElement>(null);
  const [songURI, setSongURI] = React.useState(`${process.env.PUBLIC_URL}/${songJson.file_name}`);
  const [timeElapsed, setTimeElapsed] = React.useState(0);
  const [showLyrics, setShowLyrics] = React.useState('...');
  const [showNextLine, setShowNextLine] = React.useState('...');

  const lyricsMap = songJson['mapping'];

  function updateTime() {
    if (audioRef && audioRef.current) {
      setTimeElapsed(Math.round(audioRef.current.currentTime * 1000));
    }
  }

  React.useEffect(() => {
    setSongURI(`${process.env.PUBLIC_URL}/${songJson.file_name}`);
    setTimeElapsed(0);
    if (audioRef.current) {
      audioRef.current.load();
    }
  }, [songJson]);

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
        <source src={songURI} type="audio/mpeg" />
        Your browser does not support the audio element.
      </audio>
      <h2>{showLyrics}</h2>
      <h4>{showNextLine}</h4>
    </div>
  );
}
