from flask import Flask, jsonify
import pandas as pd
import io
import json
import numpy as np

app = Flask(__name__)

# Load the CSV data into a DataFrame
data = pd.read_csv('foodhub_order.csv')

@app.route('/', methods=['GET'])
def index():
    return "Hello, this is the root of the API!"


@app.route('/firstfiverows', methods=["GET"])
def get_first_five_rows():
    # Get the first 5 rows from the DataFrame
    first_five_rows = data.head(5).to_dict(orient='records')

    # Convert the data to JSON and return as a response
    return jsonify(first_five_rows)


@app.route('/rowsandcols', methods=["GET"])
def get_rowsandcols():
    num_rows, num_cols = data.shape
    result = {
        'number_of_rows': num_rows,
        'number_of_columns': num_cols
    }
    return jsonify(result)


@app.route('/colinfo', methods=["GET"])
def get_data_info_full():
    # Capture the stdout output of data.info() into a variable
    buffer = io.StringIO()
    data.info(buf=buffer)
    data_info_output = buffer.getvalue()

    # Return the data_info_output as a JSON-formatted response
    return jsonify(data_info_output)


@app.route('/nullpercol', methods=["GET"])
def get_nullpercol():
    nullvaluespercol = data.isnull().sum().to_dict()
    return jsonify(nullvaluespercol)


@app.route('/describe', methods=["GET"])
def get_describe():
    desc = data.describe().to_dict()
    return jsonify(desc)


@app.route('/unratedorders', methods=["GET"])
def get_unratedorders():
    unratedorders = data[data['rating'] == 'Not given'].shape[0]
    result = {
        "Number of unrated orders": unratedorders
    }
    return jsonify(result)


@app.route('/uniquevalues/<column_name>', methods=["GET"])
def get_uniquevalues(column_name):
    if column_name in data.columns:
        uniquevalues_count = data[column_name].nunique()
        unique_values = {
            "column name": column_name,
            "number of unique values": uniquevalues_count
        }
        return jsonify(unique_values)
    else:
        return jsonify({"error": "Column name not found"})


@app.route('/uniquecuisines', methods=['GET'])
def unique_cuisines():
    unique_cuisine_counts = data['cuisine_type'].value_counts(sort=True).to_dict()
    return jsonify(unique_cuisine_counts)


@app.route('/ordercostcounts', methods=['GET'])
def get_ordercostcounts():
    cost_counts = data['cost_of_the_order'].value_counts().sort_index()
    costs = cost_counts.index.tolist()
    counts = cost_counts.tolist()

    cost_counts_dict = {cost: count for cost, count in zip(costs, counts)}
    return jsonify(cost_counts_dict)


@app.route('/costhistogramdata', methods=['GET'])
def get_cost_histogram_data():
    try:
        cost_data = data['cost_of_the_order']
        bin_edges = np.arange(0, 40, 2)  # Bin edges from 0 to 30 with a range of 2

        # Calculate the histogram
        hist, _ = np.histogram(cost_data, bins=bin_edges)

        # Convert the values in hist to Python integers
        hist = hist.tolist()

        # Create the dictionary with keys and values
        result = {}
        for i in range(len(bin_edges) - 1):
            range_str = f"{bin_edges[i]} to {bin_edges[i + 1]}"
            result[range_str] = hist[i]

        # Sort the dictionary keys numerically
        sorted_result = dict(sorted(result.items(), key=lambda x: int(x[0].split()[2])))

        # Use json.dumps for nicely formatted JSON
        response_json = json.dumps(sorted_result, indent=4)

        # Return the nicely formatted JSON response
        return response_json, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/costboxplotdata', methods=['GET'])
def get_costboxplotdata():
    try:
        cost_data = data['cost_of_the_order']

        minimum = np.min(cost_data)
        q1 = np.percentile(cost_data, 25)
        median = np.median(cost_data)
        q3 = np.percentile(cost_data, 75)
        maximum = np.max(cost_data)

        result = {
            "min": minimum,
            "Q1": q1,
            "median": median,
            "Q3": q3,
            "max": maximum
        }

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/ratingcounts', methods=['GET'])
def get_ratingcounts():
    try:
        rating_counts = {
            "Rating Not given": int((data['rating'] == 'Not given').sum()),
            "0 stars": int((data['rating'] == '0').sum()),
            "1 stars": int((data['rating'] == '1').sum()),
            "2 stars": int((data['rating'] == '2').sum()),
            "3 stars": int((data['rating'] == '3').sum()),
            "4 stars": int((data['rating'] == '4').sum()),
            "5 stars": int((data['rating'] == '5').sum())
        }

        return jsonify(rating_counts)
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/top10resto', methods=['GET'])
def get_top10resto():
    try:
        top10resto = data['restaurant_name'].value_counts().head(10).to_dict()
        top10resto_sorted = sorted(top10resto.items(), key=lambda x: x[1], reverse=True)
        return top10resto_sorted
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/popularweekendcuisine', methods=['GET'])
def get_popularweekendcuisine():
    data_weekend_cuisine = data[data['day_of_the_week'] == 'Weekend']
    top_cuisine = data_weekend_cuisine['cuisine_type'].value_counts().head(10).to_dict()
    top_cuisine_sorted = sorted(top_cuisine.items(), key=lambda x: x[1], reverse=True)
    return top_cuisine_sorted


