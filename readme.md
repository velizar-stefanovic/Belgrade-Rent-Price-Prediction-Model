![cover photo](https://i.postimg.cc/4NzPfp6V/Screenshot-at-Aug-15-14-00-39.png)

# Belgrade Renting Price Prediction Tool

The Renting Price Prediction Tool is designed to assist users in estimating rental prices for properties in Belgrade, Serbia. The project involves the collection, cleaning, and analysis of rental data from the popular Serbian renting website - [Nekretnine](www.nekretnine.rs). With this tool, users can input various property attributes such as property area size, number of rooms, heating type, general condition, and location to receive a predicted rental price in euros.

## Dataset

The dataset used for this project comprises approximately 5000 instances of rental listings scraped from [Nekretnine](www.nekretnine.rs). The dataset includes a variety of features such as property type, location, size, number of rooms, and more. Images were not included in the dataset. The dataset was cleaned and preprocessed using Python's Numpy and Pandas library to ensure accurate model training.

## Model Building

The final predictive model was built using Linear Regression from the Scikit-Learn library. However, during the development process, various machine learning algorithms were tested, including Decision Trees and Random Forests, to determine the most suitable model for predicting rental prices accurately. The model was trained on the cleaned dataset and optimized for performance.

## Technologies Used

- Python
- Numpy and Pandas for data cleaning and manipulation
- Matplotlib for data visualization
- Scikit-Learn for building and evaluating machine learning models
- Python Flask for creating the HTTP server to host the prediction tool
- HTML/CSS/Javascript for UI
