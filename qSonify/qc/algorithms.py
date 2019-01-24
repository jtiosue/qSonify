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