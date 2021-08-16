import adaptors.company as company_adaptor
import adaptors.portfolio as portfolio_adaptor
import manager
import numpy as np
import matplotlib.pyplot as plt
import helpers.timeline as timeline
import datetime
import scipy.stats as scipy_stats

# ---------- Helper Functions --------- #

# ---------- Porfolio Performance Functions --------- #

# ---------- Stock Performance Functions ----------#

# ---------- Correlation Functions ---------- #

def calculate_correlation(sample_size, period):

    plots = get_performance_rating_plots([company.ticker for company in company_adaptor.get_n_companies(sample_size)], period)

    correlation = scipy_stats.pearsonr(plots['modelOne']['rating'], plots['modelOne']['growth'])
    print(correlation)
    plt.scatter(plots['modelOne']['rating'], plots['modelOne']['growth'])
    plt.show()


    return correlation

def get_portfolio_performance_ratings(period):
    portfolio = portfolio_adaptor.get_current_board()

    plots = get_performance_rating_plots(portfolio.tickers, period)

    print(plots)
    return sum(plots['modelOne']['growth']) / len(plots['modelOne']['growth'])

def get_performance_rating_plots(company_tickers, period):
    plots = {}
    count = 0
    for ticker in company_tickers:
        company = company_adaptor.get_company(ticker)
        count+=1
        print(str(count) + ' / ' + str(len(company_tickers)) + ' - ' + ticker)
        for evaluation in company.get_evaluations():
            if evaluation.evaluator_name not in plots.keys():
                plots[evaluation.evaluator_name] = {'rating': [], 'growth': []}
            
            growth = company.performance(timeline.change_months(str(datetime.date.today()), -period), period)

            if growth:

                plots[evaluation.evaluator_name]['rating'].append(evaluation.rating)
                plots[evaluation.evaluator_name]['growth'].append(growth)

    return plots