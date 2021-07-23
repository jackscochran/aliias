import controllers.data_pipeline as data_pipeline
import datetime

# collect data on all the companies who released their earnings yesterday
data_pipeline.collect_earnings(str(datetime.date.today() - datetime.timedelta(days=1)))
