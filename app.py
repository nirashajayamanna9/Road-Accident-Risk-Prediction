from flask import Flask, render_template, request
from predict import predict_accident

app = Flask(__name__)

def str_to_bool(value):
    """Convert string True/False from form to real boolean"""
    return True if value == "True" else False

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    error_message = None

    if request.method == 'POST':
        try:
            # Handle empty dropdowns safely
            def safe_get(name, default="unknown"):
                val = request.form.get(name)
                return val if val != "" else default

            input_data = {
                'road_type': safe_get('road_type'),
                'num_lanes': int(request.form.get('num_lanes', 0)),
                'curvature': float(request.form.get('curvature', 0)),
                'speed_limit': int(request.form.get('speed_limit', 0)),
                'lighting': safe_get('lighting'),
                'weather': safe_get('weather'),
                'road_signs_present': str_to_bool(request.form.get('road_signs_present')),
                'public_road': str_to_bool(request.form.get('public_road')),
                'time_of_day': safe_get('time_of_day'),
                'holiday': str_to_bool(request.form.get('holiday')),
                'school_season': str_to_bool(request.form.get('school_season')),
                'num_reported_accidents': int(request.form.get('num_reported_accidents', 0))
            }

            # Predict
            score = predict_accident(input_data)
            result = score


        except Exception as e:
            error_message = f"Prediction error: {str(e)}"

    return render_template('index.html', result=result, error_message=error_message)


if __name__ == '__main__':
    app.run(debug=True)
