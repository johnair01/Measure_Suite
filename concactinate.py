import os
import glob
import pandas

def concatenate (indir='C:\\Users\\Temp account\\OneDrive\\PhD_Research\\Silicon_FET\\Raman\\20171230', outfile= 'C:\\Users\\Temp account\\OneDrive\\PhD_Research\\Silicon_FET\\Raman\\20171230\\RamanComb.csv'):
	os.chdir(indir)
	fileList=glob.glob("*.txt")
	
	fnList=[]
	dfList=[]
	
	for filename in fileList:
		print(filename)
		nms=os.path.splitext(filename)[0]
		fnList.append(nms)
		df= pandas.read_table(filename,usecols=[1])
		df.rename(columns={1: nms}, inplace=True)
		dfList.append(df)
	concatDf =pandas.concat(dfList,axis=1)
	concatDf.to_csv(outfile,index=None)

concatenate()