from qSonify.qc import *
from qSonify import maps
from qSonify.sonify import *
from qSonify.qSonify import alg_to_song
from ._version import __version__

state_to_decimal = lambda s: int(s, base=2)
decimal_to_state = lambda x, num_qubits: ("{0:0%db}" % num_qubits).format(x)
