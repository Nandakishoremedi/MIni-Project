# Objective : To develop a basiv vesrion of rule  based expert system module in Python
# this module is a precursor to RETE which is main goal of mini project
#-------------------------------------------------------------------------------------------------------------------
# this module shows how a general rule based expert system works.
# forward chaining is used
# It uses brute force technique
# it searches the facts repeatedly every cycle.
# expert tules are matched in sequential order
# this is developed to demonstrate basic version of rule based expert system
#-------------------------------------------------------------------------------------------------------------------
# Team : III/II Sec. C
#1. M.Nandakishore  20B81A05E9
#2. A.Abhishek 20B81A05C2
#3.K.Manishanthan 20B81A05E7
#-------------------------------------------------------------------------------------------------------------------

class Rule:
    def __init__(self, condition, action, name):
        self.condition = condition
        self.action = action
        self.name = name

    def is_applicable(self, facts):
        return self.condition(facts)
    
class ForwardChainingEngine:
    def __init__(self):
        self.rules = []
        self.facts = set()
        self.rule_counter = 1  # Add a counter for rule names

    def add_rule(self, condition, action):
        rule_name = f"R{self.rule_counter}"
        self.rules.append(Rule(condition, action, rule_name))
        self.rule_counter += 1

    def add_fact(self, fact):
        self.facts.add(fact)

    def infer(self):
        rule_chain = []
        while True:
            applied_rules = False
            for rule in self.rules:
                if rule.is_applicable(self.facts):
                    new_facts = rule.action()
                    self.facts.update(new_facts)
                    
                    rule_chain.append(rule.name)  # Add the applied rule's name to the chain
                    print(f"Applied rule: {rule.name} ({rule.condition.__name__}), new facts: {new_facts}")
                    print(f"Current rule chain: {' -> '.join(rule_chain)}")  # Display chaining graphically
                    
                    applied_rules = True
                    # Remove the applied rule to prevent infinite loops
                    self.rules.remove(rule)
                    break

            if not applied_rules:
                break
# Sample rules and facts
def has_flu(facts):
    return 'flu' in facts

def has_fever_and_cough(facts):
    return 'fever' in facts and 'cough' in facts

def has_sore_throat_and_fatigue(facts):
    return 'sore throat' in facts and 'fatigue' in facts

engine = ForwardChainingEngine()

# Add rules
engine.add_rule(has_fever_and_cough, lambda: {'flu'})
engine.add_rule(has_sore_throat_and_fatigue, lambda: {'flu'})
engine.add_rule(has_flu, lambda: {'visit_doctor'})

# Add facts
engine.add_fact('fever')
engine.add_fact('cough')
engine.add_fact('sore throat')

# Perform inference
engine.infer()

# Print inferred facts
print(engine.facts)
