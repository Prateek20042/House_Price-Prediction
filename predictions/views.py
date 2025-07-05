from django.shortcuts import render, redirect
import requests

def predict_price(request):
    if request.method == "POST":
        bhk = int(request.POST["bhk"])
        area = float(request.POST["area"])
        bathroom = int(request.POST["bathroom"])
        car_parking = int(request.POST["car_parking"])
        furnishing = request.POST["furnishing"]
        address = request.POST["address"]

        furnishing_mapping = {"Unfurnished": 0, "Semi-Furnished": 1, "Furnished": 2}
        furnishing_num = furnishing_mapping.get(furnishing, 0)

        all_addresses = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Pune", "Hyderabad"]
        address_one_hot = [1 if address == city else 0 for city in all_addresses]

        features = [bhk, area, bathroom, car_parking, furnishing_num] + address_one_hot

        try:
            response = requests.post(
                "http://127.0.0.1:5000/predict",
                json={"features": features},
                timeout=10
            )
            if response.status_code == 200:
                predicted_price = response.json().get("predicted_price")
                request.session["predicted_price"] = predicted_price
            else:
                request.session["predicted_price"] = None
        except Exception as e:
            request.session["predicted_price"] = None
        return redirect("predict_price")  

    # GET request
    predicted_price = request.session.pop("predicted_price", None)
    return render(request, "predictions/predict.html", {"predicted_price": predicted_price})
