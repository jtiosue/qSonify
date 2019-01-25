import numpy as np
from qSonify.qc.gates import str_to_gate


def all_states(num_qubits):
    """
    Generator, yields '00', '01', '10', '11'
    for two qubits, and similar for more
    """
    if num_qubits == 1: yield from ("0", "1")
    elif num_qubits > 1:
        for s in all_states(num_qubits-1):
            yield from (s+"0", s+"1")
            

def random_state(prob_dist):
    """
    Pick a state from the probability distribution.
    
    prob_dist: dict, maps states to probabilities.
                    ex: {"000": 0.5, "110": .25, "111": .25}
    
    return: str, state.
    """
    r = np.random.random()
    total = 0.0
    for state in prob_dist:
        total += prob_dist[state]
        if r <= total: return state
    raise Exception("Register's probability distribution is not normalized")
    

def get_sub_state(state, qubits=None):
    """
    Find the sub-state of the state given the qubits of the sub state.
    For example,
        get_sub_state("100101", (0, 2, 3))
    would return "101".
    
    state: str.
    qubits: tuple.
    
    returns: str, sub-state.
    """
    return "".join(state[i] for i in qubits)


class Register(dict):

    def __init__(self, num_qubits=None):
        """
        initialize register to |"0"*num_qubits>
        num_qubits: int. If num_qubits is None, then the register will grow
                         as needed WHEN APPLYING GATES.
        """
        super().__init__()
        if num_qubits is None: self.num_qubits, self.grow = 1, True
        else: self.num_qubits, self.grow = num_qubits, False
        self["0"*self.num_qubits] = 1.0+0.0j

    def __getitem__(self, item):
        """
        return the amplitude of the state. setitem still works
        by inheriting from dict class
        """
        return super().__getitem__(item) if item in self else 0.0+0.0j

    def amplitude(self, state):
        return self[state]

    def probability(self, state):
        return abs(self[state])**2
    
    def get_prob_dist(self, qubits=None):
        """
        Get the probability distribution for measuring the qubits.
        
        qubits: tuple, qubits for the distrubution. If qubits is None, then
                       will find the distribution over all the qubits.
        return: dict, states mapped to probabilities.
        """
        if qubits is None: 
            return {state: self.probability(state) for state in self}
        
        prob_dist = {}
        for state in self:
            s = get_sub_state(state, qubits)
            prob_dist[s] = prob_dist.get(s, 0) + self.probability(state)
            
        return prob_dist

    def apply_gate(self, gate):
        """ 
        apply Gate object to the register 
        
        gate: Gate object or str gate.
        return: None.
        """
        if isinstance(gate, str):
            self.apply_gate(str_to_gate(gate))
            return
        
        m = max(gate.qubits)
        if m >= self.num_qubits:
            if not self.grow:
                raise ValueError("Gate operates on non initialized qubit")
            else:
                # Grow the register so that it is big enough for the gate.
                n = m + 1 - self.num_qubits
                old = self.copy()
                self.clear()
                for state, amp in old.items(): self[state + "0"*n] = amp
                self.num_qubits = m + 1
        
        old = self.copy() 
        temp_states = [x for x in all_states(gate.num_qubits)]
        for state in old:
            s = ""
            for q in gate.qubits: s += state[q]
            r = int(s, base=2)
            self[state] -= (1.0 - gate[r][r]) * old[state]
            
            # zero beyond machine precision
            if self.probability(state) < 1e-16: self.pop(state)

            j = 0
            for k in temp_states:
                if j != r:
                    s = list(state)
                    for l in range(len(k)): s[gate.qubits[l]] = k[l]
                    s = "".join(s)
                    c = gate[j][r] * old[state]
                    if s in self:
                        self[s] += c
                        if self.probability(s) < 1e-16: self.pop(s)
                    elif c != 0.0: self[s] = c
                j += 1

    def measure(self, qubits=None):
        """
        Measure the system and collapse it into a state 
        
        qubits: tuple, qubits to measure. If qubits is None, then we measure
                       all.
        return: str, collapsed state.
        """
        prob_dist = self.get_prob_dist(qubits)
        state = random_state(prob_dist)
        if qubits is None:
            self.clear()
            self[state] = 1.0+0.0j
        else:
            old_register = self.copy()
            self.clear()
            p = prob_dist[state]**0.5
            for s, amp in old_register.items():
                if get_sub_state(s, qubits) == state: self[s] = amp / p
            
        return state
    
    def sample(self, num_samples=1, qubits=None):
        """
        Generator that yields samples from the register, measuring the qubits.
        
        num_samples: int, number of sampels to take.
        qubits: tuple, qubits to measure. If qubits is None, then use all.
        
        yields: strs, "001", "110", ...
        """
        prob_dist = self.get_prob_dist(qubits)
        for _ in range(num_samples): yield random_state(prob_dist)
        
    def single_sample(self, qubits=None):
        """
        Returns a single sample of the qubits without collapsing the register.
        
        qubits: tuple, qubits to measure. If qubits is None, then use all.
        
        return: str, state.
        """
        return [x for x in self.sample(1, qubits)][0]

    def duplicate(self):
        """ return a copy of the register """
        reg = Register(self.num_qubits)
        for (key, item) in self.items(): reg[key] = item
        return reg

    def ket(self):
        """
        Returns the ket vector of the state in the computational basis.
        Returns in the form of a numpy array.
        """
        ket = np.zeros((1 << self.num_qubits, 1))*0j
        for state in self: ket[int(state, base=2)][0] = self[state]
        return ket

    def bra(self):
        """
        Returns the bra vector of the state in the computational basis.
        Returns in the form of a numpy array.
        """
        return np.conjugate(np.transpose(self.ket()))

    def density_matrix(self):
        """
        Returns the density matrix representing the state of ther resgister.
        Returns in the form of a numpy array. Note that the Register class
        only supports pure states, so the density matrix will be that of a
        pure state
        """
        ket = self.ket()
        return ket @ np.conjugate(np.transpose(ket))
        
    def apply_algorithm(self, algorithm):
        """
        Apply the algorithm to the register
        
        algorithm: list of Gate objects and/or string gates. Example:
                      ["cx(0, 1)", 
                       "x(0)", 
                       qSonify.Gate(unitary=[[...], ...], qubits=(1, 2))
                      ]
        return: None
        """
        for gate in algorithm: self.apply_gate(gate)