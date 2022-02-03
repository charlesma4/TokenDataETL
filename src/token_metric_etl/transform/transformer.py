import traceback

class Transformer:
    supported_metrics = set([
        "volume",
        "liquidity"
    ])

    calculated_metrics = set([
        "volume"
    ])
    """
    Currently supports the following calculations:

    24 hour volume
    """
    def __init__(self, requested_metrics):
        self.requested_metrics = requested_metrics
        self.metric_map = {
            "volume": ("swaps", self.volume)
        }

    def volume(self, swaps):
        return sum(swaps)

    def run_transformation(self, tokens_to_data):
        tokens_to_metrics = {}
        for token in tokens_to_data:
            # pass extract timestamp to transformed result
            tokens_to_metrics[token] = {"timestamp": tokens_to_data[token]["timestamp"]}
            del tokens_to_data[token]["timestamp"]

            for metric in self.supported_metrics:
                if not self.requested_metrics[metric]:
                    continue

                if metric not in self.calculated_metrics:
                    tokens_to_metrics[token][metric] = tokens_to_data[token][metric]
                else:
                    try:
                        token_data_key, calc_func = self.metric_map[metric]
                        tokens_to_metrics[token][metric] = calc_func(tokens_to_data[token][token_data_key])
                    except Exception as e:
                        print(traceback.format_exc())
                        print("The metric data may not be supported yet, \
                               please check if there are calculation functions for the data you are passing in.")
                        print(traceback.format_exc())
        return tokens_to_metrics
