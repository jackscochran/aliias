import adaptors.stock_adaptor as stock_adaptor

def calculate_correlation(period):

    plots = {}

    for company in stock_adaptor.get_all_companies():
        for evaluation in company.get_evaluations():
            if evaluation.evaluator not in plots.keys():
                plots[evaluation.evaluator] = {'rating': [], 'growth': []}
            
            growth = company.revenue_growth(evaluation.date, period)

            if growth:

                plots[evaluation.evaluator]['rating'].append(evaluation.rating)
                plots[evaluation.evaluator]['growth'].append(growth)

    return plots
            
