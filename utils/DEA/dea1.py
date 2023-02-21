
###包络形式的CCR模型

import gurobipy
import pandas as pd
from gurobipy import quicksum

# 分页显示数据, 设置为 False 不允许分页
pd.set_option('display.expand_frame_repr', False)

# 最多显示的列数, 设置为 None 显示全部列
pd.set_option('display.max_columns', None)

# 最多显示的行数, 设置为 None 显示全部行
pd.set_option('display.max_rows', None)


class DEA(object):
    def __init__(self, DMUs_Name, X, Y, AP=False):
        self.m1, self.m1_name = X.shape[1], X.columns.tolist()
        self.m2, self.m2_name = Y.shape[1], Y.columns.tolist()
        self.AP = AP
        self.DMUs, self.X, self.Y = gurobipy.multidict({DMU: [X.loc[DMU].tolist(),
                                                              Y.loc[DMU].tolist()] for DMU in DMUs_Name})
        print(f'DEA(AP={AP}) MODEL RUNING...')
        # multidict扩展字典，便于处理同一个对象的不同属性约束

    def __CCR(self): ##input-oriented
        for k in self.DMUs:
            MODEL = gurobipy.Model()

            OE = MODEL.addVar()
            lambdas = MODEL.addVars(self.DMUs)

            MODEL.update()
            ## 更新变量环境
            MODEL.setObjective(OE, sense=gurobipy.GRB.MINIMIZE)

            MODEL.addConstrs(quicksum(lambdas[i] * self.X[i][j] for i in self.DMUs) <= OE * self.X[k][j] for j in range(self.m1))
            MODEL.addConstrs(quicksum(lambdas[i] * self.Y[i][j] for i in self.DMUs) >= self.Y[k][j] for j in range(self.m2))
            MODEL.setParam('OutputFlag', 0)
            MODEL.setParam('NonConvex',2)

            MODEL.optimize()

            self.Result.at[k, ('效益分析', '综合技术效益(CCR)')] = MODEL.objVal

        return self.Result


    def dea(self):
        columns_Page = ['效益分析']
        columns_Group = ['综合技术效益(CCR)']
        self.Result = pd.DataFrame(index=self.DMUs, columns=[columns_Page, columns_Group])
        self.__CCR()
        return self.Result

    def analysis(self, file_name=None):
        Result = self.dea()
        file_name = 'DEA 数据包络分析报告.xlsx' if file_name is None else f'\\{file_name}.xlsx'
        Result.to_excel(file_name, 'DEA 数据包络分析报告')


if __name__=='__main__':
    innum, outnum = 2, 1
    file = "样本数.xlsx"
    data = pd.read_excel(file, header=0, index_col=0)

    X = data[data.columns[:innum]]
    Y = data[data.columns[innum:innum+outnum]]

    dea = DEA(DMUs_Name=data.index, X=X, Y=Y)
    #dea.analysis()  # dea 分析并输出表格
    print(dea.dea())  # dea 分析，不输出结果


