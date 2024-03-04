from app import app
from app import db
from flask import Flask, render_template, redirect, url_for, request
import pika, sys
import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.models import RealEstate
from app.forms import FilterForm
from app.forms import PublishForm
from app.forms import StatsForm1

@app.shell_context_processor
def make_shell_context():
  return {'db': db, 'RealEstate': RealEstate}

maindf = pd.read_csv('D:/xxx/Documents/cian_parsing.csv', sep=";", encoding='windows-1251')
maindfcols = maindf.columns

def sendmsg(task):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='powerImport', durable=True)


    channel.basic_publish(exchange='',
                          routing_key='powerImport',
                          body=str(task),
                          properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))

    print(" [x] Sent ", task)

    connection.close()

@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    form = FilterForm()
    #power = Power.query.all()
    realestate = RealEstate.query.all()
    #realestateres = realestate
    print("test")
    if form.validate_on_submit():
        #filt_rooms = request.args.get("f_rooms")
        print("inside")
        realestateres2 = RealEstate.query
        if form.f_rooms.data:
          filt_rooms = form.f_rooms.data
          realestateres2 = realestateres2.filter(RealEstate.rooms_count == filt_rooms)
        if form.f_district.data:
          filt_district = form.f_district.data
          realestateres2 = realestateres2.filter(RealEstate.district == filt_district)
        if form.f_metro.data:
          filt_metro = form.f_metro.data
          realestateres2 = realestateres2.filter(RealEstate.underground == filt_metro)
        if form.f_author_type.data:
          filt_author_type = form.f_author_type.data
          if filt_author_type != "Не выбрано":
            if filt_author_type == "Агент": filt_author_type = "real_estate_agent"
            if filt_author_type == "Официальный представитель": filt_author_type = "official_representative"
            if filt_author_type == "Риэлтор": filt_author_type = "realtor"
            if filt_author_type == "Собственник": filt_author_type = "homeowner"
            realestateres2 = realestateres2.filter(RealEstate.author_type == filt_author_type)
        if form.f_area_lower.data:
          filt_area_lower = float(form.f_area_lower.data)
          realestateres2 = realestateres2.filter(RealEstate.total_meters >= filt_area_lower)
        if form.f_area_upper.data:
          filt_area_upper = float(form.f_area_upper.data)
          realestateres2 = realestateres2.filter(RealEstate.total_meters <= filt_area_upper)
        if form.f_price_lower.data:
          filt_price_lower = form.f_price_lower.data
          realestateres2 = realestateres2.filter(RealEstate.price_per_month >= filt_price_lower)
        if form.f_price_upper.data:
          filt_price_upper = form.f_price_upper.data
          realestateres2 = realestateres2.filter(RealEstate.price_per_month <= filt_price_upper)
        #realestateres = realestateres2

        realestate = realestateres2.all()
        #realestateres = cur.execute(f'select * from real_estate where rooms_count = {filt_rooms};')\
        #.fetchall().tolist()
        #print(filt_rooms)
        #print(filt_rooms)
    print(form.errors)
    #test = RealEstate.query.filter(RealEstate.rooms_count == filt_rooms).get(7)
    #print(test)
    return render_template("filter.html", rows=realestate, form=form) # changed to the altered version for filters
    #return render_template("tables.html", rows=power)
   # return render_template("tables.html", rows=list(maindf.values.tolist()))
    #return render_template("tables.html", column_names=maindf.columns.values, row_data=list(maindf.values.tolist()), zip=zip)

@app.route("/publish", methods=['GET', 'POST'])
def publish():
    con = sqlite3.connect("app.db")
    cur = con.cursor()
    formp = PublishForm()
    if formp.validate_on_submit():
        print("publish form submitted!")
        pub_author = formp.p_author.data
        pub_author_type = formp.p_author_type.data
        pub_link = formp.p_link.data
        pub_city = formp.p_city.data
        pub_deal_type = formp.p_deal_type.data
        pub_accommodation_type = formp.p_accommodation_type.data
        pub_floor = formp.p_floor.data
        pub_floors_count = formp.p_floors_count.data
        pub_rooms_count = formp.p_rooms_count.data
        pub_total_meters = float(formp.p_total_meters.data)
        pub_price_per_month = formp.p_price_per_month.data
        pub_price_per_m2 = pub_price_per_month / pub_total_meters
        pub_commissions =  float(formp.p_commissions.data)
        pub_district = formp.p_district.data
        pub_street = formp.p_street.data
        pub_house_number = formp.p_house_number.data
        pub_underground = formp.p_underground.data

        new_ad_obj = RealEstate(
            author = pub_author,
            author_type = pub_author_type,
            link = pub_link,
            city = pub_city,
            deal_type = pub_deal_type,
            accommodation_type = pub_accommodation_type,
            floor = pub_floor,
            floors_count = pub_floors_count,
            rooms_count = pub_rooms_count,
            total_meters = pub_total_meters,
            price_per_m2 = pub_price_per_m2,
            price_per_month = pub_price_per_month,
            commissions = pub_commissions,
            district = pub_district,
            street = pub_street,
            house_number = pub_house_number,
            underground = pub_underground
        )
        with app.app_context():
            try:
                db.session.add(new_ad_obj)
                db.session.commit()
            except IntegrityError as int_err:
                print(int_err)
                print("Error on insert")
            finally:
                return redirect(url_for('index'))
    print(formp.errors)
    return render_template("publishform.html", formp=formp)

