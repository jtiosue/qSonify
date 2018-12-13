import qSonify.maps as maps
import qSonify.qc as qc

def alg_to_song(algorithm, num_qubits=None, 
                num_samples=40, backend=qc.simulator, 
                markovian=True, mapping=maps.default_map, 
                name="alg", tempo=100):
    """
    Make a song from an algorithm.
    
    algorithm: algorithm (list of strings), NOT a list of algorithms, 
               each string is a gate in GATE_ARGUMENTS.keys() with whatever 
               arguments required to define the gate.
    num_qubits: int, number of qubits to run each algorithm on.
    num_samples: int, number of samples to take from the quantum computer,
                      for most mappings this is equal to the number of beats.
    backend: str, IBM backend to run the algorithm on. If backend is not
                  a local simulator then credentials must have already
                  been applied.
    markovian: bool, whether to sample using qc.sample or qc.markovian_sample.
    mapping: function, which mapping from output to sound to use. Can either 
                       use the ones already defined (ie maps.[map name](args)), 
                       or create your own mapping function. mapping must take
                       a list of outputs from the qc, a name of the song, and
                       a tempo of the song, and return a Song object.
    name: str, name of song.
    tempo: int, tempo of song.
                  
    returns: Song object
    """
    sample_f = qc.markovian_sample if markovian else qc.sample
    res = sample_f(algorithm, num_qubits=num_qubits, 
                   num_samples=num_samples, backend=backend)
    return mapping(res, name=name, tempo=tempo)
