import numpy as np
import matplotlib.pyplot as plt

def calculate_pr_eos(temperatures_K, molar_volumes):
    """
    Calculates the pressure of CO2 using the Peng-Robinson Equation of State.

    Args:
        temperatures_K (np.ndarray): An array of temperatures in Kelvin.
        molar_volumes (np.ndarray): An array of molar volumes in m^3/mol.

    Returns:
        np.ndarray: A 2D array of pressures in Pascals. Each row corresponds
                    to a temperature, and each column to a molar volume.
    """
    # --- CO2 Physical Constants ---
    Tc = 304.2     # Critical Temperature (K)
    Pc = 7.377e6   # Critical Pressure (Pa)
    w = 0.228      # Acentric factor
    R = 8.314      # Universal Gas Constant (J/(mol*K))

    # --- Peng-Robinson EOS Constants ---
    Psi = 0.45724
    Omega = 0.07780
    K = 0.37464 + 1.54226 * w - 0.26992 * w**2

    # --- Intermediate Calculations ---
    # The 'b' parameter is constant
    b = Omega * R * Tc / Pc

    # The 'a' parameter is temperature-dependent
    Tr = temperatures_K / Tc
    # Reshape Tr to allow for broadcasting with the 1D molar_volumes array
    Tr = Tr.reshape(-1, 1)
    
    alpha = (1 + K * (1 - np.sqrt(Tr)))**2
    a = Psi * alpha * (R**2 * Tc**2) / Pc

    # --- Peng-Robinson Equation of State ---
    # This is the vectorized calculation. No loops needed!
    pressure_Pa = (R * temperatures_K.reshape(-1, 1)) / (molar_volumes - b) - \
                  a / (molar_volumes * (molar_volumes + b) + b * (molar_volumes - b))
                  
    return pressure_Pa

def main():
    """
    Main function to run the EOS calculation and generate the plot.
    """
    # --- System Information ---
    molar_mass_co2 = 0.044  # kg/mol
    
    # Define the range of densities and temperatures to analyze
    densities_kg_m3 = np.linspace(50, 1000, 50) # Avoid rho=0 to prevent division by zero
    temperatures_K = np.array([295, 325, 345, 375])

    # Convert density to molar volume (v = M/rho)
    molar_volumes_m3_mol = molar_mass_co2 / densities_kg_m3

    # --- Calculation ---
    pressure_Pa = calculate_pr_eos(temperatures_K, molar_volumes_m3_mol)
    
    # Convert Pascals to MegaPascals for plotting
    pressure_MPa = pressure_Pa / 1e6

    # --- Plotting ---
    plt.figure(figsize=(10, 7))
    
    # Plot a line for each temperature
    for i, T in enumerate(temperatures_K):
        plt.plot(densities_kg_m3, pressure_MPa[i, :], marker='o', linestyle='-', label=f'{T} K')

    # Add plot details for a professional look
    plt.title('CO2 Pressure vs. Density (Peng-Robinson EOS)')
    plt.xlabel('Density (kg/m³)')
    plt.ylabel('Pressure (MPa)')
    plt.legend()
    plt.grid(True)
    plt.ylim(bottom=0) # Pressure cannot be negative
    
    # Save the figure and show it
    plt.savefig('co2_eos_plot.png', dpi=300)
    print("Plot saved as co2_eos_plot.png")
    plt.show()


if __name__ == "__main__":
    main()