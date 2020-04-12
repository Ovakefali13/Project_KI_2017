from CPTCalculator import CPTCalculator
from pomegranate import *

# Documentation chapter 4
# # Implemenation of Bayesian Network
class BayesNetwork:
    cpt_calc = None
    sex_cpt = None
    sex_node = None
    age_cpt = None
    age_node = None
    fam_status_cpt = None
    fam_status_node = None
    children_cpt = None
    children_node = None
    education_cpt = None
    education_node = None
    job_cpt = None
    job_node = None
    salary_cpt = None
    salary_node = None
    prop_owner_cpt = None
    prop_owner_node = None
    tariff_cpt = None
    tariff_node = None

    model = None
    
    def __init__(self, cpt_calc):
        self.cpt_calc = cpt_calc
        # Defining probability distributions
        self.sex_cpt = DiscreteDistribution({'Geschlecht=="maennlich"': 0.502, 'Geschlecht=="weiblich"': 0.498})
        self.age_cpt = DiscreteDistribution({"Alter < 20": 0.122, "Alter >=20 & Alter < 65": 0.764, "Alter>=65": 0.114})
        self.fam_status_cpt = ConditionalProbabilityTable(self.cpt_calc.fam_status.cpt, [self.age_cpt])
        self.children_cpt = ConditionalProbabilityTable(self.cpt_calc.children.cpt, [self.age_cpt])
        self.education_cpt = ConditionalProbabilityTable(self.cpt_calc.education.cpt, [self.age_cpt, self.sex_cpt])
        self.job_cpt = ConditionalProbabilityTable(self.cpt_calc.job.cpt, [self.age_cpt, self.sex_cpt, self.education_cpt])
        self.salary_cpt = ConditionalProbabilityTable(self.cpt_calc.salary.cpt, [self.age_cpt, self.education_cpt, self.job_cpt])
        self.prop_owner_cpt = ConditionalProbabilityTable(self.cpt_calc.prop_owner.cpt, [self.age_cpt, self.sex_cpt, self.children_cpt, self.salary_cpt])
        self.tariff_cpt = ConditionalProbabilityTable(self.cpt_calc.tariff.cpt, [self.age_cpt, self.fam_status_cpt, self.job_cpt, self.salary_cpt, self.prop_owner_cpt])

        # Defining nodes
        self.sex_node = Node(self.sex_cpt, name="Geschlecht")
        self.age_node = Node(self.age_cpt, name="Alter")
        self.fam_status_node = Node(self.fam_status_cpt, name="Familienstand")
        self.children_node = Node(self.children_cpt, name="Kinder")
        self.education_node = Node(self.education_cpt, name="Bildungsstand")
        self.job_node = Node(self.job_cpt, name="Beruf")
        self.salary_node = Node(self.salary_cpt, name="Gehalt")
        self.prop_owner_node = Node(self.prop_owner_cpt, name="Immobilienbesitz")
        self.tariff_node = Node(self.tariff_cpt, name="Versicherungstarif")

        # Init model
        self.model = BayesianNetwork("Versicherungstariff_nodeetz")

        # Add states
        self.model.add_states(self.sex_node, self.fam_status_node, self.age_node, self.children_node, 
            self.education_node, self.job_node, self.salary_node, self.prop_owner_node, self.tariff_node)

    def add_edges(self):
        # Add edges
        # familienstand und kinder
        self.model.add_edge(self.age_node, self.fam_status_node) 
        self.model.add_edge(self.age_node, self.children_node) 

        # Bildungsstand
        self.model.add_edge(self.age_node, self.education_node)
        self.model.add_edge(self.sex_node, self.education_node)

        # Beruf
        self.model.add_edge(self.age_node, self.job_node)
        self.model.add_edge(self.sex_node, self.job_node)
        self.model.add_edge(self.education_node, self.job_node)

        # Gehalt
        self.model.add_edge(self.age_node, self.salary_node)
        self.model.add_edge(self.education_node, self.salary_node)
        self.model.add_edge(self.job_node, self.salary_node)

        # Immobilie
        self.model.add_edge(self.age_node, self.prop_owner_node)
        self.model.add_edge(self.sex_node, self.prop_owner_node)
        self.model.add_edge(self.children_node, self.prop_owner_node)
        self.model.add_edge(self.salary_node, self.prop_owner_node)

        # Immobilie
        self.model.add_edge(self.age_node, self.tariff_node)
        self.model.add_edge(self.fam_status_node, self.tariff_node)
        self.model.add_edge(self.job_node, self.tariff_node)
        self.model.add_edge(self.salary_node, self.tariff_node)
        self.model.add_edge(self.prop_owner_node, self.tariff_node)

        self.model.bake()

    def run_example(self):
        # Beispiele
        print("Those are the examples of the Bayes Network")
        print("________________________________________________________________________________________________________________")
        print(self.model.predict([['Geschlecht=="maennlich"', None, 'Alter < 20', None, None, None, None, None, None]]))
        print("________________________________________________________________________________________________________________")
        print(self.model.predict_proba([['Geschlecht=="maennlich"', 'Familienstand=="verheiratet"', 'Alter >=20 & Alter < 65', 'Kinder < 3', 
                        'Bildungsstand=="Master"', 'Beruf=="selbständig"', 'Jahresgehalt >= 100000', 
                        'Immobilienbesitz=="Einfamilienhaus"', None]]))
    