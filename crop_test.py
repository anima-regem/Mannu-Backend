def find_crop(n, p, k, temperature, humidity, ph, rainfall):
    import numpy as np
    import pandas as pd
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.preprocessing import MinMaxScaler

    # Load the dataset
    df = pd.read_csv('Crop_recommendation.csv')

    # Prepare the data for modeling
    c = df.label.astype('category')
    targets = dict(enumerate(c.cat.categories))
    df['target'] = c.cat.codes
    y = df.target
    X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]

    # Scale the features
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    # Train the KNN model
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_scaled, y)

    # Function to make predictions based on user input
    def make_prediction(n, p, k, temperature, humidity, ph, rainfall):
        input_data = np.array([[n, p, k, temperature, humidity, ph, rainfall]])
        input_data_scaled = scaler.transform(input_data)
        prediction = knn.predict(input_data_scaled)
        crop = targets[prediction[0]]
        return crop


    predicted_crop = make_prediction(n, p, k, temperature, humidity, ph, rainfall)
    return predicted_crop
