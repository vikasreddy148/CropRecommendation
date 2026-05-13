import pandas as pd
import io

data = """N,P,K,temperature,humidity,ph,rainfall,label
90,42,43,20.87974371,82.00274423,6.502985292000001,202.9355362,rice
85,58,41,21.77046169,80.31964408,7.038096361,226.6555374,rice
60,55,44,23.00445915,82.3207629,7.840207144,263.9642476,rice
74,35,40,26.49109635,80.15836264,6.980400905,242.8640342,rice
78,42,42,20.13017482,81.60487287,7.628472891,262.7173405,rice
...
""" # The rest of the data will be added in the real script

# Since I can't easily paste such a large block here without risking truncation or errors, 
# I will read the data from a file after I write the user's content to a file.
