# Python API Project

## Objective
This project was made for my personal learning purposes.

The APIs were first tested on my local machine. Then they were deployed to a remote Ubuntu server and tested via Postman.

I have written Documentation for deploying a single Flask application on the Ubuntu server as well as another Documentation to deploy a second application alongside the first. The documentation's markdown source is also made available. The two apps can run on different ports on the same machine.

# Technologies Used
- Python
- Flask
- NumPy
- Pandas
- Postman
- SSH
- Nginx
- Ubuntu Server
- Gunicorn
# Documentation
### API 1
This app contains two functions, one for addition ('/add') and another for subtraction ('/subtract'). One needs to feed two numbers in JSON format as so:
``` JSON
{
    "num1": 2,
    "num2": 4
}
```
And the API returns a simple response with in the following format:
``` JSON
{
    "result": 6
}
```
### API 2
This app contains two functions, one for multiplication ('/multiply') and another for division ('/subtract'). One needs to feed two numbers in JSON format as so:
``` JSON
{
    "num1": 2,
    "num2": 4
}
```
And the API returns a simple response with in the following format:
``` JSON
{
    "result": 8
}
```

## API 3
This API was made after performing Exploratory Data Analysis on the 'foodhub_order.csv' dataset. This API return useful information about the dataset. The usual graphs such as bar graphs and box plots can be plotted using the data this API returns when asked for.
For example, the API costboxplotdata, returns the following JSON information:
``` JSON
{
    "Q1": 12.08,
    "Q3": 22.2975,
    "max": 35.41,
    "median": 14.14,
    "min": 4.47
}
```
From this the required box plot can be plotted for the column 'cost_of_the_order'.

There are around 20 functions in this API that return various information about the dataset.