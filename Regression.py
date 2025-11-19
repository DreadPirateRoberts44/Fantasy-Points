from pathlib import Path
from tkinter import filedialog
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from Loader import getPlayerData



# Determine if we're using the original file or a modified file
choice = int(input("Choose mode:\n1. Use original file and don't update modified\n2. Use original file and update modified\n3. Use  modified\n"))

# Get the file with the data
file = filedialog.askopenfilename()
df = getPlayerData(file, choice)

# TODO look to split data
#dfs_by_category = {category: df_group for category, df_group in df.groupby("FantPos")}

#df_WR = dfs_by_category[3]

# TODO Clean data so it doesn't need the weird spacing substitute \xa0
# TODO Clean data so the different yard types are named
X = df[["Age","Height (inches)", "Weight", 
        "College", "College wins", "College losses", 
        "Draft Round", "Draft Year", 
        "40\xa0Yard", "Bench Press", "Vert Leap\xa0(in)", "Broad Jump\xa0(in)", "Shuttle", "3Cone",
        "PreviousSeasonsCount", "PreviousScore", "PreviousPlayed", "PreviousStarts"]]

Y = df["FantPt"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, Y, train_size=.8)

regModel = LinearRegression()

regModel.fit(X_train, y_train)

y_pred = regModel.predict(X_test)



# The coefficients
print("Coefficients: \n", regModel.coef_)
# The mean squared error
print("Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))
# The coefficient of determination: 1 is perfect prediction
print("Coefficient of determination: %.2f" % r2_score(y_test, y_pred))
"""
# Plot outputs
plt.scatter(X_test["Weight"], y_test, color="black")
plt.plot(X_test["Weight"], y_pred, color="blue", linewidth=3)

plt.xticks(())
plt.yticks(())

plt.show()
"""