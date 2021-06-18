import review_classifier_service
from review_classifier_service import ReviewClassifierService
import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

def mlmodel():
  service = ReviewClassifierService()

  #Fetching Reviews from Hotelreview.csv and passing it to classification
  #import csv
  result=list()
  fresult=list()
  with open('Hotelreview_testingData.csv', newline='') as csvfile:
    data = csv.DictReader(csvfile)
    for row in data:
      result.append(row['Reviews'])

  for i in range(len(result)):
      reviews=result[i]
      fresult.append(service.classify(reviews))

  zipped = fresult
  #*********************************  OUTPUT Stored in out.csv *******************************************************************8
  indata = pd.read_csv('Hotelreview_testingData.csv')
  zipped = pd.DataFrame(fresult)
  #axis=1 indicates to concat the frames column wise
  outdata = pd.concat([indata, zipped], axis=1)
  #we dont want headers and dont want the row labels

  outdata.to_csv('out.csv', header=False, index=False)
  foutput=pd.read_csv("out.csv",sep=",",names=["ReviewID","Review", "Hotel", "City","UserName","Polarity"])
  #print(foutput)
  foutput.to_csv('out.csv', index=False)



  #*********************************** Specifying Header **************************************************
  df = pd.read_csv('out.csv')
  #df.drop(df.columns[[2]], axis = 1, inplace = True)
  header=["ReviewID","Reviews",'Hotel',"City","UserName","Polarity"]
  df.columns=header
  #print(df)
  #*********************************************************************************************************

  #****************************** Plotting Graph ***************************************
  a=df.groupby(["City", "Hotel","Polarity"], as_index=False)["Reviews"].count()

  City=list(a['City'])
  Hotel=list(a['Hotel'])
  Polarity=list(a['Polarity'])
  Reviews=list(a['Reviews'])

  Cities=set(City)
  #************************************************* Pune  *********************************************************
  def puneGraph():
    l1=list()
    l11=list()
    h1=list()
    h11=list()
    for j in range(len(a['Hotel'])):
      if City[j]=="Pune":
        if Polarity[j]==0:
          l1.append(Reviews[j])
          l11.append(Hotel[j])
        elif Polarity[j]==1:
          h1.append(Reviews[j])
          h11.append(Hotel[j])
          
    print("\n\n Pune \n")
    print("\nCount of Negative Review for each hotel")
    print(l1)
    print(l11)
    print("\nCount of Positive Review for each hotel")
    print(h1)
    print(h11)
    barWidth = 0.25

    # Set position of bar on X axis
    p1 = np.arange(len(l1))
    p2 = [x + barWidth for x in p1]
    # Make the plot
    p1=plt.bar(p1, l1, color='#7f6d5f', width=barWidth, edgecolor='white', label='Negative')
    p2=plt.bar(p2, h1, color='#557f2d', width=barWidth, edgecolor='white', label='Positive')
    # Add xticks on the middle of the group bars
    plt.xlabel('Hotels', fontweight='bold')
    plt.ylabel('Review Count', fontweight='bold')
    plt.title("Hotels in Pune")
    plt.xticks([r + barWidth for r in range(len(l1))], l11)

    # Create legend & Show graphic
    plt.legend(handles=[p1, p2],loc='upper right')
    plt.savefig('static/images/Punegraph.jpg')
    plt.clf()
    #plt.show()

  def mumbaiGraph():
  #*******************************************  Mumbai ********************************************************
    l2=list()
    l12=list()
    h2=list()
    h12=list()

    for j in range(len(a['Hotel'])):
      if City[j]=="Mumbai":
        if Polarity[j]==0:
          l2.append(Reviews[j])
          l12.append(Hotel[j])
        elif Polarity[j]==1:
          h2.append(Reviews[j])
          h12.append(Hotel[j])
    # set width of bar
    barWidth = 0.25

    print("\n\n Mumbai \n")
    print("\nCount of Negative Review for each hotel")
    print(l2)
    print(l12)
    print("\nCount of Positive Review for each hotel")
    print(h2)
    print(h12)

    # Set position of bar on X axis
    m1 = np.arange(len(l2))
    m2 = [x + barWidth for x in m1]
    # Make the plot
    p1=plt.bar(m1, l2, color='#7f6d5f', width=barWidth, edgecolor='white', label='Negative')
    p2=plt.bar(m2, h2, color='#557f2d', width=barWidth, edgecolor='white', label='Positive')
    # Add xticks on the middle of the group bars
    plt.xlabel('Hotels', fontweight='bold')
    plt.ylabel('Review Count', fontweight='bold')
    plt.title("Hotels in Mumbai")
    plt.xticks([r + barWidth for r in range(len(l2))], l12)

    # Create legend & Show graphic
    plt.legend(handles=[p1, p2],loc='upper right')
    plt.savefig('static/images/Mumbai.jpg')
    plt.clf()
    #plt.show()

  #************************************************* Kolkatta ********************************************************
  def kolkattaGraph():
    l3=list()
    l13=list()
    h3=list()
    h13=list()

    for j in range(len(a['Hotel'])):
      if City[j]=="Kolkata":
        if Polarity[j]==0:
          l3.append(Reviews[j])
          l13.append(Hotel[j])
        elif Polarity[j]==1:
          h3.append(Reviews[j])
          h13.append(Hotel[j])
    # set width of bar
    print("\n\n Kolkata \n")
    print("\nCount of Negative Review for each hotel")
    print(l3)
    print(l13)
    print("\nCount of Positive Review for each hotel")
    print(h3)
    print(h13)

    barWidth = 0.25

    # Set position of bar on X axis
    k1 = np.arange(len(l3))
    k2 = [x + barWidth for x in k1]
    # Make the plot
    p1=plt.bar(k1, l3, color='#7f6d5f', width=barWidth, edgecolor='white', label='Negative')
    p2=plt.bar(k2, h3, color='#557f2d', width=barWidth, edgecolor='white', label='Positive')
    # Add xticks on the middle of the group bars
    plt.xlabel('Hotels', fontweight='bold')
    plt.ylabel('Review Count', fontweight='bold')
    plt.title("Hotels in Kolkata")
    plt.xticks([r + barWidth for r in range(len(l3))], l13)

    # Create legend & Show graphic
    plt.legend(handles=[p1, p2],loc='upper right')
    plt.savefig('static/images/Kolkata.jpg')
    plt.clf()
    #plt.show()


  #************************************************** Banglore ******************************************************
  def bangloreGraph():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    l4=list()
    l14=list()
    h4=list()
    h14=list()

    for j in range(len(a['Hotel'])):
      if City[j]=="Bangalore":
        if Polarity[j]==0:
          l4.append(Reviews[j])
          l14.append(Hotel[j])
        elif Polarity[j]==1:
          h4.append(Reviews[j])
          h14.append(Hotel[j])

    print("\n\n Bangalore \n")
    print("\nCount of Negative Review for each hotel")
    print(l4)
    print(l14)
    print("\nCount of Positive Review for each hotel")
    print(h4)
    print(h14)

    # set width of bar
    barWidth = 0.25

    # Set position of bar on X axis
    b1 = np.arange(len(l4))
    b2 = [x + barWidth for x in b1]
    # Make the plot
    p1=plt.bar(b1, l4, color='#7f6d5f', width=barWidth, edgecolor='white', label='Negative')
    p2=plt.bar(b2, h4, color='#557f2d', width=barWidth, edgecolor='white', label='Positive')
    # Add xticks on the middle of the group bars
    plt.xlabel('Hotels', fontweight='bold')
    plt.ylabel('Review Count', fontweight='bold')
    plt.title("Hotels in Bangalore")
    plt.xticks([r + barWidth for r in range(len(l4))], l14)

    # Create legend & Show graphic
    plt.legend(handles=[p1, p2],loc='upper right')
  #  axis.plot(b1,b2)
    #return fig
    plt.savefig('static/images/Bangalore.jpg')
    plt.clf()
    #plt.show()
    print("\n")

  puneGraph()
  mumbaiGraph()
  kolkattaGraph()
  bangloreGraph()

