from loadFiles import telemetry_df,errors_df,maint_df,failures_df,machines_df
from sklearn.linear_model import LinearRegression


def lin_regress(x,y):
    linear_regressor = LinearRegression()  # create object for the class
    linear_regressor.fit(x, y)  # perform linear regression
    y_pred = linear_regressor.predict(x)  # make predictions
    return y_pred