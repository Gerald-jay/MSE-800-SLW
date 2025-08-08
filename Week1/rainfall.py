def rainfall_analysis():
    import numpy as np

    sample_rainfall = [0.0, 5.2, 3.1, 0.0, 12.4, 0.0, 7.5]

    rainfalls = np.array(sample_rainfall)
    print("The list of rainfall: ", rainfalls);

    #The total rainfall for the week.
    sum_rainfall = np.sum(rainfalls)
    print(f"Total rainfall for the week: {sum_rainfall:.2f}mm")

    #The average rainfall for the week.
    mean_rainfall = np.mean(rainfalls)
    print(f"Average rainfall for the week: {mean_rainfall:.2f}mm")

    #Count how many days had no rain (0 mm).
    count_rainfall = np.sum(rainfalls == 0)
    print("There were had no rain for", count_rainfall, "days")

    #The days (by index) where the rainfall was more than 5 mm.
    index_rainfall = np.where(rainfalls > 5)
    print("Indices where the rainfall > 5 mm: ", index_rainfall[0])

    #Calculate the 75th percentile and identify values above it
    r75 = np.percentile(rainfalls, 75)
    print(f"The 75th percentile rainfall {r75:.2f}mm")

    values_rainfall = rainfalls[rainfalls > r75]
    print("Values above the 75th percentile:", values_rainfall)

if __name__ == "__main__":
    ans = rainfall_analysis()

