from file_manager import FileManager


class StocksData:
        def __init__(self, stocks, index):
                self.stocks = stocks
                self.index = index

        def market_value(self, week_num):
                val = 1.0
                for t in range(week_num + 1):
                        val *= (1 + self.index[0][t])
                return val

        def stock_value(self, week_num, stock_index):
                val = 1.0
                for t in range(week_num + 1):
                        val *= (1 + self.stocks[stock_index][t])
                return val
        
        def portfolio_value(self, week_num, stock_share):
                val = 0.0
                for i in range(len(stock_share)):
                        val += self.stock_value(week_num, i) * stock_share[i]
                return val

        def weekly_error(self, stock_share, week_num):
                e = 0.0
                for i in range(len(stock_share)):
                        e += self.stocks[i][week_num] * stock_share[i] - self.index[0][week_num]
                return e * e
                
        def error(self, stock_share):
                e = 0.0
                for t in range(len(self.index[0])):
                        e += self.weekly_error(stock_share, t)
                return e
                
        @staticmethod
        def initialize_list(rows, cols):
                r = [[0.0 for i in range(cols)] for j in range(rows)]
                return r

        @staticmethod
        def extract_data(raw_data, week_num, min_index, max_index):
                r = StocksData.initialize_list(rows=max_index-min_index+1, cols=week_num)
                for t in range(1, week_num + 1):
                        for i in range(min_index - 1, max_index):
                                r[i - min_index + 1][t - 1] = float(raw_data[t][i])
                return r

        @staticmethod
        def extract_index_data(raw_data, week_num):
                return StocksData.extract_data(raw_data, week_num, min_index=101, max_index=101)

        @staticmethod
        def extract_stocks_data(raw_data, week_num):
               return StocksData.extract_data(raw_data, week_num, min_index=1, max_index=100)

        @staticmethod               
        def extract_training_index_data(raw_data):
                        return StocksData.extract_index_data(raw_data, week_num=104)

        @staticmethod
        def extract_training_stocks_data(raw_data):
                        return StocksData.extract_stocks_data(raw_data, week_num=104)

        @staticmethod
        def extract_training_data(dataset):
                raw_data = FileManager.read_from_excel(file_name=dataset, sheet_name='IS_R')
                stocks_data = StocksData.extract_training_stocks_data(raw_data)
                index_data = StocksData.extract_training_index_data(raw_data)
                return StocksData(stocks_data, index_data)

        @staticmethod               
        def extract_testing_index_data(raw_data):
                return StocksData.extract_index_data(raw_data, week_num=52)

        @staticmethod
        def extract_testing_stocks_data(raw_data):
                return StocksData.extract_stocks_data(raw_data, week_num=52)

        @staticmethod
        def extract_testing_data(dataset):
                raw_data = FileManager.read_from_excel(file_name=dataset, sheet_name='OS_R')
                stocks_data = StocksData.extract_testing_stocks_data(raw_data)
                index_data = StocksData.extract_testing_index_data(raw_data)
                return StocksData(stocks_data, index_data)
