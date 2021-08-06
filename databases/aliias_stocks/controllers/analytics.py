import adaptors.company as company_adaptor
import manager
import numpy as np
import matplotlib.pyplot as plt

def calculate_correlation(period):

    plots = {}

    for company in company_adaptor.get_all_companies():
        for evaluation in company.get_evaluations():
            if evaluation.evaluator_name not in plots.keys():
                plots[evaluation.evaluator_name] = {'rating': [], 'growth': []}
            
            growth = company.performance(evaluation.date, period)

            if growth:

                plots[evaluation.evaluator_name]['rating'].append(evaluation.rating)
                plots[evaluation.evaluator_name]['growth'].append(growth)

    plt.scatter(plots['modelOne']['rating'], plots['modelOne']['growth'])
    plt.show()


    return plots

