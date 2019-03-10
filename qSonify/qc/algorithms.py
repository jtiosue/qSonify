import numpy as np

def prepare_basis_state(state):
    """
    Find the algorithm to create the basis state.
    
    state: str, ie "0010".
    return: list of strs, algorithm to create the state.
    """
    return ["X(%d)" % i for i in range(len(state)) if state[i] == "1"]


def QFT(*endpoints):
    """ end is non inclusive """
    if len(endpoints) == 0: raise ValueError("Must provide qubits for fourier transform")
    elif len(endpoints) == 1: start, end = 0, endpoints[0]
    elif len(endpoints) == 2: start, end = endpoints
    else: raise ValueError("Bad start, end qubits")
    
    alg = []
    for j in range(start, end):
        alg.append("H(%d)" % j)
        for k in range(1, end-j):
            alg.append("crz(%g, %d, %d)" % (np.pi/(1<<k), j+k, j))
    alg.extend(["swap(%d, %d)" % (start+i, end-i-1) for i in range((end-start) // 2)])
    
    return alg


def IQFT(*endpoints):
    """ end is non inclusive """
    if len(endpoints) == 0: raise ValueError("Must provide qubits for fourier transform")
    elif len(endpoints) == 1: start, end = 0, endpoints[0]
    elif len(endpoints) == 2: start, end = endpoints
    else: raise ValueError("Bad start, end qubits")
    
    alg = ["swap(%d, %d)" % (start+i, end-i-1) for i in range((end-start) // 2)]
    
    for j in range(end-1, start-1, -1):
        for k in range(end-j-1, 0, -1):
            alg.append("crz(%g, %d, %d)" % (-np.pi / (1 << k), j+k, j))
        alg.append("H(%d)" % j)
    
    return alg


def GHZ(num_qubits, d=2, qubit_start=0):
    """
    Make a GHZ state in base d for qubits [qubit_start, qubit_start+num_qubits]
    Returns a list of strings representing gates.
    
    So, for example, 
       GHZ_alg(6, 4, 1) 
    will return
       ["H(1)", "H(2)", "CNOT(1, 3)", CNOT("2, 4"), "CNOT(3, 5)", "CNOT(4, 6)"]
    
    On a register with >= 7 qubits, this will prepare 
        (1/sqrt(4))*(|000>+|111>+|222>+|333>)
    on qubits 1 through 6.
    
    In general, GHZ_alg(num_qubits, d, qubit_start) prepares the state
        (1/sqrt(d))*(|0...0>+|1...1>+...+|(d-1)...(d-1)>)
    on the qubits in the range [qubit_start, qubit_start+num_qubits].
    
    Thus, num_qubits must be an integer times log2(d).
    
    This algorithm only works for d is a power of 2.    
    """
    l = int(np.log2(d))
    assert l == np.log2(d), "d must be a power of 2"
    assert num_qubits / l == num_qubits // l, (
        "num qubits must be a integer times log2(d)"        
    )
    return (
        ["H(%d)" % i for i in range(qubit_start, qubit_start+l)] + 
        ["CX(%d, %d)" % (i, i+l)
         for i in range(qubit_start, qubit_start+num_qubits-l)]
    )
    

def hadamard_tensor(qubits):
    """
    Return the algorithm for H^{\otimes num_qubits}.
    
    qubits: tuple or list of ints, or an int;
                if it is an iterable, then it is the qubits to apply the 
                hadamards to.
                if it is an int, then we apply the hadamards to qubits 
                [0, qubits) non inclusive.
    
    returns: list, algorithm.
    """
    if isinstance(qubits, int): qubits = tuple(range(qubits))
    return ["h(%d)" % i for i in qubits]


#### General two body gate arxiv:1807.00800 ####
def U2(p, r0, r1):
    """
    General two body gate arxiv:1807.00800. Uses 15 parameters.
    
    p: list or tuple of 15 floats, angles for the rotation gates.
    r0: int, first register/qubit to apply the gate to.
    r1: int, second register/qubit to apply the gate to.
    
    returns: list, algorithm.
    """
    return [
        "rz(%g, %d)" % (p[0], r0),
        "ry(%g, %d)" % (p[1], r0),
        "rz(%g, %d)" % (p[2], r0),
        "rz(%g, %d)" % (p[3], r1),
        "ry(%g, %d)" % (p[4], r1),
        "rz(%g, %d)" % (p[5], r1),
        "cx(%d, %d)" % (r1, r0),
        "rz(%g, %d)" % (p[6], r0),
        "ry(%g, %d)" % (p[7], r1),
        "cx(%d, %d)" % (r0, r1),
        "ry(%g, %d)" % (p[8], r1),
        "cx(%d, %d)" % (r1, r0),
        "rz(%g, %d)" % (p[9], r0),
        "ry(%g, %d)" % (p[10], r0), 
        "rz(%g, %d)" % (p[11], r0),
        "rz(%g, %d)" % (p[12], r1), 
        "ry(%g, %d)" % (p[13], r1), 
        "rz(%g, %d)" % (p[14], r1),
    ]


def U2dag(p, r0, r1):
    """ The inverse of U2 (see the documentation for U2) """
    return list(reversed(U2(tuple(-x for x in p), r0, r1)))