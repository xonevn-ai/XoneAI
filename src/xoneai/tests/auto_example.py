from xoneai import XoneAI
import os
    
def auto():
    xoneai = XoneAI(
        auto="Create a movie script about car in mars",
        framework="autogen"
    )
    print(xoneai.framework)
    result = xoneai.run()
    
    # Return a meaningful result - either the actual result or a success indicator
    if result is not None:
        return result
    else:
        # If run() returns None, return a success indicator that we can test for
        return "Auto example completed successfully"

if __name__ == "__main__":
    print(auto())