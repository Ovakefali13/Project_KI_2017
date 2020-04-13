import pandas as pd
import seaborn as sns
import numpy as np
from pomegranate import *
from CPTCalculator import CPTCalculator
from BayesNetwork import BayesNetwork
import os
from Person import Person
import platform

def clear():
    if(platform.system() == 'Linux' or platform.system() == 'Darwin'):
        os.system('clear')
    else:
        os.system('cls')

def show_plot_no_1(data):
    unknown_vars = ['Bildungsstand', 'Familienstand', 'Beruf', 'Kinder', 'Jahresgehalt', 'Immobilienbesitz']
    print("Scaterplots can't be shown in the console please see documnetation or jupyter notebook")
    print("________________________________________________________________________________________________________________")
    for var in unknown_vars:
        if var == 'Jahresgehalt':
            pass
        else:
            print(sns.catplot(x=var, y='Alter', data=data))
            print(sns.catplot(x=var, hue='Geschlecht', data=data, kind='count'))
    print("________________________________________________________________________________________________________________")
    # Geschlecht vs Gehalt
    print(data.groupby('Geschlecht').describe()['Jahresgehalt'])

def show_plot_no_2(data):
    cont_vars = ['Alter', 'Jahresgehalt', 'Kinder']
    print("Scaterplots can't be shown in the console please see documnetation or jupyter notebook")
    print("________________________________________________________________________________________________________________")
    for cont in cont_vars:
        print(sns.catplot(x='Versicherungstarif', y=cont, data=data))
    
    print(sns.catplot(x='Immobilienbesitz', y='Kinder', data=data))

def table_one_hot_encoding(data):
    # one-hot encoding
    data_dummies = pd.get_dummies(data)
    return data_dummies

def prob_calculation(data):
    data_dummies = table_one_hot_encoding(data)

    # categorical input variables
    cat_columns = ['Geschlecht_maennlich', 'Geschlecht_weiblich', 'Familienstand_geschieden',
       'Familienstand_ledig', 'Familienstand_verheiratet',
       'Familienstand_verwitwet', 'Bildungsstand_Abitur',
       'Bildungsstand_Bachelor', 'Bildungsstand_Hauptschule',
       'Bildungsstand_Keine', 'Bildungsstand_Lehre', 'Bildungsstand_Master',
       'Bildungsstand_Promotion', 'Bildungsstand_Realschule',
       'Beruf_angestellt', 'Beruf_arbeitend', 'Beruf_im Ruhestand',
       'Beruf_kein', 'Beruf_selbständig', 'Beruf_verbeamtet',
       'Immobilienbesitz_Eigentumswohnung', 'Immobilienbesitz_Einfamilienhaus',
       'Immobilienbesitz_Mehrfamilienhaus', 'Immobilienbesitz_Villa',
       'Immobilienbesitz_keiner']

    total = len(data)
    print("________________________________________________________________________________________________________________")
    print("This is the total number of values")
    print("________________________________________________________________________________________________________________")
    print(total)

    # Calculating P(A)
    target_variables = ['Versicherungstarif_Tarif A',
       'Versicherungstarif_Tarif B', 'Versicherungstarif_Tarif C',
       'Versicherungstarif_ablehnen']
    p_A = {}
    for target in target_variables:
        p_A[target] = data_dummies[target].sum()/total
    print("________________________________________________________________________________________________________________")
    print("This is P(A)")
    print("________________________________________________________________________________________________________________")
    print(p_A)

    # Calculating P(B)
    p_B = {}
    for cat in cat_columns:
        p_B[cat] = data_dummies[cat].sum()/total
    print("________________________________________________________________________________________________________________")
    print("This is P(B)")
    print("________________________________________________________________________________________________________________")
    print(p_B)

    # Calculating P(A and B)
    p_A_and_B = {}
    for target in target_variables:
        for cat in cat_columns:
            b = data_dummies[cat] == 1
            a = data_dummies[target] == 1
            p_A_and_B[f'{target}_and_{cat}'] = len(data_dummies[a&b])/total
    print("________________________________________________________________________________________________________________")
    print("This is P(A and B)")
    print("________________________________________________________________________________________________________________")
    print(p_A_and_B)

    # Calculating P(A|B) = P(A and B)/P(B)
    p_A_given_B = {}
    for target in target_variables:
        for cat in cat_columns:
            p_A_given_B[f'{target}_given_{cat}'] = p_A_and_B[f'{target}_and_{cat}']/p_B[cat]     
    print("________________________________________________________________________________________________________________")
    print("This is P(A given B)")
    print("________________________________________________________________________________________________________________")
    print(p_A_given_B)

    print("________________________________________________________________________________________________________________")
    print("Now we are checking for stochastic independence")
    print("________________________________________________________________________________________________________________")
    # Checking for stochastic independence
    for target in target_variables:
        for cat in cat_columns:
            ratio = p_A_given_B[f'{target}_given_{cat}'] / p_A[target]
            if 4/5 < ratio < 5/4:
                print(f'{target[19:]} - {cat}')

