import numpy as np


def update(self, currentState, measurement, currentCovariance, error, driftError, measurementError, angularVelocity, dt):
    '\n\t\tCore function of Kalman relating to its implmentation\n\n\t\tParameters\n\t\t----------\n\t\tcurrentState: float array \n\t\t\t\t\tIt is current state of the sensor which implies current \n\t\t\t\t\torientation in a specific axis and its corresponding \n\t\t\t\t\tbias. ex - [roll, roll_bias]\n\t\tmeasurement: float \n\t\t\testimate of the orinetation by the sensor. ex - measuredRoll\n\t\tcurrentCovariance: 2*2 array \n\t\t\t\t\t\tThis represents matrix relating orientation and bias\n\t\t\t\t\t\tex - rollCovariance\n\t\terror: float\n\t\t\tThis represents error in estimating the orientation\n\t\tdriftError: float\n\t\t\t\tThis represents error in estimating the  bias in orientation\n\t\tmeasurementError: float\n\t\t\t\t\t\tThis represents error in sensor values\n\t\tangularVelocity: float\n\t\t\t\t\t\tThe angular velocity about the direction\n\t\t\t\t\t\tof orientation\n\t\tdt: float\n\t\t\ttime interval for kalman filter to be applied\n\n\t\tReturns\n\t\t-------\n\t\torientation: float\n\t\t\t\t\tIt is the corrected angle from previous\n\t\t\t\t\testimate and current measurment\n\t\tcorrectedState:\n\t\t\t\t\tIt is the corrected state from previous\n\t\t\t\t\testimate and current measurment\n\t\tupdatedCovariance: \n\t\t\t\t\tNew updated covariance after taking \n\t\t\t\t\tnew measurement into consideration\n\n\t\t'
    motionModel = np.array([[1, ((- 1) * dt)], [0, 1]])
    prediction = (np.matmul(motionModel, currentState) + (dt * np.vstack((angularVelocity, 0.0))))
    errorMatrix = (np.array([error, driftError]) * np.identity(2))
    predictedCovariance = (np.matmul(np.matmul(motionModel, currentCovariance), motionModel.T) + errorMatrix)
    difference = (measurement - np.matmul(np.array([1.0, 1.0]), prediction))
    measurementCovariance = (np.matmul(np.matmul(np.array([1.0, 0.0]), predictedCovariance), np.vstack((1.0, 0.0))) + measurementError)
    kalmanGain = (np.matmul(predictedCovariance, np.vstack((1.0, 0.0))) / measurementCovariance)
    correctedState = (prediction + (kalmanGain * (measurement - np.matmul(np.array([1.0, 0.0]), prediction))))
    updatedCovariance = np.matmul((np.identity(2) - np.matmul(kalmanGain, np.array([1.0, 0.0]).reshape((1, 2)))), predictedCovariance)
    return (correctedState[(0, 0)], correctedState, updatedCovariance)
