import qiskit, time
from numpy import pi
# define pi so that in string gates we can have pi as an angle.
# For example, gate = "rz(pi/2, 1)"

name = "IBM"

simulators = simulator, unitary_simulator, state_simulator = (
    "qasm_simulator", "unitary_simulator", 
    "statevector_simulator"
)

quantum_computer = "ibmqx4"


def apply_credentials():
    print("\nApplying credentials...\n")
#    with open("qSonify/qc/APItoken.txt") as f: APItoken = f.read().strip()
    
    try:
#        qiskit.IBMQ.enable_account(APItoken)
        qiskit.IBMQ.load_accounts()
    
        print('Available backends:')
        print(qiskit.IBMQ.backends())
        print(qiskit.Aer.backends())
        print("\nCredientials applied\n")
    except:
        print('Something went wrong.\nDid you enter a correct token?')


#### String algorithm methods ####

# With this, we can write an algorithm as a list with any of the keys in
# GATE_ARGUMENTS. So, for example,
#   alg = ["H(0)", "RX(pi/2, 1)", "CX(1, 2)", "u3(pi/2, pi/4, .2, 0)"]
# then apply it to a qiskit.QuantumCircuit and qiskit.QuantumRegister qc and r
# respectively by calling 
#   apply_string_algorithm(alg, r, qc).

p = lambda x: ("reg[%d]",)*x
a = lambda x: ("%g",)*x
b = lambda x, y: "(" + ", ".join(a(x)+p(y)) + ")"


GATE_PARAMS = { ## The first number is the number of parameters,
                ## The second number is the number of qubit arguments.
    "ccx": (0, 3), "ch": (0, 2), "crz": (1, 2), "cswap": (0, 3), "cu1": (1, 2),
    "cu3": (3, 2), "cx": (0, 2), "cx_base": (0, 2), "cy": (0, 2), "cz": (0, 2),
    "h": (0, 1), "iden": (0, 1), "rx": (1, 1), "ry": (1, 1), "rz": (1, 1),
    "rzz": (1, 2), "s": (0, 1), "sdg": (0, 1), "swap": (0, 2), "t": (0, 1), 
    "tdg": (0, 1), "u0": (1, 1), "u1": (1, 1), "u2": (2, 1), "u3": (3, 1),
    "u_base": (3, 1), "x": (0, 1), "y": (0, 1), "z": (0, 1),
}

GATE_ARGUMENTS = {gate: b(*args) for gate, args in GATE_PARAMS.items()}
GATE_ARGUMENTS["measure"] = "(reg[%d], c_reg[%d])"


def get_num_qubits(algorithm):
    """
    Determine the max qubit value used in the algorithm.
    
    algorithm: iterable, each element must be a string gate, as in 
                     apply_string_gate above.
                     ie, algorithm = ["h(0)", "cx(0, 1)", "rx(pi/4, 1)",..]
                     
    returns: int, max qubit value in algorithm.
    """
    n = -1
    for gate in algorithm:
        gate = gate.strip().lower().replace("cnot", "cx")
        i = gate.index("(")
        gate_name, gate_args = gate[:i], eval(gate[i:])
        if gate_name == "measure": m = gate_args[0]
        elif sum(GATE_PARAMS[gate_name]) == 1: m = gate_args
        else: m = max(gate_args[GATE_PARAMS[gate_name][0]:])
        n = max(n, m)
    return n + 1
    


def apply_string_gate(gate, reg, cir, c_reg=None):
    """
    gate: str, one of the elements in GATE_ARGUMENTS.keys() + a tuple of 
               arguments. ie, for a rx rotation by pi/2 radians on qubit 0, 
               gate = "rx(pi/2, 0)".
    reg: qiskit.QuantumRegister, register to apply gate to.
    cir: qiskit.QuantumCircuit, circuit to add gate to.
    c_reg: qiskit.ClassicalRegister, must be supplied if gate is a measurement.
                                     Classical register to measure to.
    
    returns: int, if gate is a measure gate, then return the integer
                  corresponding to the classical register to measure to,
                  otherwise returns -1.
    """
    gate = gate.strip().lower().replace("cnot", "cx")
    i = gate.index("(")
    gate_name, gate_args = gate[:i], eval(gate[i:])
    
    # apply gate
    eval("cir." + gate_name + GATE_ARGUMENTS[gate_name] % gate_args)
    
    # value of the classical register to measure to
    if "measure" in gate: return gate_args[-1]
    else: return -1
    
    
