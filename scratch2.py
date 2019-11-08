import pstats
stats = pstats.Stats("profiling_resultNewest2")
stats.sort_stats("cumtime")
stats.print_stats(500)

