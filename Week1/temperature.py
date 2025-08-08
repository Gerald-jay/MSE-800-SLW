def calculate_temperature():
    import numpy as np
    temperatures = np.array([18.5, 19, 20, 25.0, 2, 30, 13.9])

    average_temperature = np.mean(temperatures)
    print(f"average temperature: {average_temperature:.2f}°C")
    
    max_temperature = np.max(temperatures)
    print("max temperature: ", max_temperature)

    min_temperature = np.min(temperatures)
    print("min temperature: ", min_temperature)

    #Formula: F = C × 9/5 + 32
    temperatures_f = temperatures * 9/5 + 32
    print("temperatures_f data:", temperatures_f)

    #temperature > 20°C
    condition = temperatures > 20
    indices = np.where(condition)
    print("Indices where temperature > 20: ", indices[0])
    
if __name__ == "__main__":
    ans = calculate_temperature()