def apply_string_algorithm(algorithm, reg, cir, c_reg=None):
    """
    algorithm: iterable, each element must be a string gate, as in 
                         apply_string_gate above.
                         ie, algorithm = ["h(0)", "cx(0, 1)", "rx(pi/4, 1)",..]
    reg: qiskit.QuantumRegister, register to apply algorithm to.
    cir: qiskit.QuantumCircuit, circuit to add gates in algorithm to.
    c_reg: qiskit.ClassicalRegister, must be supplied if gate is a measurement.
                                     Classical register to measure to.
    
    returns: int, if the algorithm has any measure gates, then returns the
                  integer corresponding to the largest index of the classical
                  register that is measured to, otherwise returns -1.
    """
    if not algorithm: return -1
    return max(apply_string_gate(gate, reg, cir, c_reg) for gate in algorithm)


def _make_job(qc, backend, num_samples):
    """
    Begin the execution of the circuit qc on the backend with shots=num_samples
    
    qc: qiskit.QuantumCircuit or list of circuits, circuits to run.
    backend: str, IBM backend to run circuit on. Can be 'ibmqx4', 'ibmqx5',
                  'local_qasm_simulator', 'local_unitary_simulator', etc.
    num_samples: int, number of samples to take from the quantum computer in
                      in order to determine the probabilities for each state.
                      
    returns: qiskit Job object from qiskit.backends.
    """
    if backend in simulators: f = qiskit.Aer
    else: f = qiskit.IBMQ
    try:
        return qiskit.execute(qc, backend=f.get_backend(backend), 
                                  shots=num_samples, max_credits=3)
    except LookupError:
        apply_credentials()
        return qiskit.execute(qc, backend=f.get_backend(backend),
                                  shots=num_samples, max_credits=3)
        
        
class Result(dict):
    """ Just a dictionary that automatically gives default values = 0.0 """
    def __getitem__(self, key):
        """ Return 0.0 if key not in result dictionary """
        return self.get(key, 0.0)
        
    
def run(algorithm, num_qubits=None, 
        num_samples=8000, backend=simulator):
    """
    Create a quantum circuit, run the algorithm, return the resulting
    probability distribution.
    
    algorithm: algorithm (list of strings) or list of algorithms, 
               each string is a gate in GATE_ARGUMENTS.keys() with whatever 
               arguments required to define the gate.
    num_qubits: int, number of qubits to run each algorithm on.
    num_samples: int, number of samples to take from the quantum computer in
                      in order to determine the probabilities for each state.
    backend: str, IBM backend to run the algorithm on. If backend is not
                  a local simulator then credentials must have already
                  been applied.
                  
    returns: dict, keys are states, values are probabilities found to be in
                   that state.
    """
    multiple = bool(algorithm and isinstance(algorithm[0], list))
    if not multiple: algorithm = [algorithm]
    
    n = len(algorithm)
    if num_qubits is None: 
        num_qubits = max(get_num_qubits(a) for a in algorithm)
    q = qiskit.QuantumRegister(num_qubits)
    c = [qiskit.ClassicalRegister(num_qubits) for _ in range(n)]
    qc = [qiskit.QuantumCircuit(q, c[j]) for j in range(n)]
    for j in range(n):
        i = apply_string_algorithm(algorithm[j], q, qc[j], c[j])
        if i == -1: qc[j].measure(q, c[j])
        else: c[j].size = i + 1
        
    job_exp = _make_job(qc, backend, num_samples)
    
    # Often there are random queue errors that have happened to 
    # me that cause the job to never complete. Two things I have
    # encountered: I lose connection or something, and I get an
    # error, or for some reason their server tells me that the
    # job is running indefinitely, ie it just get stuck running.
    # So if either of those things happen, we reset and
    # reinitialize our job(s) into the queue.
    if backend not in simulators:
        lapse, interval = 0, 30
        done = False
        while not done:
            str_status = str(job_exp.status())
            queue_position = job_exp.queue_position()
            error = job_exp.error_message()
            print('\nStatus @ %d seconds' % (interval * lapse))
            print("queue position =", queue_position)
            print(str_status)
            done = queue_position is not None and queue_position < 1
            
            if error:
                print("\nEncountered an error")
                print(error)
                print("reentering job into queue\n")
                job_exp.cancel()
                job_exp = _make_job(qc, backend, num_samples)
                lapse = 0
                
            lapse += 1
            time.sleep(interval)
            
    res = job_exp.result()
    
    if multiple:
        return [
            Result({k: v/num_samples for k, v in res.get_counts(cir).items()})
            for cir in qc
        ]
    else:
        return Result(
            {k: v/num_samples for k, v in res.get_counts(qc[0]).items()}
        )
        
        
