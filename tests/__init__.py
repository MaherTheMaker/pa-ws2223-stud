import h5py
import pandas as pd
from matplotlib import pyplot as plt

with h5py.File("D:\Desktop\WORK\Fatemah\PA3\pa-ws2223-stud\Data\data_230209_GdD_PA3_Datensatz_Kennfeldmessung_Exzenterschneckenpumpe.hdf5", "r") as f:
    # get the keys of the file
    keys = list(f.keys())
    print(keys)

    # get the first key
    key = keys[0]

    for k in keys:
     print(f[k])
    # get the data of the first key
    data = f[key]
    print(data)

    # create a pandas dataframe
    df = pd.DataFrame(data)
    # print(df)
# print(len(df))
# for f in df[0]:
#    for d in df[0][f]:
#        print(d)

# # plot the data
# plt.plot(df["cyan_pumpe_char_laenge"], df["cyan_pumpe_char_laenge"])
# plt.xlabel("Volumenstrom (Q)")
# plt.ylabel("Druckdifferenz (∆p)")
# plt.title("Kennlinie")
# plt.show()

# function to plot the data for each key
def plot_data(key, f):
    data = f[key]
    df = pd.DataFrame(data)

    plt.plot(df["cyan_q"], df["cyan_dp"])
    plt.xlabel("Volumenstrom (Q)")
    plt.ylabel("Druckdifferenz (∆p)")
    plt.title("Kennlinie für " + key)
    plt.show()

# # plot the data for each key
# for key in keys:
#     plot_data(key, f)