# Python API Project

## Objective
This project was made for my personal learning purposes.

The APIs were first tested on my local machine. Then they were deployed to a remote Ubuntu server and tested via Postman.

I have written Documentation for deploying a single Flask application on the Ubuntu server as well as another Documentation to deploy a second application alongside the first. The two apps can run on different ports on the same machine.

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