import numpy as np
from g2p_en import G2p
from hmmlearn import hmm

class State:
    def __init__(self, type, name, value, emm, emm_prob):
        self.type = type            # start/end/graph/phone/syllabic
        self.name = name            # S/E/Gi/Pj/Sx
        self.value = value          # $/T/O/D/A/Y/AH/EY/2
        self.trans = []             # [next] (list of states)
        self.trans_prob = []        # [1]
        self.emm = emm              # [value, '!', '@']/[value]
        self.emm_prob = emm_prob    # [0.7, 0.2, 0.1]

    def set_trans(self, nexts, nexts_prob):
        self.trans += nexts
        self.trans_prob += nexts_prob


class HMM:
    def __init__(self, graphs, phones, syllables):
        self.start = State('start', 'S', '$', ['$'], [1])
        self.end = State('end', 'E', '$', ['$'], [0])
        
        current = self.start
        p = 0
        for i, graph in enumerate(graphs):
            phone = phones[p]
            if phone[0] is graph:
                p += 1
            else:
                prob = [1/len(phone[1]) for _ in range(len(phone[1]))]
                ps = State('phone', 'P'+str(p+1), phone[0], phone[1], prob)
                current.set_trans([ps], [1])
            
                if p+1 < len(phones) and i+1 < len(graphs):
                    next_phone = phones[p+1][0]
                    next_graph = graphs[i+1]
                    if next_phone is next_graph:
                        p += 1

            g = State('graph', 'G'+str(i+1), graph, [graph, '!', '@'], [0.7, 0.2, 0.1])
            current.set_trans([g], [1])
            current = g
        current.set_trans([self.end], [1])

# TODO Manual mapping (currently hardcoded)
def emissions(phone):
    if('ay' in phone):
        return ['y', 'e', 'i']
    if('ah' in phone):
        return ['a', 'o', 'u']
    return [phone[0]]

def get_states(word):

    graphs = list(word)
    phones = G2p()(word)

    for i, phone in enumerate(phones):
        phone = phone.lower()
        phones[i] = [phone, emissions(phone)]
    
    # TODO Find syllabic states from phones
    syllables = []
    
    return graphs, phones, syllables


def create_hmm(word):

    n = len(word)
    G, P, S = get_states(word)

    model = HMM(G, P, S)

    # model = hmm.MultinomialHMM(n_components=n)
    # model.startprob_ = start_prob
    # model.transmat_ = trans_mat
    # model.emissionprob_ = emm_mat

    return model



word = 'today'
model = create_hmm(word)
print(model.start.trans[0])