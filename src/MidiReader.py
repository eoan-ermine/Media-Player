from mido import Message, MidiFile, MidiTrack

class MidiTrack:
    def __init__(self, idx, track):
        self.idx = idx
        self.track = track
    
    def play(self):
        return self.track.play()
    
    def __str__(self):
        return 'Track {}: {}\n'.format(self.idx, self.track.name) +\
               "\n".join([str(msg) for msg in self.track])

class MidiReader:
    def __init__(self, filename):
        self.midi = MidiFile(filename)
    
    def get_track(self, idx):
        return self.midi.tracks[idx]

    def __str__(self):
        return "\n".join([str(MidiTrack(i, track)) for i, track in enumerate(self.midi.tracks)])
        
if __name__ == "__main__":
    import sys
    
    print(MidiReader(sys.argv[1]))