def get_bayesian_network(cpt_calc):
    bayesian_network = BayesNetwork(cpt_calc)
    bayesian_network.add_edges()
    return bayesian_network

def print_examples_of_network(cpt_calc):
    bayes_network = get_bayesian_network(cpt_calc)
    print(bayes_network.run_example())

def test(data, cpt_calc):
    print("This is the test table we are using")
    print("________________________________________________________________________________________________________________")
    bayes_network = get_bayesian_network(cpt_calc)

    # Testdatensatz
    data_test = pd.read_csv('test_daten.csv', sep=";")
    data_test = data_test.where(pd.notnull(data_test), None)
    print(data_test.head())
    print("________________________________________________________________________________________________________________")
    print("This is the formated result of the Bayesian Network")
    print("________________________________________________________________________________________________________________")
    # Ausgabe der vorhergesagten Werte
    for index, row in data_test.iterrows():
        p = Person(data_test.iloc[index,:])
        array = bayes_network.model.predict([p.get_bayes_query()])
        print(str(index) + " (" + str(array[0][0]) + ")(" + str(array[0][1]) + ")(" + str(array[0][2]) + ")(" + str(array[0][3]) + ")(" + str(array[0][4]) + ")(" + str(array[0][5])
            + ")(" + str(array[0][6]) + ")(" + str(array[0][7]) + ")(" + str(array[0][8][20:]) + ")")
    print("________________________________________________________________________________________________________________")
    print("And this are the real values of the real table")
    print("________________________________________________________________________________________________________________")
    # Vergleich mit echten Werten
    print(data.head())

def main():
    # Data import
    data = pd.read_csv('Versicherung_A1.csv', sep=';')
    data.head()
    i = True
    while(i):
        print("________________________________________________________________________________________________________________")
        print("Welcome to our implementation of the Bayesian Network")
        print("________________________________________________________________________________________________________________")
        print("Please choose one of the following options")
        print("[0]: Show scaterplot of the influence of age and sex to the other variables")
        print("[1]: Show the  scaterplot of the influence of the variables to the tariff")
        print("[2]: Show True/False Table with one-hot encoding")
        print("[3]: Show calculation of P(A|B)")
        print("[4]: Show the calculated CPTs")
        print("[5]: Run the tests against the calculated CPTs")
        print("[6]: Show the examples of the Bayes Network")
        print("[7]: Test and evaluate based on dummy data")
        print("[8]: Exit")
        print("________________________________________________________________________________________________________________")
        choose = int(input("Your option: "))
        print("Your input is processed. Please wait...")

        if(choose == 0):
            clear()
            print("________________________________________________________________________________________________________________")
            show_plot_no_1(data)
        elif(choose == 1):
            clear()
            print("________________________________________________________________________________________________________________")
            show_plot_no_2(data)
        elif(choose == 2):
            clear()
            print("________________________________________________________________________________________________________________")
            print(table_one_hot_encoding(data).head())
        elif(choose == 3):
            clear()
            print("________________________________________________________________________________________________________________")
            prob_calculation(data)
        elif(choose == 4):
            cpt_calc = CPTCalculator(data)
            clear()
            print("________________________________________________________________________________________________________________")
            cpt_calc.print_all_cpts()
        elif(choose == 5):
            cpt_calc = CPTCalculator(data)
            clear()
            print("________________________________________________________________________________________________________________")
            cpt_calc.tests()
        elif(choose == 6):
            cpt_calc = CPTCalculator(data)
            clear()
            print("________________________________________________________________________________________________________________")
            print_examples_of_network(cpt_calc)
        elif(choose == 7):
            cpt_calc = CPTCalculator(data)
            clear()
            print("________________________________________________________________________________________________________________")
            test(data, cpt_calc)
        elif(choose == 8):
            i = False
            break
        print("________________________________________________________________________________________________________________")
        input("Press enter to return to return")

if __name__ == '__main__':
    main()