@app.route("/refresh") # update
def refresh():
    #sendmsg("Push")
    #realestate = RealEstate.query.all()
    return redirect(url_for('index'))


@app.route("/stats", methods=['GET', 'POST'])
def stats():
    forms1 = StatsForm1()
    con = sqlite3.connect("app.db")
    cur = con.cursor()
    q1res = ()
    querytextleft = """select district, round(avg(price_per_month), 2) as avg_price, round(avg(total_meters), 2) as avg_area,
    round(avg(price_per_m2), 2) as avg_price_per_m2, COUNT(district) as district_appearances
    from real_estate group by district"""
    querytextright = " order by avg_price"
    if forms1.validate_on_submit():
        print("inside stats")
        if forms1.s1_sort.data == "pricetotal":
            querytextright = " order by avg_price"
        if forms1.s1_sort.data == "area":
            querytextright = " order by avg_area"
        if forms1.s1_sort.data == "priceperm2":
            querytextright = " order by avg_price_per_m2"
        if forms1.s1_direction.data == "down":
            querytextright = querytextright + " desc"
        #return render_template("statsform1.html", rows=q1res, forms1=forms1)
    print(forms1.errors)
    querytext = querytextleft + querytextright + ";"
    q1res = cur.execute(querytext)\
    .fetchall()
    for i in range (len(q1res)):
        q1res[i] = (i+1,) + q1res[i]
        #print(q1res[i])
    #price graph
    #pricemax = cur.execute("select max(price_per_month) as max_price from real_estate").fetchall()[0][0]
    #pricemin = cur.execute("select min(price_per_month) as max_price from real_estate").fetchall()[0][0]
    #pricedelta = pricemax - pricemin
    q1res2 = cur.execute("select price_per_month as max_price from real_estate").fetchall()
    print(q1res2[0:5])
    prices = [elem[0] for elem in q1res2]
    prices = np.sort(prices)
    pricemax = max(prices)
    pricemin = min(prices)
    pricedelta = pricemax - pricemin
    s1_n = 11 # 11 intervals for 1.3k entries
    s1_h = pricedelta / s1_n
    left = np.arange(pricemin, pricemax, s1_h)
    right = np.arange(pricemin+s1_h, pricemax+1000, s1_h)  #+1 works too but just in case
    labels1 = []
    labels2 = []
    labels3 = []
    for i in range(s1_n):
        labels1.append(str(round(left[i], 2)) + " - " + str(round(right[i], 2)))
    counts = np.zeros(s1_n)
    counts2 = np.zeros(s1_n)
    counts3 = np.zeros(s1_n) # still > 1024 entries so still 11 intervals
    #prices2 = np.sort(prices)
    tocut = round(len(prices) / 100)
    tocut3 = round(len(prices) / 20) # 5 percent off each side
    pricemincut = prices[tocut]
    pricemaxcut = prices[len(prices) - 1 - tocut]
    pricedeltacut = pricemaxcut - pricemincut
    #prices = prices[tocut:(len(prices) - tocut)]
    pricemincut3 = prices[tocut3]
    pricemaxcut3 = prices[len(prices) - 1 - tocut3]
    pricedeltacut3 = pricemaxcut3 - pricemincut3
    s1_hc = pricedeltacut / s1_n
    s1_hc3 = pricedeltacut3 / s1_n
    leftcut = np.arange(pricemincut, pricemaxcut, s1_hc)
    rightcut = np.arange(pricemincut+s1_hc, pricemaxcut+100, s1_hc)
    leftcut3 = np.arange(pricemincut3, pricemaxcut3, s1_hc3)
    rightcut3 = np.arange(pricemincut3+s1_hc3, pricemaxcut3+100, s1_hc3)
    for i in range(s1_n):
        labels2.append(str(round(leftcut[i], 2)) + " - " + str(round(rightcut[i], 2)))
        labels3.append(str(round(leftcut3[i], 2)) + " - " + str(round(rightcut3[i], 2)))
    for elem in prices:
        # guaranteed for uncropped
        curintindex = 0
        for i in range(1, s1_n):
            if (elem < left[i]):
                break
            curintindex += 1
        counts[curintindex] += 1
        # conditional for cropped
        curintindex = 0
        if ((elem >= pricemincut) and (elem <= pricemaxcut)):
            for i in range(1, s1_n):
                if (elem < leftcut[i]):
                    break
                curintindex += 1
            counts2[curintindex] += 1
        # conditional for cropped 10 percent
        curintindex = 0
        if ((elem >= pricemincut3) and (elem <= pricemaxcut3)):
            for i in range(1, s1_n):
                if (elem < leftcut3[i]):
                    break
                curintindex += 1
            counts3[curintindex] += 1
    """for elem in prices2:
        curintindex = 0
        for i in range(1, s1_n):
            if (elem < leftcut[i]):
                break
            curintindex += 1
        counts2[curintindex] += 1"""
    print(pricemax, pricemin, pricedelta)
    print(counts)
    print("left:", left)
    print(pricemaxcut, pricemincut, pricedeltacut)
    print(counts2)
    print(labels2)
    print(labels1)
    # graph for area distribution
    q1res3 = cur.execute("select total_meters as area from real_estate").fetchall()
    areas = [float(elem[0]) for elem in q1res3]
    areas = np.sort(areas)
    areamax = max(areas)
    areamin = min(areas)
    areadelta = areamax - areamin
    s4_n = 11
    s4_h = areadelta / s4_n
    arealeft = np.arange(areamin, areamax, s4_h)
    arearight = np.arange(areamin+s4_h, areamax+1, s4_h)
    tocut4 = round(len(areas) / 40) # 5 percent
    areamincut = areas[tocut4]
    areamaxcut = areas[len(areas) - 1 - tocut4]
    areadeltacut = areamaxcut - areamincut
    s5_h = areadeltacut / s4_n
    arealeftcut = np.arange(areamincut, areamaxcut, s5_h)
    arearightcut = np.arange(areamincut+s5_h, areamaxcut+1, s5_h)
    labels4 = []
    labels5 = []
    for i in range(s4_n):
        labels4.append(str(round(arealeft[i], 2)) + " - " + str(round(arearight[i], 2)))
        labels5.append(str(round(arealeftcut[i], 2)) + " - " + str(round(arearightcut[i], 2)))
    counts4 = np.zeros(s4_n)
    counts5 = np.zeros(s4_n)
    for elem in areas:
        # guaranteed for uncropped
        curintindex = 0
        for i in range(1, s4_n):
            if (elem < arealeft[i]):
                break
            curintindex += 1
        counts4[curintindex] += 1
        curintindex = 0
        if ((elem >= areamincut) and (elem <= areamaxcut)):
            for i in range(1, s4_n):
                if (elem < arealeftcut[i]):
                    break
                curintindex += 1
            counts5[curintindex] += 1
    # average/max tables
    q2res = ()
    q2res = cur.execute("""select distinct author_type as auth, count(id) as cnt
    from real_estate group by author_type order by cnt DESC limit 1;""").fetchall()
    q2res2 = cur.execute("""select distinct rooms_count as rooms, count(id) as cnt
    from real_estate group by rooms_count order by cnt DESC limit 1;""").fetchall()
    q2res3 = cur.execute("""select distinct district as dist, count(id) as cnt
    from real_estate group by district order by cnt DESC limit 1;""").fetchall()
    q2list = []
    q2list.append(("Тип автора",) + q2res[0])
    q2list.append(("Число комнат",) + q2res2[0])
    q2list.append(("Район",) + q2res3[0])
    # prices, areas
    q3res3 = cur.execute("select price_per_m2 as pricem2 from real_estate").fetchall()
    priceperm2 = [elem[0] for elem in q3res3]
    pricesmean = np.round(np.mean(prices), 2)
    pricesstd=  np.round(np.std(prices), 2)
    areasmean = np.round(np.mean(areas), 2)
    areasstd = np.round(np.std(areas), 2)
    priceperm2mean = np.round(np.mean(priceperm2), 2)
    priceperm2std = np.round(np.std(priceperm2), 2)
    q3list = []
    q3list.append(("Цена за месяц, руб",) + (pricesmean,) + (pricesstd,))
    q3list.append(("Площадь, кв. м",) + (areasmean,) + (areasstd,))
    q3list.append(("Цена за кв. м, руб",) + (priceperm2mean,) + (priceperm2std,))
    #querytext = querytextleft + querytextright + ";"
    #q1res = cur.execute(querytext)\
    #.fetchall()
    #for i in range (len(q1res)):
    #    #print(type(curtup))
    #    #q1res[i] = (i,) + q1res[i]
    #    #print(q1res[i])
    #print(q1res[0])
    #print(q1res[0][0], q1res[0][1], q1res[0][2])
    return render_template("statsform1.html", rows=q1res, forms1=forms1, labels1=labels1, values1=counts.tolist(),
    labels1v2=labels2, values1v2=counts2.tolist(), labels1v3=labels3, values1v3=counts3.tolist(),
    labels4=labels4, values4=counts4.tolist(), labels5=labels5, values5=counts5.tolist(), t2data=q2list, t3data=q3list)