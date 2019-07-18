from midiutil.MidiFile import MIDIFile
import os

def _create_midi_mapping():
    """ Create a dictionary that maps note name to midi note integer """
    middle_c = 60
    notes = "c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"
    equiv = (("c#", "db"), ("d#", "eb"), 
              ("f#", "gb"), ("g#", "ab"), ("a#", "bb"))
    m = {}
    
    j, o = len(notes)-1, 3
    for v in range(middle_c-1, -1, -1):
        for e in equiv: m[notes[j].replace(*e) + str(o)] = v
        if j == 0: o -= 1
        j = (j - 1) % len(notes)
        
    j, o = 0, 4
    for v in range(middle_c, 128):
        for e in equiv: m[notes[j].replace(*e) + str(o)] = v
        j = (j + 1) % len(notes)
        if j == 0: o += 1
        
    return m


_midi_mapping = _create_midi_mapping()


class Song(MIDIFile):
    _valid = tuple, list, type(x for x in range(1))
    def __init__(self, name="test", tempo=100, num_tracks=1):
        """
        Intialize Song object.
        name: str, name of song/file.
        tempo: int, bpm of song.
        num_tracks: int, number of tracks for the midi file to have.
        """
        super().__init__(num_tracks)
        self.name, self.tempo, self.volume = name, tempo, 100
        self.filename = "%s.mid" % name
        track, self.channel = 0, 0
        self.time = [0]*num_tracks # start each track at the beginning
        self.addTempo(track, self.time[0], self.tempo)
        
    def addNote(self, notes, duration=4, track=0):
        """
        Overrides MIDIFile's addNote method, but uses it as a subroutine. Adds
        a note or notes with a duration to the specified track, then increments
        the time by that duration.
        
        notes: str or tuple of strs, notes to add at the current location of
               of the track.
        duration: float, number of beats for the note/chord.
        track: int, which track to add to.
        """
        if not isinstance(notes, Song._valid): notes = notes,
        for note in notes:
            note = note.lower()
            if note in _midi_mapping: pitch = _midi_mapping[note]
            elif note+"4" in _midi_mapping: pitch = _midi_mapping[note+"4"]
            else: raise ValueError("Note not valid:", note)
            super().addNote(track, self.channel, pitch, 
                            self.time[track], duration, self.volume)
        self.time[track] += duration
        self.need_to_write = True
        
    def addRest(self, duration=1, track=0):
        """
        Add a rest to the track, just corresponds to adjusting the time.
        duration: float, number of beats the rest lasts.
        track: int, which track to add the rest to.
        """
        self.time[track] += duration
        self.need_to_write = True
        
    def addText(self, text, track=0):
        """
        Add text to a track at the current time. For it to be visible, there
        must be a note at the current time on this track.
        text: str, text to add.
        track: int, which track to add the text to.
        """
        super().addText(track, self.time[track], str(text))
        self.need_to_write = True
        
    def writeFile(self, path=""):
        """ 
        Write the current midi track to a file 
        path: str, path to write the file to. Must end with a "/"!
        """
        if not self.need_to_write: return
        try:
            with open(path+self.filename, "wb") as f: super().writeFile(f)
        except FileNotFoundError:
            os.mkdir(path)
            with open(path+self.filename, "wb") as f: super().writeFile(f)
        self.need_to_write = False
            
    def play(self):
        """
        Write the midi file, then call on the system's default midi player. On
        Windows, this is probably Windows Media Player. THIS ONLY WORKS ON 
        WINDOWS, IF YOU WANT TO USE IT YOU MUST CHANGE THE SYSTEM CALL.
        """
        self.writeFile()
        os.system("start %s" % self.filename)
        
    def __str__(self):
        """ Return the string name of the song """
        return self.filename
        
if __name__ == "__main__":
    s = Song(name="helloworld", tempo=110, path="")
    s.addNote("c")
    s.addNote("d")
    s.addNote(("c", "d", "e"))
    s.view()
