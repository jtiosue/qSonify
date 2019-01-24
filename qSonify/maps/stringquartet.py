from qSonify.sonify import Song

def stringquartet():
    """ map output of algorithm to bass, tenor, treble, and treble clef """
    def f(res, name, tempo):
        """ 
        res: list, list of output states of the qc. 
        name: str, name of song.
        tempo: int, tempo of song.
        return: Song object.
        """
        _n = ('c', 'd', 'e', 'f', 'g', 'a', 'b')
        vl1 = _n + tuple(x+'5' for x in _n) + ('c6',)
        vl2 = vl1
        vo = tuple(x+'3' for x in _n) + _n
        cel = tuple(x+'2' for x in _n) + tuple(x+'3' for x in _n) + ('c',)
        
        s = Song(name=name, tempo=tempo, num_tracks=4)
        if not res: return s
        duration, l = 1, len(res[0]) // 4
        for x in res:
            s.addNote(cel[int(x[:l], base=2) % len(cel)], duration, 3)
            s.addNote(vo[int(x[l:2*l], base=2) % len(cel)], duration, 2)
            s.addNote(vl2[int(x[2*l:3*l], base=2) % len(cel)], duration, 1)
            s.addNote(vl1[int(x[3*l:], base=2) % len(cel)], duration, 0)
        return s
    return f