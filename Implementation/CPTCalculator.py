from Vertex import Vertex

class CPTCalculator:
    data = None
    age = None
    sex = None
    fam_status = None
    children = None
    education = None
    job = None
    salary = None
    prop_owner = None
    tariff = None

    def __init__(self, data):
        self.data = data
        self.set_age()
        self.set_sex()
        self.set_fam_status()
        self.set_children()
        self.set_education()
        self.set_job()
        self.set_salary()
        self.set_prop_owner()
        self.set_tariff()

    def set_age(self):
        self.age = Vertex(self.data, 'Alter', ['Alter < 20', 'Alter >=20 & Alter < 65', 'Alter>=65'])
        self.age.update_cpt()
        self.age.get_cpt()

    def set_sex(self):
        self.sex = Vertex(self.data, 'Geschlecht', ['Geschlecht=="maennlich"', 'Geschlecht=="weiblich"'])
        self.sex.update_cpt()
        self.sex.get_cpt()
    
    def set_fam_status(self):
        self.fam_status = Vertex(self.data, 'Familienstand', ['Familienstand=="ledig"', 'Familienstand=="geschieden"',
                      'Familienstand=="verwitwet"', 'Familienstand=="verheiratet"'])
        self.fam_status.register_parent(self.age)
        self.fam_status.update_cpt()
        self.fam_status.get_cpt()        

    def set_children(self):
        self.children = Vertex(self.data, 'Kinder', ['Kinder < 3', 'Kinder >= 3'])
        self.children.register_parent(self.age)
        self.children.update_cpt()
        self.children.get_cpt()

    def set_education(self):
        states = [f'Bildungsstand=="{x}"' for x in self.data['Bildungsstand'].unique()]

        self.education = Vertex(self.data, 'Bildungsstand', states)
        self.education.register_parent(self.age)
        self.education.register_parent(self.sex)
        self.education.update_cpt()
        self.education.get_cpt()

        '''
         # ---> Stimmt

        #TODO
        '''

    def set_job(self):
        states = [f'Beruf=="{x}"' for x in self.data['Beruf'].unique()]

        self.job = Vertex(self.data, 'Beruf', states)
        self.job.register_parent(self.age)
        self.job.register_parent(self.sex)
        self.job.register_parent(self.education)
        self.job.update_cpt()
        self.job.get_cpt()

    def set_salary(self):
        states =  ['Jahresgehalt < 10000', 'Jahresgehalt >= 10000 & Jahresgehalt < 60000',
           'Jahresgehalt >= 60000 & Jahresgehalt < 80000',
           'Jahresgehalt >= 80000 & Jahresgehalt < 100000',
           'Jahresgehalt >= 100000']

        self.salary = Vertex(self.data, 'Jahresgehalt', states)
        self.salary.register_parent(self.age)
        self.salary.register_parent(self.education)
        self.salary.register_parent(self.job)
        self.salary.update_cpt()
        self.salary.get_cpt()
    
    def set_prop_owner(self):
        states = [f'Immobilienbesitz=="{x}"' for x in self.data['Immobilienbesitz'].unique()]

        self.prop_owner = Vertex(self.data, "Immobilienbesitz", states)
        self.prop_owner.register_parent(self.age)
        self.prop_owner.register_parent(self.sex)
        self.prop_owner.register_parent(self.children)
        self.prop_owner.register_parent(self.salary)
        self.prop_owner.update_cpt()
        self.prop_owner.get_cpt()
    
    def set_tariff(self):
        states = [f'Versicherungstarif=="{x}"' for x in self.data['Versicherungstarif'].unique()]

        self.tariff = Vertex(self.data, "Versicherungstarif", states)
        self.tariff.register_parent(self.age)
        self.tariff.register_parent(self.fam_status)
        self.tariff.register_parent(self.job)
        self.tariff.register_parent(self.salary)
        self.tariff.register_parent(self.prop_owner)
        self.tariff.update_cpt()
        self.tariff.get_cpt()


    def print_all_cpts(self):
        print("These are all CPTs")
        print("________________________________________________________________________________________________________________")
        print(self.age.get_cpt())
        print("________________________________________________________________________________________________________________")
        print(self.sex.get_cpt())
        print("________________________________________________________________________________________________________________")
        print(self.fam_status.get_cpt())
        print("________________________________________________________________________________________________________________")
        print(self.children.get_cpt())
        print("________________________________________________________________________________________________________________")
        print(self.education.get_cpt())
        print("________________________________________________________________________________________________________________")
        print(self.job.get_cpt())
        print("________________________________________________________________________________________________________________")
        print(self.salary.get_cpt())
        print("________________________________________________________________________________________________________________")
        print(self.prop_owner.get_cpt())
        print("________________________________________________________________________________________________________________")
        print(self.tariff.get_cpt())
    
    def P(self, query):
        total = len(self.data)
        x = self.data.query(query)
        return len(x)/total

    def tests(self):
        # Herausfiltern aller Personen unter 20 Jahre
        u20 = self.data[self.data['Alter'] < 20]
        # Anzahl der herausgefilterten Datensätze durch Gesamtzahl teilen
        print("Test results")
        print("________________________________________________________________________________________________________________")
        print(str(len(u20)/len(self.data)))

        # Gleiches für die beiden anderen Altersgruppen
        ue20 = self.data[(self.data['Alter'] >= 20) & (self.data['Alter'] < 65)]
        print("________________________________________________________________________________________________________________")
        print("Altersgruppe: " + str(len(ue20)/len(self.data)))

        ue65 = self.data[self.data['Alter'] >= 65]
        print("________________________________________________________________________________________________________________")
        print("Altersgruppe: " + str(len(ue65)/len(self.data)))

        
        print("________________________________________________________________________________________________________________")
        print('P(A und B): ')
        print(self.P('Familienstand=="ledig" & Alter < 20'))
        l_u20 = self.data[(self.data['Alter'] < 20) & (self.data['Familienstand'] == 'ledig')]
        print(len(l_u20)/len(self.data))

        print("________________________________________________________________________________________________________________")
        print("P(B):  " + str(self.P('Alter < 20')))
        print("________________________________________________________________________________________________________________")
        print("P(A|B) = P(A und B)/P(B): " + str(self.P('Familienstand=="ledig" & Alter < 20')/self.P('Alter < 20')))


        # Test, ob P(Bachelor | 20-65 & weiblich) stimmt --> Zeile 25 im Dataframe.
        p_a_und_b = self.P('Bildungsstand=="Bachelor" & Alter >=20 & Alter < 65 & Geschlecht=="weiblich"')
        p_b = self.P('Alter >=20 & Alter < 65 & Geschlecht=="weiblich"')
        print("________________________________________________________________________________________________________________")
        print("Zeile 25: " + str(p_a_und_b / p_b))