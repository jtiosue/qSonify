from qSonify import Song, freq_to_note

def frequencymapping(low_freq=300, base=2):
    """ map output of algorithm to two tracks """
    def f(res, name, tempo):
        """ 
        res: list, list of output states of the qc. 
        name: str, name of song.
        tempo: int, tempo of song.
        return: Song object.
        """
        s = Song(name=name, tempo=tempo)
        for x in res:
            note = freq_to_note(int(x, base=base) + low_freq)
            s.addNote(note, duration=.5)
        return s
    return f