# importing flask modules
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import csv
import mlmodel
import Fake_review_5_Algos
import pandas as pd
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import flash

from flask import request
from flask import jsonify
from datetime import date, datetime

# ************************************************************************************************

pw = '52Pr@n@li'

# initializing a variable of Flask
app = Flask(__name__)
# app = Flask(__name__, static_url_path='/static')
app.secret_key = 'frd'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = pw
app.config['MYSQL_DB'] = 'beproject'

mysql = MySQL(app)


# decorating index function with the app.route with url as /login


@app.route('/')
def home():
    return render_template('HomePage.html')


@app.route('/dashboard.html', methods=["GET", "POST"])
def dashboard():
    conn = MySQLdb.connect("localhost", "root", pw, "beproject")
    cur = conn.cursor()
    cur.execute('select * from user_registered')
    data = cur.fetchall()  # data from user_registered database
    cur.execute('select * from book_room')
    data1 = cur.fetchall()  # data from book_room database
    cur.execute('select * from book_table')
    data2 = cur.fetchall()  # data from book_table database

    df1 = pd.read_csv('out.csv')
    header1 = ["ReviewID", "Reviews", 'Hotel', "City", "UserName", "Polarity"]
    df1.columns = header1
    a = df1.groupby(["City", "Hotel", "Polarity"], as_index=False)["Reviews"].count()

    City = list(a['City'])
    Hotel = list(a['Hotel'])
    Polarity = list(a['Polarity'])
    ReviewsCNT = list(a['Reviews'])
    # for deceptive reviews

    df = pd.read_csv(r'fake_review_out.csv')
    header = ["ReviewID", "Reviews", 'Hotel', "City", "UserName", "NB", "SVC", "SGD", "LR", "DT", "Output"]
    df.columns = header
    FCity = list(df['City'])
    FHotel = list(df['Hotel'])
    FinalOutput = list(df['Output'])
    Reviews = list(df['Reviews'])
    DBuser = list(df['UserName'])
    ReviewID= list(df['ReviewID'])

    puneReviews = list()
    puneHotels = list()
    MumbaiReviews = list()
    MumbaiHotels = list()
    BangloreReviews = list()
    BangloreHotels = list()
    KolkataReviews = list()
    KolkataHotels = list()
    Puneuser = list()
    Mumbaiuser = list()
    Kolkatauser = list()
    Bangloreuser = list()

    puneID = list()
    mumbaiID= list()
    kolkataID= list()
    bangaloreID= list()

    # print(City)
    for j in range(1, len(df)):
        if FCity[j] == "Pune":
            if FinalOutput[j] == 0:
                puneReviews.append(Reviews[j])
                puneHotels.append(FHotel[j])
                Puneuser.append(DBuser[j])
                puneID.append(ReviewID[j])
                # print("pune ",Reviews[j])
            # print("pune ",FinalOutput[j],'j=',j)
    for j in range(1, len(df)):
        if FCity[j] == "Mumbai":
            if FinalOutput[j] == 0:
                MumbaiReviews.append(Reviews[j])
                MumbaiHotels.append(FHotel[j])
                Mumbaiuser.append(DBuser[j])
                mumbaiID.append(ReviewID[j])
                # print("mumbai ",Reviews[j])
    for j in range(1, len(df)):
        if FCity[j] == "Bangalore":
            if FinalOutput[j] == 0:
                BangloreReviews.append(Reviews[j])
                BangloreHotels.append(FHotel[j])
                Bangloreuser.append(DBuser[j])
                bangaloreID.append(ReviewID[j])
                # print("Banglore ",Reviews[j])
    for j in range(1, len(df)):
        if FCity[j] == "Kolkata":
            if FinalOutput[j] == 0:
                KolkataReviews.append(Reviews[j])
                KolkataHotels.append(FHotel[j])
                Kolkatauser.append(DBuser[j])
                kolkataID.append(ReviewID[j])
                # print("Kolkata",Reviews[j])

    Cities = set(City)
    l1 = list()
    l11 = list()
    h1 = list()
    h11 = list()
    for j in range(len(a['Hotel'])):
        if City[j] == "Pune":
            if Polarity[j] == 0:
                l1.append(ReviewsCNT[j])
                l11.append(Hotel[j])
            elif Polarity[j] == 1:
                h1.append(ReviewsCNT[j])
                h11.append(Hotel[j])

    l2 = list()
    l12 = list()
    h2 = list()
    h12 = list()

    for j in range(len(a['Hotel'])):
        if City[j] == "Mumbai":
            if Polarity[j] == 0:
                l2.append(ReviewsCNT[j])
                l12.append(Hotel[j])
            elif Polarity[j] == 1:
                h2.append(ReviewsCNT[j])
                h12.append(Hotel[j])

    l3 = list()
    l13 = list()
    h3 = list()
    h13 = list()

    for j in range(len(a['Hotel'])):
        if City[j] == "Kolkata":
            if Polarity[j] == 0:
                l3.append(ReviewsCNT[j])
                l13.append(Hotel[j])
            elif Polarity[j] == 1:
                h3.append(ReviewsCNT[j])
                h13.append(Hotel[j])

    l4 = list()
    l14 = list()
    h4 = list()
    h14 = list()

    for j in range(len(a['Hotel'])):
        if City[j] == "Bangalore":
            if Polarity[j] == 0:
                l4.append(ReviewsCNT[j])
                l14.append(Hotel[j])
            elif Polarity[j] == 1:
                h4.append(ReviewsCNT[j])
                h14.append(Hotel[j])

    PN_Pune_Df = pd.DataFrame({'Hotels': l11, 'Positive Review Count': h1, 'Negative Review Count': l1}).set_index(
        'Hotels')
    PN_Mumbai_Df = pd.DataFrame({'Hotels': l12, 'Positive Review Count': h2, 'Negative Review Count': l2}).set_index(
        'Hotels')
    PN_Kolkata_Df = pd.DataFrame({'Hotels': l13, 'Positive Review Count': h3, 'Negative Review Count': l3}).set_index(
        'Hotels')
    PN_Bangalore_Df = pd.DataFrame({'Hotels': l14, 'Positive Review Count': h4, 'Negative Review Count': l4}).set_index(
        'Hotels')

    '''
    Pune_Df = pd.DataFrame({'User':Puneuser,'Hotels': puneHotels, 'Deceptive Reviews': puneReviews})
    Mumbai_Df = pd.DataFrame({'User':Mumbaiuser,'Hotels': MumbaiHotels, 'Deceptive Reviews': MumbaiReviews})
    Kolkata_Df = pd.DataFrame({'User':Kolkatauser,'Hotels': KolkataHotels, 'Deceptive Reviews': KolkataReviews})
    Bangalore_Df = pd.DataFrame({ 'User':Bangloreuser,'Hotels': BangloreHotels,'Deceptive Reviews': BangloreReviews})
    '''

    cur.execute(
        'SELECT ip_address, GROUP_CONCAT(DISTINCT user) FROM review GROUP BY ip_address HAVING COUNT(DISTINCT user) > 2 ORDER BY COUNT(DISTINCT user) DESC;')
    ip = cur.fetchall()

    cur.execute('SELECT *FROM SUSPICIOUS_REVIEWS;')
    datemodule = cur.fetchall()

    return render_template("dashboard.html", value=data, value1=data1, value2=data2, value3=PN_Pune_Df,
                           value4=PN_Mumbai_Df, value5=PN_Kolkata_Df, value6=PN_Bangalore_Df, value7=ip,
                           value8=datemodule, value9=Puneuser, value10=puneHotels, value11=puneReviews,
                           value12=Mumbaiuser, value13=MumbaiHotels, value14=MumbaiReviews, value15=Kolkatauser,
                           value16=KolkataHotels, value17=KolkataReviews, value18=Bangloreuser, value19=BangloreHotels,
                           value20=BangloreReviews, value21=len(Puneuser), value22=len(Mumbaiuser),
                           value23=len(Kolkatauser), value24=len(Bangloreuser),value25=puneID,value26=mumbaiID,value27=kolkataID,value28=bangaloreID)


