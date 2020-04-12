class Person:
    
    def __init__(self, df_row):
        self.sex = df_row[0]
        self.fam_status = df_row[1]
        self.age = df_row[2]
        self.children = df_row[3]
        self.education = df_row[4]
        self.job = df_row[5]
        self.salary = df_row[6]
        self.prop_owner = df_row[7]
        self.tariff = df_row[8]
        
    def get_bayes_query(self):
        query = []
        query.append(None if self.sex==None else f'Geschlecht=="{self.sex}"')
        query.append(None if self.fam_status==None else f'Familienstand=="{self.fam_status}"')
        query.append(None if self.age==None else 'Alter < 20' if self.age < 20 
                     else 'Alter >=20 & Alter < 65' if 20 <= self.age < 65 
                     else 'Alter>=65')
        query.append(None if self.children==None else 'Kinder < 3' if self.children < 3 else 'Kinder >= 3')
        query.append(None if self.education==None else f'Bildungsstand=="{self.education}"')
        query.append(None if self.job==None else f'Beruf=="{self.job}"')
        query.append(None if self.salary==None else 'Jahresgehalt < 10000' if self.salary < 10000
                     else 'Jahresgehalt >= 10000 & Jahresgehalt < 60000' if 10000 <= self.salary < 60000
                     else 'Jahresgehalt >= 60000 & Jahresgehalt < 80000' if 60000 <= self.salary < 80000
                     else 'Jahresgehalt >= 80000 & Jahresgehalt < 100000' if 80000 <= self.salary < 100000
                     else 'Jahresgehalt >= 100000')
        query.append(None if self.prop_owner==None else f'Immobilienbesitz=="{self.prop_owner}"')
        query.append(None if self.tariff==None else f'Versicherungstarif=="{self.tariff}"')
        
        return query