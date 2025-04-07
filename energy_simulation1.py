import random
import datetime
import matplotlib.pyplot as plt
import csv

def simulate_occupancy(hour):
    if 8 <= hour <= 18:
        return random.uniform(0.4, 1.0)
    else:
        return random.uniform(0.0, 0.2)

def get_weather_forecast():
    return random.uniform(24, 35)

def get_historical_energy_usage(hour):
    base = 100
    if 8 <= hour <= 18:
        return base + random.uniform(50, 100)
    else:
        return base + random.uniform(0, 30)

def optimize_hvac(occupancy, temperature, historical_usage):
    efficiency_factor = 1.0
    if occupancy < 0.3:
        efficiency_factor *= 0.7
    if temperature < 26:
        efficiency_factor *= 0.9
    elif temperature > 30:
        efficiency_factor *= 1.1

    return historical_usage * efficiency_factor

def run_simulation():
    total_energy_saved = 0
    total_cost_saved = 0
    cost_per_kwh = 0.2

    hours = list(range(24))
    occupancies = []
    temperatures = []
    historical_usages = []
    optimized_usages = []
    energy_savings = []

    with open("energy_data.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Hour", "Occupancy", "Temperature (°C)", "Historical (kWh)", "Optimized (kWh)", "Energy Saved (kWh)"])

        print("Hour | Occupancy | Temp (°C) | Historical (kWh) | Optimized (kWh)")
        for hour in hours:
            occupancy = simulate_occupancy(hour)
            temp = get_weather_forecast()
            historical_usage = get_historical_energy_usage(hour)
            optimized_usage = optimize_hvac(occupancy, temp, historical_usage)

            energy_saved = historical_usage - optimized_usage
            cost_saved = energy_saved * cost_per_kwh

            total_energy_saved += energy_saved
            total_cost_saved += cost_saved

            occupancies.append(occupancy)
            temperatures.append(temp)
            historical_usages.append(historical_usage)
            optimized_usages.append(optimized_usage)
            energy_savings.append(energy_saved)

            print(f"{hour:>4} | {occupancy:.2f}      | {temp:.1f}       | {historical_usage:.1f}            | {optimized_usage:.1f}")
            writer.writerow([hour, f"{occupancy:.2f}", f"{temp:.1f}", f"{historical_usage:.1f}", f"{optimized_usage:.1f}", f"{energy_saved:.2f}"])

    print(f"\nTotal Energy Saved: {total_energy_saved:.2f} kWh")
    print(f"Total Cost Saved: ${total_cost_saved:.2f}")

    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.plot(hours, historical_usages, label='Historical Usage', marker='o')
    plt.plot(hours, optimized_usages, label='Optimized Usage', marker='o')
    plt.title('Energy Usage (kWh)')
    plt.xlabel('Hour')
    plt.ylabel('kWh')
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 3, 2)
    plt.plot(hours, occupancies, label='Occupancy Level', color='green', marker='s')
    plt.plot(hours, temperatures, label='Temperature (°C)', color='red', marker='^')
    plt.title('Occupancy & Temperature')
    plt.xlabel('Hour')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 3, 3)
    plt.bar(hours, energy_savings, color='blue')
    plt.title('Hourly Energy Savings')
    plt.xlabel('Hour')
    plt.ylabel('kWh Saved')
    plt.grid(axis='y')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_simulation()
