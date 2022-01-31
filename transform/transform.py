class Transform:
    """
    Currently supports the following calculations:

    24 hour volume for a given token
    """
    def __init__(self, tokens_to_data):
        self.tokens_to_data = tokens_to_data

    def volume(self, swaps):
        return sum(swaps)

    def liquidity(self, mints, burns):
        return

    def metric_mapper(self, metric_data):
        metric_map = {
            "swaps": [self.volume]
        }
        return metric_map[metric_data]

    def run_transformation(self):
        tokens_to_metrics = {}
        for token in self.tokens_to_data:
            tokens_to_metrics[token] = {}
            for metric_data in self.tokens_to_data[token]:
                try:
                    for calc_func in self.metric_mapper(metric_data):
                        tokens_to_metrics[token][metric_data] = calc_func(self.tokens_to_data[token][metric_data]) 
                except Exception as e:
                    print("The metric data may not be supported yet, \
                           please check if there are calculation functions for the data you are passing in.")
                    print(e)

        return tokens_to_metrics
