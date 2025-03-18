import pandas as pd

df = pd.DataFrame([(4, 2), (5, 1), (2, 4), (3, 3), (1, 5)], columns=["x", "y"])
print(df.corr())
