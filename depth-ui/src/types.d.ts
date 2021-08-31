export interface Song {
  title: string;
  artist: string;
  genre: string;
  rating: number;
  lyrics_data: Record<string, unknown>;
}
