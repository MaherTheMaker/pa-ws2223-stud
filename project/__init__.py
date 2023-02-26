from project.functions import *

deg=["deg16.5","deg18","deg24"]
sp=[300,1260,1400]
x=gen_path_for_multi_speeds(1,deg,sp)
print(x)
filename="D:\Desktop\WORK\Fatemah\PA3\pa-ws2223-stud\Data\data_230209_GdD_PA3_Datensatz_Kennfeldmessung_Exzenterschneckenpumpe.hdf5"
df=get_df(filename,x[0])
xx=df["block0_values"]

i=0
# for f in xx:
#
#     print(i)
#     i+=1
#     print(f)

att=read_dataframe_metadata(filename,x[0],"deg")
print(att)