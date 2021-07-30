import controllers.data_pipeline as data_pipeline
import datetime
import sys

# collect data on all the companies who released their earnings yesterday

if __name__ == '__main__':

    command = sys.argv[1]
    print(command)

    if command == 'earnings_calender':
        data_pipeline.collect_earnings(str(datetime.date.today() - datetime.timedelta(days=1)))

    if command == 'collect_current_prices':
        data_pipeline.collect_current_prices()