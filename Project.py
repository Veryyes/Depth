import json

class Project:
    def __init__(self):
        # Path to where this object was last saved/serialized to json
        self.filepath = None
        # Path to the audio file
        self.audio_path = None
        self.song_length = 0
        self.sample_rate = 0

    @classmethod
    def from_json(cls, json_file):
        # This is bad code given that im using this 
        # to load project objects from arbitrary files
        p = cls()
        dictionary = json.load(filename)
        for key in dictionary:
            setattr(p, key, dictionary[key])

        return p

    # TODO add err checking for json
    def to_json(self):
        with open(self.filepath, 'w') as f:
            json.dump(vars(self), f)