from qSonify import Song

def fermionic(notes=("c", "d", "e", "f", "g")):
    """
    Map each qubit to a note, each sample is a beat.
    return: function, mapping(res, name, tempo) that returns a Song object.
    """
    def f(res, name, tempo):
        """ 
        res: list, list of output states of the qc. 
        name: str, name of song.
        tempo: int, tempo of song.
        return: Song object.
        """
        s = Song(name=name, tempo=tempo)
        duration = 1
        for x in res:
            chord = tuple(
                notes[i % len(notes)] 
                for i in filter(lambda y: x[y] == '1', range(len(x)))
            )
            s.addNote(chord, duration)
        return s
    return f