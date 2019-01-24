from qSonify import maps
from qSonify.qc.register import Register
from qSonify.qc.gates import string_to_gate
from qSonify.qc.algorithms import prepare_basis_state


def alg_to_song(algorithm, num_qubits=None, 
                num_samples=40, mapping=maps.default_map, 
                name="alg", tempo=100):
    """
    Make a song from an algorithm. Markovian sample the algorithm, then map
    to a Song object.
    
    algorithm: list of Gate objects and/or string gates. Example:
                  ["cx(0, 1)", 
                   "x(0)", 
                   qSonify.Gate(unitary=[[...], ...], qubits=(1, 2))
                  ]
    num_qubits: int, number of qubits to run each algorithm on. If num_qubits
                     is None, then it will run on the minimum required.
    num_samples: int, number of samples to take from the quantum computer,
                      for most mappings this is equal to the number of beats.
    mapping: function, which mapping from output to sound to use. Can either 
                       use the ones already defined (ie maps.[map name](args)), 
                       or create your own mapping function. mapping must take
                       a list of outputs from the qc, a name of the song, and
                       a tempo of the song, and return a Song object.
    name: str, name of song.
    tempo: int, tempo of song.
                  
    returns: qSonify.Song object
    """
    algorithm = algorithm.copy()
    for i, g in enumerate(algorithm):
        if isinstance(g, str): algorithm[i] = string_to_gate(g)
    
    r = Register(num_qubits)
    r.apply_algorithm(algorithm)
    s = r.single_sample()
    
    num_qubits = len(s) # in case num_qubits was None
    
    registers = {"0"*num_qubits: r}
    res = [s] + [""] * (num_samples - 1)
    
    for i in range(1, num_samples):
        start = res[i-1]
        if start not in registers: 
            r = Register(num_qubits)
            r.apply_str_algorithm(prepare_basis_state(start))
            r.apply_algorithm(algorithm)
            registers[start] = r
        res[i] = registers[start].single_sample()
            
    return mapping(res, name=name, tempo=tempo)
        
    