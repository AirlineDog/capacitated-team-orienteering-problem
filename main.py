from Model import *
from Solution import *


mod = Model()
mod.load_model("Instance.txt")
mod.build_cost_matrix()
mod.build_selection_matrix()
s = Solution(mod)
s.solve()
