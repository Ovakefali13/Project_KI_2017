import itertools
import pandas as pd

class Vertex:
    def __init__(self, data, name, s):
        self.data = data
        self.name = name
        self.parents = []
        self.states = s
        self.cpt = None
    
    def P(self, query):
        total = len(self.data)
        x = self.data.query(query)
        return len(x)/total

    # Adds a new parent to the node
    def register_parent(self, vertex):
        self.parents.append(vertex)
        
    # Updates the CPT
    def update_cpt(self):
        
        states = []
        # Check if node has parents
        if len(self.parents) > 0:
            
            for p in self.parents:
                states.append(p.states)
                
            states.append(self.states)
            
            permutations_tuples = list(itertools.product(*states))
            self.cpt = []
            
            for p in permutations_tuples:
                self.cpt.append(list(p))
                            
            for row in self.cpt:
                given = " & ".join(row[:-1])
                
                if self.P(given) == 0:
                    row.append(0)
                else:
                    prob = self.P(" & ".join(row))/self.P(given)
                    row.append(prob)
                            
        # If node has no parents, just calculate the 'normal' probability P(s)
        else:
            states = [[s] for s in self.states]
            for s in states:
                s.append(self.P(s[0]))
            self.cpt = states
            
    def get_cpt(self):
        columns = [p.name for p in self.parents]
        columns.append(self.name)
        columns.append('Prob')
        return pd.DataFrame(self.cpt, columns = columns)