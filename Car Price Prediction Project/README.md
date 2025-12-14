🚗 Car Price Prediction — Machine Learning Regression Case Study
📘 Overview

  This project focuses on building a Machine Learning model to predict the price of cars based on various features such as engine size, fuel type, horsepower, body style, and more.
  The case study is based on a dataset from Geely Auto, a Chinese automobile manufacturer planning to enter the U.S. market.
  
  The goal is to identify key factors that influence car pricing and to develop a model that can accurately predict car prices, helping management make informed business decisions.

🎯 Objective

  To model the price of cars using available independent variables and understand:
  
  Which variables are most significant in predicting the price.
  
  How well those variables describe the price of a car.
  
  How the pricing varies with different design and performance attributes.

📊 Dataset Description

The dataset contains various car attributes, including:

Feature	Description
  Car_ID	Unique identifier for each car
  Symboling	Insurance risk rating
  CarCompany	Manufacturer name
  FuelType	Type of fuel used (e.g., gas, diesel)
  Aspiration	Type of aspiration used in car
  CarBody	Body style of the car
  DriveWheel	Type of drive wheel (e.g., RWD, FWD)
  EngineLocation	Location of the engine
  WheelBase, CarLength, CarWidth, CarHeight	Car dimensions
  CurbWeight	Weight without occupants or luggage
  EngineType, CylinderNumber, EngineSize	Engine characteristics
  FuelSystem	Fuel supply system type
  Horsepower, PeakRPM	Engine performance
  CityMPG, HighwayMPG	Mileage performance
  Price	Target variable (dependent)



🧩 Technologies Used
  Category	Tools / Libraries
  Language	Python
  IDE	Jupyter Notebook
  Libraries	pandas, numpy, matplotlib, seaborn, scikit-learn, statsmodels
  Visualization	Matplotlib, Seaborn
  Modeling	Linear Regression, Ridge, Lasso, Decision Tree, Random Forest
📈 Results

  The final model achieved a high R² score on both training and testing datasets.

Key influencing factors include:

  Engine size
  
  Horsepower
  
  Curb weight
  
  Car width and length
  
  Brand (e.g., BMW, Audi, Toyota)

💡 Business Insights

  Performance-based variables (engine size, horsepower) strongly influence price.
  
  Luxury brands tend to have higher baseline prices.
  
  Fuel efficiency and body type also have moderate influence on pricing.
  
  Model insights can guide pricing strategy, product positioning, and design decisions in the U.S. market.
