from qSonify import Song

def scale(notes=("c", "d", "e", "f", "g", "a", "b", "c5")):
    """
    Map each state to a note.
    return: function, mapping(res, name, tempo) that returns a Song object.
    """
    def f(res, name, tempo):
        """ 
        res: list, list of output states of the qc. 
        return: Song object.
        """
        s = Song(name=name, tempo=tempo)
        duration = 1
        for x in res:
            note = notes[int(x, base=2) % len(notes)]
            s.addNote(note, duration)
        return s
    return f