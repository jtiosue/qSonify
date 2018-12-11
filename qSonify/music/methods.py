from math import log2, pow

_A4 = 440
_C0 = _A4*pow(2, -4.75)
_notes = "c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"
    
def freq_to_note(freq):
    h = round(12*log2(freq/_C0))
    octave, n = h // 12, h % 12
    return _notes[n] + str(octave)