def algorithm_unitary(algorithm, num_qubits=None):
    """
    Find the unitary corresponding to the algorithm.
    
    algorithm: list of strings, each string is a gate in GATE_ARGUMENTS.keys()
                                with whatever arguments required to define the 
                                gate.
    num_qubits: int, number of qubits to run the algorithm on.
                  
    returns: np.array, unitary matrix corresponding to the algorithm.
    """
    if num_qubits is None: num_qubits = get_num_qubits(algorithm)
    if not algorithm: algorithm = ["iden(0)"]
    q = qiskit.QuantumRegister(num_qubits)
    qc = qiskit.QuantumCircuit(q)
    apply_string_algorithm(algorithm, q, qc)
    return qiskit.execute(
        qc, backend=qiskit.Aer.get_backend(unitary_simulator)
    ).result().get_data(qc)["unitary"]
    
    
def prepare_state(state):
    """
    state: string, string of 0's and 1's.
    returns: algorithm (list of strings), algorithm to prepare the state.
    """
    return ["x(%d)" % i for i in range(len(state)) if state[i] == "1"]
        
        
def sample(algorithm, num_qubits=None, 
           num_samples=1, backend=simulator):
    """
    Get a list of all the outputs from an algorithm. Differs from `run` because
    `run` returns the determined probabilities of each state, but `sample`
    returns a list of the outputs.
    
    algorithm: algorithm (list of strings), NOT a list of algorithms, 
               each string is a gate in GATE_ARGUMENTS.keys() with whatever 
               arguments required to define the gate.
    num_qubits: int, number of qubits to run each algorithm on.
    num_samples: int, number of samples to take from the quantum computer.
    backend: str, IBM backend to run the algorithm on. If backend is not
                  a local simulator then credentials must have already
                  been applied.
                  
    returns: list, each element is the measured state.
    """
    d = run([algorithm]*num_samples, 
            num_qubits=num_qubits, 
            num_samples=1, backend=backend)
    return [list(x.keys())[0] for x in d]


def single_sample(algorithm, num_qubits=None, backend=simulator):
    """ 
    Same as `sample` with one sample, but returns a state instead of a list of 
    one state.
    """
    return sample(algorithm, num_qubits, 1, backend)[0]


def markovian_sample(algorithm, num_qubits=None, 
                     num_samples=1, backend=simulator):
    """
    Get a list of all the outputs from an algorithm, where the previous output
    is prepared as the starting point for the next algorithm; ie the
    measurement of the algorithm is input to run the algorithm again.
    
    algorithm: algorithm (list of strings), NOT a list of algorithms, 
               each string is a gate in GATE_ARGUMENTS.keys() with whatever 
               arguments required to define the gate.
    num_qubits: int, number of qubits to run each algorithm on.
    num_samples: int, number of samples to take from the quantum computer.
    backend: str, IBM backend to run the algorithm on. If backend is not
                  a local simulator then credentials must have already
                  been applied.
                  
    returns: list, each element is the measured state.
    """
    if num_samples < 1: raise ValueError("Must have >= 1 sample")
    if num_qubits is None: num_qubits = get_num_qubits(algorithm)
    args = num_qubits, backend
    res = [single_sample(algorithm, *args)]
    for _ in range(num_samples-1):
        res.append(single_sample(prepare_state(res[-1])+algorithm, *args))
    return res



if __name__ == "__main__":
    ## Examples
    
    # `run` returns a dictionary mapping states to probabilities, ie
    # run(["h(0)", "cx(0, 1)"]) should return {"00":0.5, "11": 0.5}.
    
    # if no "measure" is included in alg, then by default everything will
    # be measured.
    alg = ["H(0)", "CX(0, 1)", "u3(pi, pi/2, pi/4, 0)"]
    print(run(alg, 3, num_samples=10000))
    
    # since a measure is included, only that register will be measured.
    alg = ["H(0)", "CX(0, 1)", "u3(pi, pi/2, pi/4, 0)", "measure(0, 0)"]
#    print(run(alg, 3, num_samples=1000, backend="ibmqx4"))
    
    # run multiple circuits at once
    alg0 = ["h(0)", "cx(0, 1)", "measure(0, 0)", "measure(1, 1)"]
    alg1 = ["x(0)", "H(1)", "ccx(0, 1, 2)"]
    print(run([alg0, alg1]))
    
    # convert alg to its unitary respresentation.
    alg = ["h(0)", "cx(0, 1)"]
    print(algorithm_unitary(alg, 2))