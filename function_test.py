import databases.aliias_stocks.controllers.analytics as analytics
import databases.aliias_stocks.helpers.timeline as timeline
import databases.aliias_stocks.manager as db_manager
import datetime
import databases.aliias_stocks.controllers.data_pipeline as data_pipeline

today = str(datetime.date.today())
db_manager.setup_network_connection('aliias')


analytics.collect_and_save_plots(3751, timeline.change_months(today, -12), timeline.change_months(today, -24))
