from chat_plotter import ChatStatsPlotter
from chat_stat import ChatStats

group_name_list=['family',"yavne","brothers"]
for group_name in group_name_list:
    rel_path = f'whatsapp_stat/files/chat_{group_name}.txt'
    abs_path = f'C:/Users/SmadarENB3/OneDrive/Desktop/ofek/programing/python/whatsapp_stat/files/chat_{group_name}.txt'

    chat_stats = ChatStats(rel_path)
    plotter = ChatStatsPlotter(chat_stats)
    plotter.plot_all()