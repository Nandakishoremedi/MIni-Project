# Objective : To develop a basic version of RETE  based expert system module in Python
# this module identifies all major ideas of RETE i.e. Working mememory, alfa and beta and production nodes.
# all these are implemented as classes in Python.
#-------------------------------------------------------------------------------------------------------------------
# this module shows how a general RETE rule based expert system works.
# forward chaining is used
# it searches the facts in optimum ay every cycle.
# expert tules are matched in sequential order
#-------------------------------------------------------------------------------------------------------------------
# Team : III/II Sec.C
#1. M.Nandakishore  20B81A05E9
#2. A.Abhishek 20B81A05C2
#3.K.Manishanthan 20B81A05E7
#-------------------------------------------------------------------------------------------------------------------
class WorkingMemory:
    def __init__(self):
        self.facts = []

    def add_fact(self, fact):
        self.facts.append(fact)

    def remove_fact(self, fact):
        self.facts.remove(fact)

class AlphaMemory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

class BetaMemory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

class AlphaNode:
    def __init__(self, attribute, value, alpha_memory):
        self.attribute = attribute
        self.value = value
        self.children = []
        self.alpha_memory = alpha_memory

    def activate(self, fact):
        if fact[self.attribute] == self.value:
            self.alpha_memory.add_item(fact)
            for child in self.children:
                child.activate()

class BetaNode:
    def __init__(self, condition, left_memory, right_memory, beta_memory):
        self.condition = condition
        self.left_memory = left_memory
        self.right_memory = right_memory
        self.beta_memory = beta_memory
        self.children = []

    def activate(self):
        for fact1 in self.left_memory.items:
            for fact2 in self.right_memory.items:
                if self.condition(fact1, fact2):
                    self.beta_memory.add_item((fact1, fact2))
                    for child in self.children:
                        child.activate(fact1, fact2)

class ProductionNode:
    def __init__(self, action):
        self.action = action

    def activate(self, fact1, fact2):
        new_facts = self.action(fact1, fact2)
        return new_facts

def has_fever_and_cough(fact1, fact2):
    return fact1['symptom'] == 'fever' and fact2['symptom'] == 'cough'

def has_sore_throat_and_fatigue(fact1, fact2):
    return fact1['symptom'] == 'sore throat' and fact2['symptom'] == 'fatigue'

def add_flu(fact1, fact2):
    return {'symptom': 'flu'}

def add_visit_doctor(fact1, fact2):
    return {'symptom': 'visit_doctor'}

# Create RETE network
working_memory = WorkingMemory()
alpha_memory = AlphaMemory()
beta_memory = BetaMemory()

# Alpha nodes
fever_alpha_node = AlphaNode('symptom', 'fever', alpha_memory)
cough_alpha_node = AlphaNode('symptom', 'cough', alpha_memory)
sore_throat_alpha_node = AlphaNode('symptom', 'sore throat', alpha_memory)
fatigue_alpha_node = AlphaNode('symptom', 'fatigue', alpha_memory)
flu_alpha_node = AlphaNode('symptom', 'flu', alpha_memory)

# Beta nodes
flu_beta_node = BetaNode(has_fever_and_cough, alpha_memory, alpha_memory, beta_memory)
flu_beta_node2 = BetaNode(has_sore_throat_and_fatigue, alpha_memory, alpha_memory, beta_memory)
visit_doctor_beta_node = BetaNode(lambda f1, f2: f1['symptom'] == 'flu' or f2['symptom'] == 'flu', alpha_memory, alpha_memory, beta_memory)

# Production nodes
flu_production_node = ProductionNode(add_flu)
visit_doctor_production_node = ProductionNode(add_visit_doctor)

# Connect the network
fever_alpha_node.children.append(flu_beta_node)
cough_alpha_node.children.append(flu_beta_node)
sore_throat_alpha_node.children.append(flu_beta_node2)
fatigue_alpha_node.children.append(flu_beta_node2)
flu_alpha_node.children.append(visit_doctor_beta_node)

flu_beta_node.children.append(flu_production_node)
flu_beta_node2.children.append(flu_production_node)
visit_doctor_beta_node.children.append(visit_doctor_production_node)

# Facts
facts = [
   
    {'symptom': 'headache'},
    {'symptom': 'fever'},
    {'symptom': 'cough'},
    {'symptom': 'sore throat'},
    {'symptom': 'fatigue'}
]

inferred_facts = set()

# Add facts to the working memory 
for fact in facts:
    working_memory.add_fact(fact)

# Add facts to the network
for fact in working_memory.facts:
    fever_alpha_node.activate(fact)
    cough_alpha_node.activate(fact)
    sore_throat_alpha_node.activate(fact)
    fatigue_alpha_node.activate(fact)
    flu_alpha_node.activate(fact)

    for beta_node in [flu_beta_node, flu_beta_node2, visit_doctor_beta_node]:
        beta_node.activate()

    for production_node in [flu_production_node, visit_doctor_production_node]:
        for fact_pair in beta_memory.items:
            new_fact = production_node.activate(fact_pair[0], fact_pair[1])
            if new_fact:
                inferred_facts.add(tuple(new_fact.items()))

# Print inferred facts
print("Inferred facts:")
for fact in inferred_facts:
    print(dict(fact))
