"""
Mapping function take in arguments to define the mapping. They return another
function of the form mapping(res, name, tempo) that returns a Song object.
"""

from qSonify.maps.fermionic import *
from qSonify.maps.scale import *
from qSonify.maps.grandpiano import *
from qSonify.maps.stringquartet import *
from qSonify.maps.frequencymapping import *

default_map = fermionic()