@app.route('/percentageabove/<cost>', methods=['GET'])
def get_percentageabove(cost):
    try:
        orders_above = (data['cost_of_the_order'] > float(cost)).sum()
        total_orders = len(data)
        percentage = (orders_above / total_orders) * 100

        return jsonify({f"percentage above {cost}": percentage})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/top3customers', methods=['GET'])
def get_top3customers():
    try:
        top_customers_data = data['customer_id'].value_counts().head(3)
        result = []

        for customer_id, num_orders in top_customers_data.items():
            result.append({"customer_id": customer_id, "number_of_orders": num_orders})

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/cuisinevscost', methods=['GET'])
def cuisinevscost():
    try:
        result = []

        for cuisine_type in data['cuisine_type'].unique():
            cuisine_data = data[data['cuisine_type'] == cuisine_type]['cost_of_the_order']

            if not cuisine_data.empty:
                min_cost = cuisine_data.min()
                q1 = cuisine_data.quantile(0.25)
                median = cuisine_data.median()
                q3 = cuisine_data.quantile(0.75)
                max_cost = cuisine_data.max()

                result.append({
                    "cuisine_type": cuisine_type,
                    "minimum_cost": min_cost,
                    "Q1": q1,
                    "median": median,
                    "Q3": q3,
                    "max": max_cost
                })

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/comparedeliverytime', methods=['GET'])
def get_compare_delivery_time():
    try:
        result = []

        for day in data['day_of_the_week'].unique():
            day_data = data[data['day_of_the_week'] == day]['delivery_time']

            if not day_data.empty:
                min_delivery_time = float(day_data.min())
                q1_delivery_time = float(day_data.quantile(0.25))
                median_delivery_time = float(day_data.median())
                q3_delivery_time = float(day_data.quantile(0.75))
                max_delivery_time = float(day_data.max())

                result.append({
                    "day_of_the_week": day,
                    "minimum_delivery_time": min_delivery_time,
                    "Q1_delivery_time": q1_delivery_time,
                    "median_delivery_time": median_delivery_time,
                    "Q3_delivery_time": q3_delivery_time,
                    "max_delivery_time": max_delivery_time
                })

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/restaurantrevenue/<int:restaurant_num>', methods=['GET'])
def get_restaurantrevenue(restaurant_num):
    restaurant_revenue = (
        data.groupby(['restaurant_name'])['cost_of_the_order'].sum().sort_values(ascending=False).head(restaurant_num))

    result = []
    sorted_restaurants = restaurant_revenue.reset_index().to_dict(orient='records')

    for restaurant in sorted_restaurants:
        result.append({
            "restaurant": restaurant['restaurant_name'],
            "revenue": round(restaurant['cost_of_the_order'], 2)
        })
    return jsonify(result)


@app.route('/ratingsvsdelivery', methods=['GET'])
def ratings_average_delivery():
    result = []

    # Convert 'Not given' ratings to None
    modified_data = data.copy()
    modified_data['rating'].replace('Not given', None, inplace=True)

    # Simulate average delivery time (replace this with actual calculation)
    avg_delivery_times = [20, 25, 30, 35, 40]  # Example values

    unique_ratings = modified_data['rating'].unique()

    for i, rating in enumerate(unique_ratings):
        if rating is None:
            rating_str = 'Not given'
        else:
            rating_str = str(rating) + ' stars'

        result.append({
            'rating': rating_str,
            'average delivery time': avg_delivery_times[i]
        })

    return jsonify(result)


@app.route('/highratedrestaurants/<int:num>', methods=['GET'])
def get_rated_restaurant_counts(num):
    # Filter the rated restaurants
    df_rated = data[data['rating'] != 'Not given'].copy()

    # Convert rating column from object to integer
    df_rated['rating'] = df_rated['rating'].astype('int')

    # Create a dataframe that contains the restaurant names with their rating counts
    df_rating_count = (
        df_rated.groupby(['restaurant_name'])['rating'].count().sort_values(ascending=False).reset_index().head(num))

    result = []
    for idx, row in df_rating_count.iterrows():
        result.append({
            'restaurant_name': row['restaurant_name'],
            'rating_count': row['rating']
        })

    return jsonify(result)


@app.route('/test', methods=['GET'])
def get_test():
    h = 'Hello, World!'
    return jsonify(h)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8987)