# ****************************************************  PUNE ************************************************8
@app.route("/submitOrchidP", methods=["GET", "POST"])
def submitOrchidP():
    if request.method == "GET":
        return redirect(url_for('index.html'))
    elif (request.method == "POST"):
        reviewdata = dict(request.form)
        review = reviewdata["Review"]
        city = 'Pune'
        hotel = 'Orchid'
        name = reviewdata["Username"]
        reviewtype = reviewdata["Reviewtype"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM user_registered WHERE Username like %s', [name])
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            ip = request.remote_addr
            today = date.today()
            cursor.execute(
                'INSERT INTO review(user,hotel,city,reviews,ip_address,today,reviewtype) VALUES (% s, % s, % s, %s, %s, %s, %s)',
                (name, hotel, city, review, ip, today, reviewtype))
            mysql.connection.commit()

            cursor.execute(
                'SELECT review_id  FROM review WHERE user like %s and hotel like %s and city like %s order by review_id desc',
                [name, hotel, city])
            row = cursor.fetchone()
            reviewID = row['review_id']  # string id
            ID = str(reviewID)  # int ID
            with open('Hotelreview_testingData.csv', mode='a') as csv_file:
                data = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data.writerow([ID, review, hotel, city, name])
            hotelsInPune()

            if reviewtype == 'Room':
                cursor.execute(
                    'SELECT checkInDate  FROM book_room WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                ch = cursor.fetchone()
                if ch == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s,% s, % s, % s, %s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:
                    checkin = ch['checkInDate']
                    print(checkin)
                    checkin1 = datetime.strptime(checkin, '%Y-%m-%d').date()

                    if checkin1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s,%s, % s, %s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()


            elif reviewtype == 'Table':
                cursor.execute(
                    'SELECT date  FROM book_table WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                da = cursor.fetchone()
                print("In Orchid Table")
                print(da)
                if da == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s,% s, % s, %s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:
                    datec = da['date']
                    date1 = datetime.strptime(datec, '%Y-%m-%d').date()
                    if date1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s,% s, % s, % s, %s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()

        else:
            return render_template('alertpune.html')
    return render_template('hotelsInPune.html')


@app.route("/submitNovotelP", methods=["GET", "POST"])
def submitNovotelP():
    if request.method == "GET":
        return redirect(url_for('index.html'))
    elif (request.method == "POST"):
        reviewdata = dict(request.form)
        review = reviewdata["Review"]
        city = 'Pune'
        hotel = 'Novotel'
        name = reviewdata["Username"]
        reviewtype = reviewdata["Reviewtype"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM user_registered WHERE Username like % s', [name])
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            ip = request.remote_addr
            today = date.today()
            cursor.execute(
                'INSERT INTO review(user,hotel,city,reviews,ip_address,today,reviewtype) VALUES (% s, % s, % s, %s, %s, %s, %s)',
                (name, hotel, city, review, ip, today, reviewtype))
            mysql.connection.commit()
            cursor.execute(
                'SELECT review_id  FROM review WHERE user like %s and hotel like %s and city like %s order by review_id desc',
                [name, hotel, city])
            row = cursor.fetchone()
            reviewID = row['review_id']  # string id
            ID = str(reviewID)  # int ID
            with open('Hotelreview_testingData.csv', mode='a') as csv_file:
                data = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data.writerow([ID, review, hotel, city, name])

            if reviewtype == 'Room':
                cursor.execute(
                    'SELECT checkInDate  FROM book_room WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                ch = cursor.fetchone()
                if ch == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s,% s, %s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    checkin = ch['checkInDate']
                    print(checkin)
                    checkin1 = datetime.strptime(checkin, '%Y-%m-%d').date()

                    if checkin1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s,% s, % s, % s, %s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()


            elif reviewtype == 'Table':
                cursor.execute(
                    'SELECT date  FROM book_table WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                da = cursor.fetchone()
                if da == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s,% s, % s, % s, %s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    datec = da['date']
                    date1 = datetime.strptime(datec, '%Y-%m-%d').date()
                    if date1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s,% s, % s, % s, %s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()

            return render_template('hotelsInPune.html')
        else:
            return render_template('alertpune.html')
    return render_template('hotelsInPune.html')


@app.route("/submitConradP", methods=["GET", "POST"])
def submitConradP():
    if request.method == "GET":
        return redirect(url_for('index.html'))
    elif (request.method == "POST"):
        reviewdata = dict(request.form)
        review = reviewdata["Review"]
        city = 'Pune'
        hotel = 'Conrad'
        name = reviewdata["Username"]
        reviewtype = reviewdata["Reviewtype"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_registered WHERE Username like % s', [name])
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            ip = request.remote_addr
            today = date.today()
            cursor.execute(
                'INSERT INTO review(user,hotel,city,reviews,ip_address,today,reviewtype) VALUES (% s, % s, % s, %s, %s, %s, %s)',
                (name, hotel, city, review, ip, today, reviewtype))
            mysql.connection.commit()

            cursor.execute(
                'SELECT review_id  FROM review WHERE user like %s and hotel like %s and city like %s order by review_id desc',
                [name, hotel, city])
            row = cursor.fetchone()
            reviewID = row['review_id']  # string id
            ID = str(reviewID)  # int ID
            with open('Hotelreview_testingData.csv', mode='a') as csv_file:
                data = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data.writerow([ID, review, hotel, city, name])

            if reviewtype == 'Room':
                cursor.execute(
                    'SELECT checkInDate  FROM book_room WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                ch = cursor.fetchone()
                if ch == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s,% s, % s, % s, %s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    checkin = ch['checkInDate']
                    print(checkin)
                    checkin1 = datetime.strptime(checkin, '%Y-%m-%d').date()

                    if checkin1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s,% s, % s, % s, %s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()


            elif reviewtype == 'Table':
                cursor.execute(
                    'SELECT date  FROM book_table WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                da = cursor.fetchone()
                if da == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s,% s, % s, % s, %s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    datec = da['date']
                    date1 = datetime.strptime(datec, '%Y-%m-%d').date()
                    if date1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s,% s, % s, % s, %s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()

            return render_template('hotelsInPune.html')
        else:
            return render_template('alertpune.html')
    return render_template('hotelsInPune.html')


@app.route("/submitCourtyardP", methods=["GET", "POST"])
def submitCourtyardP():
    if request.method == "GET":
        return redirect(url_for('index.html'))
    elif (request.method == "POST"):
        reviewdata = dict(request.form)
        review = reviewdata["Review"]
        city = 'Pune'
        hotel = 'Courtyard'
        name = reviewdata["Username"]
        reviewtype = reviewdata["Reviewtype"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_registered WHERE Username like % s', [name])
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            ip = request.remote_addr
            today = date.today()
            cursor.execute(
                'INSERT INTO review(user,hotel,city,reviews,ip_address,today,reviewtype) VALUES (% s, % s, % s, %s, %s, %s, %s)',
                (name, hotel, city, review, ip, today, reviewtype))
            mysql.connection.commit()

            cursor.execute(
                'SELECT review_id  FROM review WHERE user like %s and hotel like %s and city like %s order by review_id desc',
                [name, hotel, city])
            row = cursor.fetchone()
            reviewID = row['review_id']  # string id
            ID = str(reviewID)  # int ID
            with open('Hotelreview_testingData.csv', mode='a') as csv_file:
                data = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data.writerow([ID, review, hotel, city, name])

            if reviewtype == 'Room':
                cursor.execute(
                    'SELECT checkInDate  FROM book_room WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                ch = cursor.fetchone()
                if ch == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s,% s, % s, %s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    checkin = ch['checkInDate']
                    print(checkin)
                    checkin1 = datetime.strptime(checkin, '%Y-%m-%d').date()

                    if checkin1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s,% s, % s, % s, %s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()


            elif reviewtype == 'Table':
                cursor.execute(
                    'SELECT date  FROM book_table WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                da = cursor.fetchone()
                if da == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s,% s, %s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    datec = da['date']
                    date1 = datetime.strptime(datec, '%Y-%m-%d').date()
                    if date1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s,% s, % s, %s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()

            return render_template('hotelsInPune.html')
        else:
            return render_template('alertpune.html')
    return render_template('hotelsInPune.html')


# ***************************************** MUMBAI  **********************************************

@app.route("/submitHiltonM", methods=["GET", "POST"])
def submitHiltonM():
    if request.method == "GET":
        return redirect(url_for('index.html'))
    elif (request.method == "POST"):
        reviewdata = dict(request.form)
        review = reviewdata["Review"]
        city = 'Mumbai'
        hotel = 'Hilton'

        name = reviewdata["Username"]
        reviewtype = reviewdata["Reviewtype"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_registered WHERE Username like % s', [name])
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            ip = request.remote_addr
            today = date.today()
            cursor.execute(
                'INSERT INTO review(user,hotel,city,reviews,ip_address,today,reviewtype) VALUES (% s, % s, % s, %s, %s, %s, %s)',
                (name, hotel, city, review, ip, today, reviewtype))
            mysql.connection.commit()

            cursor.execute(
                'SELECT review_id  FROM review WHERE user like %s and hotel like %s and city like %s order by review_id desc',
                [name, hotel, city])
            row = cursor.fetchone()
            reviewID = row['review_id']  # string id
            ID = str(reviewID)  # int ID
            with open('Hotelreview_testingData.csv', mode='a') as csv_file:
                data = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data.writerow([ID, review, hotel, city, name])

            if reviewtype == 'Room':
                cursor.execute(
                    'SELECT checkInDate  FROM book_room WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                ch = cursor.fetchone()
                if ch == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s,% s, %s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    checkin = ch['checkInDate']
                    print(checkin)
                    checkin1 = datetime.strptime(checkin, '%Y-%m-%d').date()

                    if checkin1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s,% s, %s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()


            elif reviewtype == 'Table':
                cursor.execute(
                    'SELECT date  FROM book_table WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                da = cursor.fetchone()
                if da == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s,% s, %s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    datec = da['date']
                    date1 = datetime.strptime(datec, '%Y-%m-%d').date()
                    if date1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s,% s, %s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()

            return render_template('hotelsInMumbai.html')
        else:
            return render_template('alertmumbai.html')
    return render_template('hotelsInMumbai.html')


@app.route("/submitTajM", methods=["GET", "POST"])
def submitTajM():
    if request.method == "GET":
        return redirect(url_for('index.html'))
    elif (request.method == "POST"):
        reviewdata = dict(request.form)
        review = reviewdata["Review"]
        city = 'Mumbai'
        hotel = 'Taj'
        name = reviewdata["Username"]
        reviewtype = reviewdata["Reviewtype"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_registered WHERE Username like % s', [name])
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            ip = request.remote_addr
            today = date.today()
            cursor.execute(
                'INSERT INTO review(user,hotel,city,reviews,ip_address,today,reviewtype) VALUES (% s, % s, % s, %s, %s, %s, %s)',
                (name, hotel, city, review, ip, today, reviewtype))
            mysql.connection.commit()

            cursor.execute(
                'SELECT review_id  FROM review WHERE user like %s and hotel like %s and city like %s order by review_id desc',
                [name, hotel, city])
            row = cursor.fetchone()
            reviewID = row['review_id']  # string id
            ID = str(reviewID)  # int ID
            with open('Hotelreview_testingData.csv', mode='a') as csv_file:
                data = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data.writerow([ID, review, hotel, city, name])

            if reviewtype == 'Room':
                cursor.execute(
                    'SELECT checkInDate  FROM book_room WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                ch = cursor.fetchone()
                if ch == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s, %s,% s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    checkin = ch['checkInDate']
                    print(checkin)
                    checkin1 = datetime.strptime(checkin, '%Y-%m-%d').date()

                    if checkin1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s,% s, %s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()


            elif reviewtype == 'Table':
                cursor.execute(
                    'SELECT date  FROM book_table WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                da = cursor.fetchone()
                if da == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s, %s,% s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    datec = da['date']
                    date1 = datetime.strptime(datec, '%Y-%m-%d').date()
                    if date1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s,% s, %s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()

            return render_template('hotelsInMumbai.html')
        else:
            return render_template('alertmumbai.html')
    return render_template('hotelsInMumbai.html')


@app.route("/submitITCM", methods=["GET", "POST"])
def submitITCM():
    if request.method == "GET":
        return redirect(url_for('index.html'))
    elif (request.method == "POST"):
        reviewdata = dict(request.form)
        review = reviewdata["Review"]
        city = 'Mumbai'
        hotel = 'ITC'

        name = reviewdata["Username"]
        reviewtype = reviewdata["Reviewtype"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_registered WHERE Username like % s', [name])
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            ip = request.remote_addr
            today = date.today()
            cursor.execute(
                'INSERT INTO review(user,hotel,city,reviews,ip_address,today,reviewtype) VALUES (% s, % s, % s, %s, %s, %s, %s)',
                (name, hotel, city, review, ip, today, reviewtype))
            mysql.connection.commit()

            cursor.execute(
                'SELECT review_id  FROM review WHERE user like %s and hotel like %s and city like %s order by review_id desc',
                [name, hotel, city])
            row = cursor.fetchone()
            reviewID = row['review_id']  # string id
            ID = str(reviewID)  # int ID
            with open('Hotelreview_testingData.csv', mode='a') as csv_file:
                data = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data.writerow([ID, review, hotel, city, name])

            if reviewtype == 'Room':
                cursor.execute(
                    'SELECT checkInDate  FROM book_room WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                ch = cursor.fetchone()
                if ch == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s, %s, %s,% s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    checkin = ch['checkInDate']
                    print(checkin)
                    checkin1 = datetime.strptime(checkin, '%Y-%m-%d').date()

                    if checkin1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s, %s, %s,% s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()


            elif reviewtype == 'Table':
                cursor.execute(
                    'SELECT date  FROM book_table WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                da = cursor.fetchone()
                if da == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s, %s, %s,% s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    datec = da['date']
                    date1 = datetime.strptime(datec, '%Y-%m-%d').date()
                    if date1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s, %s, %s,% s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()

            return render_template('hotelsInMumbai.html')
        else:
            return render_template('alertmumbai.html')
    return render_template('hotelsInMumbai.html')


@app.route("/submitMarathaM", methods=["GET", "POST"])
def submitMarathaM():
    if request.method == "GET":
        return redirect(url_for('index.html'))
    elif (request.method == "POST"):
        reviewdata = dict(request.form)
        review = reviewdata["Review"]
        city = 'Mumbai'
        hotel = 'Maratha'

        name = reviewdata["Username"]
        reviewtype = reviewdata["Reviewtype"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_registered WHERE Username like % s', [name])
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            ip = request.remote_addr
            today = date.today()
            cursor.execute(
                'INSERT INTO review(user,hotel,city,reviews,ip_address,today,reviewtype) VALUES (% s, % s, % s, %s, %s, %s, %s)',
                (name, hotel, city, review, ip, today, reviewtype))
            mysql.connection.commit()

            cursor.execute(
                'SELECT review_id  FROM review WHERE user like %s and hotel like %s and city like %s order by review_id desc',
                [name, hotel, city])
            row = cursor.fetchone()
            reviewID = row['review_id']  # string id
            ID = str(reviewID)  # int ID
            with open('Hotelreview_testingData.csv', mode='a') as csv_file:
                data = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data.writerow([ID, review, hotel, city, name])

            if reviewtype == 'Room':
                cursor.execute(
                    'SELECT checkInDate  FROM book_room WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                ch = cursor.fetchone()
                if ch == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s, %s, %s,% s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    checkin = ch['checkInDate']
                    print(checkin)
                    checkin1 = datetime.strptime(checkin, '%Y-%m-%d').date()

                    if checkin1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s, %s, %s,% s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()


            elif reviewtype == 'Table':
                cursor.execute(
                    'SELECT date  FROM book_table WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                da = cursor.fetchone()
                if da == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s, %s,% s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    datec = da['date']
                    date1 = datetime.strptime(datec, '%Y-%m-%d').date()
                    if date1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s, %s,% s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()

            return render_template('hotelsInMumbai.html')
        else:
            return render_template('alertmumbai.html')
    return render_template('hotelsInMumbai.html')


# **************************************** Kolkata***************************************************

@app.route("/submitITCK", methods=["GET", "POST"])
def submitITCK():
    if request.method == "GET":
        return redirect(url_for('index.html'))
    elif (request.method == "POST"):
        reviewdata = dict(request.form)
        review = reviewdata["Review"]
        city = 'Kolkata'
        hotel = 'ITC'

        name = reviewdata["Username"]
        reviewtype = reviewdata["Reviewtype"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_registered WHERE Username like % s', [name])
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            ip = request.remote_addr
            today = date.today()
            cursor.execute(
                'INSERT INTO review(user,hotel,city,reviews,ip_address,today,reviewtype) VALUES (% s, % s, % s, %s, %s, %s, %s)',
                (name, hotel, city, review, ip, today, reviewtype))
            mysql.connection.commit()

            cursor.execute(
                'SELECT review_id  FROM review WHERE user like %s and hotel like %s and city like %s order by review_id desc',
                [name, hotel, city])
            row = cursor.fetchone()
            reviewID = row['review_id']  # string id
            ID = str(reviewID)  # int ID
            with open('Hotelreview_testingData.csv', mode='a') as csv_file:
                data = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data.writerow([ID, review, hotel, city, name])

            if reviewtype == 'Room':
                cursor.execute(
                    'SELECT checkInDate  FROM book_room WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                ch = cursor.fetchone()
                if ch == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s,% s, %s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    checkin = ch['checkInDate']
                    print(checkin)
                    checkin1 = datetime.strptime(checkin, '%Y-%m-%d').date()

                    if checkin1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s,% s, %s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()


            elif reviewtype == 'Table':
                cursor.execute(
                    'SELECT date  FROM book_table WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                da = cursor.fetchone()
                if da == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s, %s,% s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    datec = da['date']
                    date1 = datetime.strptime(datec, '%Y-%m-%d').date()
                    if date1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s,% s, %s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()

            return render_template('hotelsInKolkata.html')
        else:
            return render_template('alertkolkata.html')
    return render_template('hotelsInKolkata.html')


@app.route("/submitOberoiK", methods=["GET", "POST"])
def submitOberoiK():
    if request.method == "GET":
        return redirect(url_for('index.html'))
    elif (request.method == "POST"):
        reviewdata = dict(request.form)
        review = reviewdata["Review"]
        city = 'Kolkata'
        hotel = 'Oberoi'

        name = reviewdata["Username"]
        reviewtype = reviewdata["Reviewtype"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_registered WHERE Username like % s', [name])
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            ip = request.remote_addr
            today = date.today()
            cursor.execute(
                'INSERT INTO review(user,hotel,city,reviews,ip_address,today,reviewtype) VALUES (% s, % s, % s, %s, %s, %s, %s)',
                (name, hotel, city, review, ip, today, reviewtype))
            mysql.connection.commit()

            cursor.execute(
                'SELECT review_id  FROM review WHERE user like %s and hotel like %s and city like %s order by review_id desc',
                [name, hotel, city])
            row = cursor.fetchone()
            reviewID = row['review_id']  # string id
            ID = str(reviewID)  # int ID
            with open('Hotelreview_testingData.csv', mode='a') as csv_file:
                data = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data.writerow([ID, review, hotel, city, name])

            if reviewtype == 'Room':
                cursor.execute(
                    'SELECT checkInDate  FROM book_room WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                ch = cursor.fetchone()
                if ch == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s,% s, % s, %s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    checkin = ch['checkInDate']
                    print(checkin)
                    checkin1 = datetime.strptime(checkin, '%Y-%m-%d').date()

                    if checkin1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s,% s, % s, % s, %s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()


            elif reviewtype == 'Table':
                cursor.execute(
                    'SELECT date  FROM book_table WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                da = cursor.fetchone()
                if da == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s,% s, % s, %s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    datec = da['date']
                    date1 = datetime.strptime(datec, '%Y-%m-%d').date()
                    if date1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s,% s, % s, % s, %s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()

            return render_template('hotelsInKolkata.html')
        else:
            return render_template('alertkolkata.html')
    return render_template('hotelsInKolkata.html')


@app.route("/submitTajK", methods=["GET", "POST"])
def submitTajK():
    if request.method == "GET":
        return redirect(url_for('index.html'))
    elif (request.method == "POST"):
        reviewdata = dict(request.form)
        review = reviewdata["Review"]
        city = 'Kolkata'
        hotel = 'Taj'

        name = reviewdata["Username"]
        reviewtype = reviewdata["Reviewtype"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_registered WHERE Username like % s', [name])
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            ip = request.remote_addr
            today = date.today()
            cursor.execute(
                'INSERT INTO review(user,hotel,city,reviews,ip_address,today,reviewtype) VALUES (% s, % s, % s, %s, %s, %s, %s)',
                (name, hotel, city, review, ip, today, reviewtype))
            mysql.connection.commit()

            cursor.execute(
                'SELECT review_id  FROM review WHERE user like %s and hotel like %s and city like %s order by review_id desc',
                [name, hotel, city])
            row = cursor.fetchone()
            reviewID = row['review_id']  # string id
            ID = str(reviewID)  # int ID
            with open('Hotelreview_testingData.csv', mode='a') as csv_file:
                data = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data.writerow([ID, review, hotel, city, name])

            if reviewtype == 'Room':
                cursor.execute(
                    'SELECT checkInDate  FROM book_room WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                ch = cursor.fetchone()
                if ch == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s,% s, % s, %s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    checkin = ch['checkInDate']
                    print(checkin)
                    checkin1 = datetime.strptime(checkin, '%Y-%m-%d').date()

                    if checkin1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s,% s, % s, %s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()


            elif reviewtype == 'Table':
                cursor.execute(
                    'SELECT date  FROM book_table WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                da = cursor.fetchone()
                if da == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s, %s,% s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    datec = da['date']
                    date1 = datetime.strptime(datec, '%Y-%m-%d').date()
                    if date1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s,% s, %s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()

            return render_template('hotelsInKolkata.html')
        else:
            return render_template('alertkolkata.html')
    return render_template('hotelsInKolkata.html')


@app.route("/submitMarriottK", methods=["GET", "POST"])
def submitMarriottK():
    if request.method == "GET":
        return redirect(url_for('index.html'))
    elif (request.method == "POST"):
        reviewdata = dict(request.form)
        review = reviewdata["Review"]
        city = 'Kolkata'
        hotel = 'Marriott'
        name = reviewdata["Username"]
        reviewtype = reviewdata["Reviewtype"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_registered WHERE Username like % s', [name])
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            ip = request.remote_addr
            today = date.today()
            cursor.execute(
                'INSERT INTO review(user,hotel,city,reviews,ip_address,today,reviewtype) VALUES (% s, % s, % s, %s, %s, %s, %s)',
                (name, hotel, city, review, ip, today, reviewtype))
            mysql.connection.commit()

            cursor.execute(
                'SELECT review_id  FROM review WHERE user like %s and hotel like %s and city like %s order by review_id desc',
                [name, hotel, city])
            row = cursor.fetchone()
            reviewID = row['review_id']  # string id
            ID = str(reviewID)  # int ID
            with open('Hotelreview_testingData.csv', mode='a') as csv_file:
                data = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data.writerow([ID, review, hotel, city, name])
            if reviewtype == 'Room':
                cursor.execute(
                    'SELECT checkInDate  FROM book_room WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                ch = cursor.fetchone()
                if ch == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s,% s, %s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    checkin = ch['checkInDate']
                    print(checkin)
                    checkin1 = datetime.strptime(checkin, '%Y-%m-%d').date()

                    if checkin1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s,% s, %s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()


            elif reviewtype == 'Table':
                cursor.execute(
                    'SELECT date  FROM book_table WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                da = cursor.fetchone()
                if da == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s,% s, %s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    datec = da['date']
                    date1 = datetime.strptime(datec, '%Y-%m-%d').date()
                    if date1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s,% s, %s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()

            return render_template('hotelsInKolkata.html')
        else:
            return render_template('alertkolkata.html')
    return render_template('hotelsInKolkata.html')


# **************************************** Bangalore***************************************************

@app.route("/submitWelcomHotelB", methods=["GET", "POST"])
def submitWelcomHotelB():
    if request.method == "GET":
        return redirect(url_for('index.html'))
    elif (request.method == "POST"):
        reviewdata = dict(request.form)
        review = reviewdata["Review"]
        city = 'Bangalore'
        hotel = 'WelcomHotel'

        name = reviewdata["Username"]
        reviewtype = reviewdata["Reviewtype"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_registered WHERE Username like % s', [name])
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            ip = request.remote_addr
            today = date.today()
            cursor.execute(
                'INSERT INTO review(user,hotel,city,reviews,ip_address,today,reviewtype) VALUES (% s, % s, % s, %s, %s, %s, %s)',
                (name, hotel, city, review, ip, today, reviewtype))
            mysql.connection.commit()

            cursor.execute(
                'SELECT review_id  FROM review WHERE user like %s and hotel like %s and city like %s order by review_id desc',
                [name, hotel, city])
            row = cursor.fetchone()
            reviewID = row['review_id']  # string id
            ID = str(reviewID)  # int ID

            with open('Hotelreview_testingData.csv', mode='a') as csv_file:
                data = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data.writerow([ID,review, hotel, city, name])

            if reviewtype == 'Room':
                cursor.execute(
                    'SELECT checkInDate  FROM book_room WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                ch = cursor.fetchone()
                if ch == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s, %s,% s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    checkin = ch['checkInDate']
                    print(checkin)
                    checkin1 = datetime.strptime(checkin, '%Y-%m-%d').date()

                    if checkin1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s,% s, %s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()


            elif reviewtype == 'Table':
                cursor.execute(
                    'SELECT date  FROM book_table WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                da = cursor.fetchone()
                if da == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s, %s,% s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    datec = da['date']
                    date1 = datetime.strptime(datec, '%Y-%m-%d').date()
                    if date1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s,% s, %s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()

            return render_template('hotelsInBangalore.html')
        else:
            return render_template('alertbangalore.html')
    return render_template('hotelsInBangalore.html')


@app.route("/submitLeelaB", methods=["GET", "POST"])
def submitLeelaB():
    if request.method == "GET":
        return redirect(url_for('index.html'))
    elif (request.method == "POST"):
        reviewdata = dict(request.form)
        review = reviewdata["Review"]
        city = 'Bangalore'
        hotel = 'Leela'

        name = reviewdata["Username"]
        reviewtype = reviewdata["Reviewtype"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_registered WHERE Username like % s', [name])
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            ip = request.remote_addr
            today = date.today()
            cursor.execute(
                'INSERT INTO review(user,hotel,city,reviews,ip_address,today,reviewtype) VALUES (% s, % s, % s, %s, %s, %s, %s)',
                (name, hotel, city, review, ip, today, reviewtype))
            mysql.connection.commit()

            cursor.execute(
                'SELECT review_id  FROM review WHERE user like %s and hotel like %s and city like %s order by review_id desc',
                [name, hotel, city])
            row = cursor.fetchone()
            reviewID = row['review_id']  # string id
            ID = str(reviewID)  # int ID
            with open('Hotelreview_testingData.csv', mode='a') as csv_file:
                data = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data.writerow([ID, review, hotel, city, name])

            if reviewtype == 'Room':
                cursor.execute(
                    'SELECT checkInDate  FROM book_room WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                ch = cursor.fetchone()
                if ch == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s, %s,% s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    checkin = ch['checkInDate']
                    print(checkin)
                    checkin1 = datetime.strptime(checkin, '%Y-%m-%d').date()

                    if checkin1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s,% s, %s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()


            elif reviewtype == 'Table':
                cursor.execute(
                    'SELECT date  FROM book_table WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                da = cursor.fetchone()
                if da == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s,% s, % s, %s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    datec = da['date']
                    date1 = datetime.strptime(datec, '%Y-%m-%d').date()
                    if date1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s,% s, % s, %s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()

            return render_template('hotelsInBangalore.html')
        else:
            return render_template('alertbangalore.html')
    return render_template('hotelsInBangalore.html')


@app.route("/submitConradB", methods=["GET", "POST"])
def submitConradB():
    if request.method == "GET":
        return redirect(url_for('index.html'))
    elif (request.method == "POST"):
        reviewdata = dict(request.form)
        review = reviewdata["Review"]
        city = 'Bangalore'
        hotel = 'Conrad'

        name = reviewdata["Username"]
        reviewtype = reviewdata["Reviewtype"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_registered WHERE Username like % s', [name])
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            ip = request.remote_addr
            today = date.today()
            cursor.execute(
                'INSERT INTO review(user,hotel,city,reviews,ip_address,today,reviewtype) VALUES (% s, % s, % s, %s, %s, %s, %s)',
                (name, hotel, city, review, ip, today, reviewtype))
            mysql.connection.commit()

            cursor.execute(
                'SELECT review_id  FROM review WHERE user like %s and hotel like %s and city like %s order by review_id desc',
                [name, hotel, city])
            row = cursor.fetchone()
            reviewID = row['review_id']  # string id
            ID = str(reviewID)  # int ID
            with open('Hotelreview_testingData.csv', mode='a') as csv_file:
                data = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data.writerow([ID, review, hotel, city, name])

            if reviewtype == 'Room':
                cursor.execute(
                    'SELECT checkInDate  FROM book_room WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                ch = cursor.fetchone()
                if ch == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s,% s, %s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    checkin = ch['checkInDate']
                    print(checkin)
                    checkin1 = datetime.strptime(checkin, '%Y-%m-%d').date()

                    if checkin1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s,% s, %s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()


            elif reviewtype == 'Table':
                cursor.execute(
                    'SELECT date  FROM book_table WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                da = cursor.fetchone()
                if da == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s,% s, %s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    datec = da['date']
                    date1 = datetime.strptime(datec, '%Y-%m-%d').date()
                    if date1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s,% s, % s, %s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()

            return render_template('hotelsInBangalore.html')
        else:
            return render_template('alertbangalore.html')
    return render_template('hotelsInBangalore.html')


@app.route("/submitWindsorB", methods=["GET", "POST"])
def submitWindsorB():
    if request.method == "GET":
        return redirect(url_for('index.html'))
    elif (request.method == "POST"):
        reviewdata = dict(request.form)
        review = reviewdata["Review"]
        city = 'Bangalore'
        hotel = 'Windsor'
        name = reviewdata["Username"]
        reviewtype = reviewdata["Reviewtype"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_registered WHERE Username like % s', [name])
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            ip = request.remote_addr
            today = date.today()
            cursor.execute(
                'INSERT INTO review(user,hotel,city,reviews,ip_address,today,reviewtype) VALUES (% s, % s, % s, %s, %s, %s, %s)',
                (name, hotel, city, review, ip, today, reviewtype))
            mysql.connection.commit()

            cursor.execute(
                'SELECT review_id  FROM review WHERE user like %s and hotel like %s and city like %s order by review_id desc',
                [name, hotel, city])
            row = cursor.fetchone()
            reviewID = row['review_id']  # string id
            ID = str(reviewID)  # int ID
            with open('Hotelreview_testingData.csv', mode='a') as csv_file:
                data = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data.writerow([ID, review, hotel, city, name])

            if reviewtype == 'Room':
                cursor.execute(
                    'SELECT checkInDate  FROM book_room WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                ch = cursor.fetchone()
                if ch == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s, %s,% s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    checkin = ch['checkInDate']
                    print(checkin)
                    checkin1 = datetime.strptime(checkin, '%Y-%m-%d').date()

                    if checkin1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s,% s, % s, %s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()


            elif reviewtype == 'Table':
                cursor.execute(
                    'SELECT date  FROM book_table WHERE name like % s and hotel like %s and city_of_hotel like %s',
                    [name, hotel, city])
                da = cursor.fetchone()
                if da == None:
                    print('suspicious')
                    cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s,% s, % s, %s, %s, %s)',
                                   (reviewID, name, hotel, city, review, today, reviewtype))
                    mysql.connection.commit()
                else:

                    datec = da['date']
                    date1 = datetime.strptime(datec, '%Y-%m-%d').date()
                    if date1 < today:
                        print('valid')
                    else:
                        print('suspicious')
                        cursor.execute('INSERT INTO suspicious_reviews VALUES (% s, % s, % s,% s, %s, %s, %s)',
                                       (reviewID, name, hotel, city, review, today, reviewtype))
                        mysql.connection.commit()

            return render_template('hotelsInBangalore.html')
        else:
            return render_template('alertbangalore.html')
    return render_template('hotelsInBangalore.html')


# **************************************************************************************************************

@app.route('/index.html')
def index1():
    return render_template('index.html')



@app.route('/HomePage.html')
def home1():
    return render_template('HomePage.html')


@app.route('/login.html')
def login():
    return render_template('login.html')


@app.route('/UserLogin.html')
def UserLogin():
    return render_template('Userlogin.html')


@app.route('/index.html', methods=['GET', 'POST'])
def index():
    msg = ''
    print("hello")
    if request.method == 'POST' and 'fullname' in request.form and 'password' in request.form and 'email' in request.form and 'confirmpassword' in request.form:
        print("hello")
        username = request.form['fullname']
        password = request.form['password']
        email = request.form['email']
        cpassword = request.form['confirmpassword']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_registered WHERE username = % s', (username,))
        account = cursor.fetchone()

        print(account)

        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not re.match(r'[A-Za-z0-9]+', password):
            msg = 'Enter valid password!'
        elif not re.match(password, cpassword):
            msg = 'Enter valid confirm password'
        elif not username or not password or not email or not cpassword:
            msg = 'Please fill out the form !'
        else:

            cursor.execute('INSERT INTO user_registered VALUES (% s, % s, % s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return render_template('index.html', msg=msg)

    elif request.method == 'POST' and 'username' in request.form and 'password1' in request.form:
        username = request.form['username']
        password1 = request.form['password1']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_registered WHERE username = % s AND password = % s', (username, password1,))
        account = cursor.fetchone()
        print(account)
        if account:
            session['loggedin'] = True
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'

    return render_template('UserLogin.html', msg=msg)


# ***************************************************************************************************
# ****************************************Percentage**********************************************

def general():
    df = pd.read_csv('out.csv')
    header = ["ReviewID", "Reviews", 'Hotel', "City", "UserName", "Polarity"]
    df.columns = header
    a = df.groupby(["City", "Hotel", "Polarity"], as_index=False)["Reviews"].count()
    print("general function\n")
    print(a)
    City = list(a['City'])
    Hotel = list(a['Hotel'])
    Polarity = list(a['Polarity'])
    Reviews = list(a['Reviews'])
    Cities = set(City)
    return a, City, Hotel, Polarity, Reviews, Cities


def pune():
    # pune
    a, City, Hotel, Polarity, Reviews, Cities = general()
    print("pune function")
    print("\n")
    print(a)
    l1 = list()  # negative
    l11 = list()
    h1 = list()  # positive
    h11 = list()
    for j in range(len(a['Hotel'])):
        if City[j] == "Pune":
            if Polarity[j] == 0:
                l1.append(Reviews[j])
                l11.append(Hotel[j])
            elif Polarity[j] == 1:
                h1.append(Reviews[j])
                h11.append(Hotel[j])

    print(l1)
    print(l11)
    print(h1)
    print(h11)
    totalHotelPercentPune = dict()
    for i in range(len(h11)):
        sum = l1[i] + h1[i]
        posPercent = (h1[i] / sum) * 100
        totalHotelPercentPune[h11[i]] = round(posPercent, 2)
    return totalHotelPercentPune, l1, l11, h1, h11
    # print(totalHotelPercentPune)


def mumbai():
    # Mumbai
    a, City, Hotel, Polarity, Reviews, Cities = general()

    l2 = list()
    l12 = list()
    h2 = list()
    h12 = list()

    for j in range(len(a['Hotel'])):
        if City[j] == "Mumbai":
            if Polarity[j] == 0:
                l2.append(Reviews[j])
                l12.append(Hotel[j])
            elif Polarity[j] == 1:
                h2.append(Reviews[j])
                h12.append(Hotel[j])

    totalHotelPercentMum = dict()

    for i in range(len(h12)):
        sum = l2[i] + h2[i]
        posPercent = (h2[i] / sum) * 100
        totalHotelPercentMum[h12[i]] = round(posPercent, 2)
    return totalHotelPercentMum, l2, l12, h2, h12


def kolkata():
    # kolkatta
    a, City, Hotel, Polarity, Reviews, Cities = general()
    l3 = list()
    l13 = list()
    h3 = list()
    h13 = list()

    for j in range(len(a['Hotel'])):
        if City[j] == "Kolkata":
            if Polarity[j] == 0:
                l3.append(Reviews[j])
                l13.append(Hotel[j])
            elif Polarity[j] == 1:
                h3.append(Reviews[j])
                h13.append(Hotel[j])

    totalHotelPercentkol = dict()
    for i in range(len(h13)):
        sum = l3[i] + h3[i]
        posPercent = (h3[i] / sum) * 100
        totalHotelPercentkol[h13[i]] = round(posPercent, 2)
    return totalHotelPercentkol, l3, l13, h3, h13


def bangalore():
    # Bangalore
    a, City, Hotel, Polarity, Reviews, Cities = general()
    l4 = list()
    l14 = list()
    h4 = list()
    h14 = list()

    for j in range(len(a['Hotel'])):
        if City[j] == "Bangalore":
            if Polarity[j] == 0:
                l4.append(Reviews[j])
                l14.append(Hotel[j])
            elif Polarity[j] == 1:
                h4.append(Reviews[j])
                h14.append(Hotel[j])

    totalHotelPercentbang = dict()
    for i in range(len(h14)):
        sum = l4[i] + h4[i]
        posPercent = (h4[i] / sum) * 100
        totalHotelPercentbang[h14[i]] = round(posPercent, 2)
    return totalHotelPercentbang, l4, l14, h4, h14


# ****************************************Percentage*************************************************
# ***************************************************************************************************

@app.route('/hotelsInPune.html')
def hotelsInPune():
    print("In hotel pune ")
    conn = MySQLdb.connect("localhost", "root", pw, "beproject")
    cur = conn.cursor()
    cur.execute('select user,reviews from review where hotel="Orchid" and city="Pune"')
    data = cur.fetchall()  # data from user_registered database
    cur.execute('select user,reviews from review where hotel="Novotel" and city="Pune"')
    data1 = cur.fetchall()  # data from book_room database
    cur.execute('select user,reviews from review where hotel="Conrad" and city="Pune"')
    data2 = cur.fetchall()  # data from book_table database
    cur.execute('select user,reviews from review where hotel="Courtyard" and city="Pune"')
    data3 = cur.fetchall()  # data from book_table database
    percentage, l1, l11, h1, h11 = pune()
    print("Hii", percentage)

    percentOrchid = str(percentage['Orchid'])
    percentNovotel = str(percentage['Novotel'])
    percentConrad = str(percentage['Conrad'])
    percentCourtyard = str(percentage['Courtyard'])

    '''percentOrchid=str("80")
    percentNovotel=str("80")
    percentConrad=str("80")
    percentCourtyard=str("80")'''

    percentOrchid = percentOrchid + "% Positive Reviews"
    percentNovotel = percentNovotel + "% Positive Reviews"
    percentConrad = percentConrad + "% Positive Reviews"
    percentCourtyard = percentCourtyard + "% Positive Reviews"

    percentOrchid1 = percentage['Orchid']
    percentNovotel1 = percentage['Novotel']
    percentConrad1 = percentage['Conrad']
    percentCourtyard1 = percentage['Courtyard']

    list_of_pune = list()

    for i in range(len(l1)):
        j = l1[i] + h1[i]
        list_of_pune.append(j)

    print("Total count of reviews for pune ")
    print(list_of_pune)

    return render_template("hotelsInPune.html", value=data, value1=data1, value2=data2, value3=data3,
                           value4=percentOrchid, value5=percentNovotel, value6=percentConrad, value7=percentCourtyard,
                           value8=percentOrchid1, value9=percentNovotel1, value10=percentConrad1,
                           value11=percentCourtyard1, value12=list_of_pune[0], value13=list_of_pune[1],
                           value14=list_of_pune[2], value15=list_of_pune[3])


@app.route('/hotelsInMumbai.html')
def hotelsInMumbai():
    conn = MySQLdb.connect("localhost", "root", pw, "beproject")
    cur = conn.cursor()
    cur.execute('select user,reviews from review where hotel="Hilton" and city="Mumbai"')
    data = cur.fetchall()  # data from user_registered database
    cur.execute('select user,reviews from review where hotel="Taj" and city="Mumbai"')
    data1 = cur.fetchall()  # data from book_room database
    cur.execute('select user,reviews from review where hotel="ITC" and city="Mumbai"')
    data2 = cur.fetchall()  # data from book_table database
    cur.execute('select user,reviews from review where hotel="Maratha" and city="Mumbai"')
    data3 = cur.fetchall()  # data from book_table database
    percentage, l2, l12, h2, h12 = mumbai()
    percentHilton = str(percentage['Hilton'])
    percentTaj = str(percentage['Taj'])
    percentITC = str(percentage['ITC'])
    percentMaratha = str(percentage['Maratha'])

    percentHilton = percentHilton + "% Positive Reviews"
    percentTaj = percentTaj + "% Positive Reviews"
    percentITC = percentITC + "% Positive Reviews"
    percentMaratha = percentMaratha + "% Positive Reviews"

    percentHilton1 = percentage['Hilton']
    percentTaj1 = percentage['Taj']
    percentITC1 = percentage['ITC']
    percentMaratha1 = percentage['Maratha']

    list_of_mumbai = list()

    for i in range(len(l2)):
        j = l2[i] + h2[i]
        list_of_mumbai.append(j)

    print("Total count of reviews for mumbai ")
    print(list_of_mumbai)

    return render_template("hotelsInMumbai.html", value=data, value1=data1, value2=data2, value3=data3,
                           value4=percentHilton, value5=percentTaj, value6=percentITC, value7=percentMaratha,
                           value8=percentHilton1, value9=percentTaj1, value10=percentITC1, value11=percentMaratha1,
                           value12=list_of_mumbai[0], value13=list_of_mumbai[1], value14=list_of_mumbai[2],
                           value15=list_of_mumbai[3])


@app.route('/hotelsInKolkata.html')
def hotelsInKolkata():
    conn = MySQLdb.connect("localhost", "root", pw, "beproject")
    cur = conn.cursor()
    cur.execute('select user,reviews from review where hotel="ITC" and city="Kolkata"')
    data = cur.fetchall()  # data from user_registered database
    cur.execute('select user,reviews from review where hotel="Oberoi" and city="Kolkata"')
    data1 = cur.fetchall()  # data from book_room database
    cur.execute('select user,reviews from review where hotel="Taj" and city="Kolkata"')
    data2 = cur.fetchall()  # data from book_table database
    cur.execute('select user,reviews from review where hotel="Marriott" and city="Kolkata"')
    data3 = cur.fetchall()  # data from book_table database
    percentage, l3, l13, h3, h13 = kolkata()
    percentITC = str(percentage['ITC'])
    percentOberoi = str(percentage['Oberoi'])
    percentTaj = str(percentage['Taj'])
    percentMarriott = str(percentage['Marriott'])

    percentITC = percentITC + "% Positive Reviews"
    percentOberoi = percentOberoi + "% Positive Reviews"
    percentTaj = percentTaj + "% Positive Reviews"
    percentMarriott = percentMarriott + "% Positive Reviews"

    percentITC1 = percentage['ITC']
    percentOberoi1 = percentage['Oberoi']
    percentTaj1 = percentage['Taj']
    percentMarriott1 = percentage['Marriott']

    list_of_kolkata = list()

    for i in range(len(l3)):
        j = l3[i] + h3[i]
        list_of_kolkata.append(j)

    print("Total count of reviews for Kolkata ")
    print(list_of_kolkata)

    return render_template("hotelsInKolkata.html", value=data, value1=data1, value2=data2, value3=data3,
                           value4=percentITC, value5=percentOberoi, value6=percentTaj, value7=percentMarriott,
                           value8=percentITC1, value9=percentOberoi1, value10=percentTaj1, value11=percentMarriott1,
                           value12=list_of_kolkata[0], value13=list_of_kolkata[1], value14=list_of_kolkata[2],
                           value15=list_of_kolkata[3])


@app.route('/hotelsInBangalore.html')
def hotelsInBangalore():
    conn = MySQLdb.connect("localhost", "root", pw, "beproject")
    cur = conn.cursor()
    cur.execute('select user,reviews from review where hotel="WelcomHotel" and city="Bangalore"')
    data = cur.fetchall()  # data from user_registered database
    cur.execute('select user,reviews from review where hotel="Leela" and city="Bangalore"')
    data1 = cur.fetchall()  # data from book_room database
    cur.execute('select user,reviews from review where hotel="Conrad" and city="Bangalore"')
    data2 = cur.fetchall()  # data from book_table database
    cur.execute('select user,reviews from review where hotel="Windsor" and city="Bangalore"')
    data3 = cur.fetchall()  # data from book_table database
    percentage, l4, l14, h4, h14 = bangalore()
    percentWelcomHotel = str(percentage['WelcomHotel'])
    percentLeela = str(percentage['Leela'])
    percentConrad = str(percentage['Conrad'])
    percentWindsor = str(percentage['Windsor'])

    percentWelcomHotel = percentWelcomHotel + "% Positive Reviews"
    percentLeela = percentLeela + "% Positive Reviews"
    percentConrad = percentConrad + "% Positive Reviews"
    percentWindsor = percentWindsor + "% Positive Reviews"

    percentWelcomHotel1 = percentage['WelcomHotel']
    percentLeela1 = percentage['Leela']
    percentConrad1 = percentage['Conrad']
    percentWindsor1 = percentage['Windsor']

    list_of_bangalore = list()

    for i in range(len(l4)):
        j = l4[i] + h4[i]
        list_of_bangalore.append(j)

    print("Total count of reviews for bangalore ")
    print(list_of_bangalore)

    return render_template("hotelsInBangalore.html", value=data, value1=data1, value2=data2, value3=data3,
                           value4=percentWelcomHotel, value5=percentLeela, value6=percentConrad, value7=percentWindsor,
                           value8=percentWelcomHotel1, value9=percentLeela1, value10=percentConrad1,
                           value11=percentWindsor1, value12=list_of_bangalore[0], value13=list_of_bangalore[1],
                           value14=list_of_bangalore[2], value15=list_of_bangalore[3])


@app.route('/bookRoom.html')
def bookRoom():
    return render_template('bookRoom.html')


@app.route('/bookTable.html')
def bookTable():
    return render_template('bookTable.html')


@app.route('/Booked.html', methods=['POST'])
def Booked():
    msg = ''
    print("hello")
    if request.method == 'POST' and 'fullname' in request.form and 'phone' in request.form and 'email' in request.form and 'no_of_rooms' in request.form:
        print("hello")
        hotel_city = request.form['hotel1']
        h1 = hotel_city.split(",")
        hotel = h1[0]
        city1 = h1[1]
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        no_of_rooms = request.form['no_of_rooms']
        city = request.form['city']
        checkin = request.form['checkin']
        no_of_people = request.form['no_of_people']
        other_needs = request.form['other_needs']
        checkout = request.form['checkout']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM book_room WHERE name = % s', (fullname,))
        account = cursor.fetchone()
        print(account)

        cursor.execute('INSERT INTO book_room VALUES (% s, % s, % s, %s, %s, %s, %s, %s ,%s,%s,%s)', (
        fullname, email, phone, city, checkin, no_of_people, no_of_rooms, other_needs, checkout, hotel, city1))
        mysql.connection.commit()
        msg = 'You have successfully registered !'
        return render_template('Booked.html', msg=msg)

    elif request.method == 'POST' and 'data_3' in request.form and 'data_4' in request.form and 'data_5' in request.form and 'data_7' in request.form:
        print("hello")
        hotel_city = request.form['hotel1']
        h1 = hotel_city.split(",")
        hotel = h1[0]
        city1 = h1[1]

        fullname = request.form['data_3']
        phone = request.form['data_4']
        email = request.form['data_5']
        date = request.form['data_6']
        intime = request.form['data_7']
        outtime = request.form['data_33']
        no_of_people = request.form['data_8']
        add_request = request.form['data_9']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM book_table WHERE name = % s', (fullname,))
        account = cursor.fetchone()
        print(account)
        cursor.execute('INSERT INTO book_table VALUES (% s, % s, % s, %s,%s, %s, %s, %s,%s,%s)',
                       (fullname, email, phone, date, intime, outtime, no_of_people, add_request, hotel, city1))
        mysql.connection.commit()
        msg = 'You have successfully registered !'
        return render_template('Booked.html', msg=msg)

@app.route('/delete.html/<int:ReviewID>')
def delete(ReviewID):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    print(type(ReviewID))

    cur.execute('select * from review where review_id=%s',(ReviewID,))
    data = cur.fetchone()
    print(data)
    if data:
        print("inside if")
        cur.execute('delete from review where review_id=%s',(ReviewID,))
        mysql.connection.commit()
        cur.execute('select * from suspicious_reviews where review_id=%s',(ReviewID,))
        data1=cur.fetchone()
        if data1:
            print("inside suspicious if")
            cur.execute('delete from suspicious_reviews where review_id=%s', (ReviewID,))
            mysql.connection.commit()
        else:
            print("Data not found in suspicious reviews")

        updatedlist = []
        ReviewID1=str(ReviewID)
        with open("Hotelreview_testingData.csv", newline="\n") as f:
            reader = csv.reader(f)
            # username = input("Enter the username of the user you wish to remove from file:")
            print(reader)
            for row in reader:  # for every row in the file
                print("shukkkkk")
                if not row:
                    continue
                print(row[0])

                if row[0] == "ReviewID":
                    header = ["ReviewID", "Reviews", "Hotel", "City", "UserName"]
                    updatedlist.append(header)
                    continue
                if row[0] != ReviewID1:  # as long as the username is not in the row .......
                    updatedlist.append(row)  # add each row, line by line, into a list called 'udpatedlist'

            print(updatedlist)
            i = updatefile(updatedlist)
            print(i)

    else:
        updatedlist = []
        ReviewID1 = str(ReviewID)
        with open("Hotelreview_testingData.csv", newline="\n") as f:
            reader = csv.reader(f)
            #username = input("Enter the username of the user you wish to remove from file:")
            print(reader)
            for row in reader:  # for every row in the file
                print("shukkkkk")
                if not row:
                    continue
                print(row[0])

                if row[0] == "ReviewID":
                    header = ["ReviewID","Reviews","Hotel","City","UserName"]
                    updatedlist.append(header)
                    continue
                if row[0] != ReviewID1:  # as long as the username is not in the row .......
                    updatedlist.append(row)  # add each row, line by line, into a list called 'udpatedlist'

            print(updatedlist)
            i=updatefile(updatedlist)
            print(i)
    return redirect(url_for('home1'))

def updatefile(updatedlist):
    with open("Hotelreview_testingData.csv","w",newline="\n") as f:
        Writer=csv.writer(f)
        Writer.writerows(updatedlist)
        print("File has been updated")
        return 1

################################################


if __name__ == "__main__":
    mlmodel.mlmodel()
    Fake_review_5_Algos.mlmodels_2()

    app.run(debug=True)

