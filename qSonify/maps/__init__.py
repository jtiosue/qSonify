"""
Mapping function take in arguments to define the mapping. They return another
function of the form mapping(res, name, tempo) that returns a Song object.
"""

from qSonify.maps.fermionic import fermionic
from qSonify.maps.scale import scale
from qSonify.maps.grandpiano import grandpiano
from qSonify.maps.stringquartet import stringquartet
from qSonify.maps.frequencymapping import frequencymapping

default_map = fermionic()