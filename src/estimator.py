def estimator(data):
    impact = {}
    severe_impact = {}
    region = data.get('region')
    period_type = data.get('periodType')
    time_to_elapse = data.get("timeToElapse")
    reported_cases = data.get("reportedCases")
    population = data.get("population")
    total_hospital_beds = data.get('totalHospitalBeds')

    currently_infected = reported_cases * 10
    severe_currently_infected = reported_cases * 50
    impact["currentlyInfected"] = currently_infected
    severe_impact["currentlyInfected"] = severe_currently_infected

    multiplier = _compute_multiplier(period_type, time_to_elapse)
    impact["infectionsByRequestedTime"] = currently_infected * multiplier
    severe_impact["infectionsByRequestedTime"] = severe_currently_infected * multiplier

    impact["severeCasesByRequestedTime"] = impact["infectionsByRequestedTime"] * 0.15
    severe_impact["severeCasesByRequestedTime"] = severe_impact["infectionsByRequestedTime"] * 0.15

    available_hospital_beds = total_hospital_beds * 0.35
    impact["hospitalBedsByRequestedTime"] = available_hospital_beds - impact["severeCasesByRequestedTime"]
    severe_impact["hospitalBedsByRequestedTime"] = available_hospital_beds - severe_impact["severeCasesByRequestedTime"]

    impact["casesForICUByRequestedTime"] = impact["infectionsByRequestedTime"] * 0.05
    severe_impact["casesForICUByRequestedTime"] = severe_impact["infectionsByRequestedTime"] * 0.05

    impact["casesForVentilatorsByRequestedTime"] = impact["infectionsByRequestedTime"] * 0.02
    severe_impact["casesForVentilatorsByRequestedTime"] = severe_impact["infectionsByRequestedTime"] * 0.02

    duration = _compute_duration_in_days(period_type, time_to_elapse)
    impact["dollarsInFlight"] = impact["infectionsByRequestedTime"] * region.get("avgDailyIncomePopulation") * region.get("avgDailyIncomeInUSD") * duration
    severe_impact["dollarsInFlight"] = severe_impact["infectionsByRequestedTime"] * region.get("avgDailyIncomePopulation") * region.get("avgDailyIncomeInUSD") * duration

    return {"data": data, "impact": impact, "severeImpact": severe_impact}


def _compute_multiplier(period_type, time_to_elapse):
    duration = _compute_duration_in_days(period_type, time_to_elapse)
    factor = int("%d" % (duration / 3))
    return 2 ** factor


def _compute_duration_in_days(period_type, time_to_elapse):
    duration = 0
    if period_type == "days":
        duration = time_to_elapse
    elif period_type == "weeks":
        duration = time_to_elapse * 7
    elif period_type == "months":
        duration = time_to_elapse * 30
    return duration
