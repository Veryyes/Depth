import * as React from 'react';

export default function SongQueue() {
  const [queue, setQueue] = React.useState([]);

  React.useEffect(() => {
    // on render, load song queue via API
  }, []);
}
