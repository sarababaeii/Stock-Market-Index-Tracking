from stocks_data import StocksData
import matplotlib.pyplot as plt
import gams
import os

BASE_DIR = os.path.abspath('')
ws = gams.GamsWorkspace(working_directory=BASE_DIR)

def set_input_data(training_data, c):
        db = ws.add_database()
        
        i_python = [str(i) for i in range(len(training_data.stocks))]
#        print("i:", i_python, "\n")
        i = db.add_set("i", 1)
        for ip in i_python:
                i.add_record(ip)
        
        t_python = [str(t) for t in range(len(training_data.index[0]))]
#        print("t:", t_python, "\n")
        t = db.add_set("t", 1)
        for tp in t_python:
                t.add_record(tp)

        r1_python = {}
        for tp in range(len(training_data.index[0])):
                r1_python[str(tp)] = training_data.index[0][tp]
#        print("r1:", r1_python, "\n")
        r1 = db.add_parameter_dc("r1", [t])
        for tp in t_python:
                r1.add_record(tp).value = r1_python[tp]
                
        r_python = {}
        for ip in range(len(training_data.stocks)):
                for tp in range(len(training_data.stocks[ip])):
                        r_python[str(ip), str(tp)] = training_data.stocks[ip][tp]
#        print("r:", r_python, "\n")
        r = db.add_parameter_dc("r", [i, t])
        for ip in i_python:
                for tp in t_python:
                        r.add_record((ip, tp)).value = r_python[(ip, tp)]
                        
        c_python = c
#        print("c:", c_python, "\n")
        c = db.add_parameter("c", 0)
        c.add_record().value = c_python

        l_python = 0.01
#        print("l:", l_python, "\n")
        l = db.add_parameter("l", 0)
        l.add_record().value = l_python

        u_python = 0.3
#        print("u:", u_python, "\n")
        u = db.add_parameter("u", 0)
        u.add_record().value = u_python
                
        return db

def run_model(db):
        opt = ws.add_options()
        opt.defines["gdxincname"] = db.name
        m = ws.add_job_from_file("rm.gms")
        m.run(opt, databases=db)
        return m

def show_output_data(m):
        var_z = [rec.level for rec in m.out_db["z"]]
        print("z: ", var_z[0], "\n")

        var_delta = []
        for rec in m.out_db["delta"]:
                if int(rec.level) != 0:
                    var_delta.append((rec.key(0), rec.level))
        print("delta: ", var_delta, "\n")

        var_x = []
        for rec in m.out_db["x"]:
                var_x.append(float(rec.level))
        print("x: ", var_x, "\n")
        
        return var_x

def draw_chart(weeks, market_value, portfolio_value, error, title):
        plt.plot(weeks, market_value, label = "Index")
        plt.plot(weeks, portfolio_value, label = "RM")
        plt.xlabel("week, error = " + str(error))
        plt.ylabel("value")
        plt.title(title)
        plt.legend()
        plt.show()

def show_results(testing_data, stock_share, dataset, c):
        weeks = [i for i in range(len(testing_data.index[0]))]
        market = [testing_data.market_value(i) for i in range(len(testing_data.index[0]))]
        portfolio = [testing_data.portfolio_value(i, stock_share) for i in range(len(testing_data.index[0]))]
        error = testing_data.error(stock_share)
        draw_chart(weeks, market, portfolio, error, title=dataset + ", c = " + str(c))

dataset = input("Dataset Name: ") # without postfix
c = int(input("Number of stocks will be chosen: "))

#dataset = "Dataset1"
#c = 10

training_data = StocksData.extract_training_data(dataset=dataset + '.xlsx')
db = set_input_data(training_data, c)
m = run_model(db)
results = show_output_data(m)

testing_data = StocksData.extract_testing_data(dataset=dataset + '.xlsx')
show_results(testing_data, results, dataset, c)
