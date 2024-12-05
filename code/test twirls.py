import full_twirling_set

def main():
    # Define your error model
    error_model = {
        "11": {"XX": 0.1},
        "10": {"XI": 0.3},
        "01": {"IZ": 0.2}
    }
    
    # Call the wrapper function
    results = full_twirling_set.twirl(error_model)
    
    # Display the results
    print("Twirling Results:")
    for pauli_error, probability in results.items():
        print(f"{pauli_error}: {probability:.6f}")

if __name__ == "__main__":
    main()    

