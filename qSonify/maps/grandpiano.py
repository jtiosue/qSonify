from qSonify.sonify import Song

def grandpiano(low_notes=("c3", "d3", "e3"), high_notes=("c", "d", "e")):
    """ map output of algorithm to two tracks """
    def f(res, name, tempo):
        """ 
        res: list, list of output states of the qc. 
        name: str, name of song.
        tempo: int, tempo of song.
        return: Song object.
        """
        s = Song(name=name, tempo=tempo, num_tracks=2)
        if not res: return s
        duration, l = 1/2, len(res[0]) // 2
        note0 = lambda x: low_notes[int(x[:l], base=2) % len(low_notes)]
        note1 = lambda x: high_notes[int(x[l:], base=2) % len(high_notes)]
        for x in res:
            s.addNote(note0(x), duration, 1)
            s.addNote(note1(x), duration, 0)
        return s
    return f