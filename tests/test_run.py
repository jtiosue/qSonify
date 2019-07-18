import qSonify

def test_run():

    alg1 = ["h(0)", "cx(0, 1)", "cx(0, 2)", "cx(0, 3)", "cx(0, 4)"]
    alg2 = ['h(0)', 'rz(pi, 2)', 
            qSonify.Gate([[0.5, 0.75**0.5], [-0.75**0.5, 0.5]], (4,)), 'rx(pi/2, 2)', 'cx(0, 3)']
    notes = "c4", "d4", "e4", "f4", "g4", "a4", "b4", "c5"
    mapping = qSonify.maps.grandpiano(low_notes=("c3", "d3", "e3", "f3", "g3"), high_notes=notes)
    
    kwargs = dict(num_samples=40, mapping=mapping, tempo=150)

    s1 = qSonify.alg_to_song(alg1, name="HelloWorld_alg1", **kwargs)
    s2 = qSonify.alg_to_song(alg2, name="HelloWorld_alg2", **kwargs)
