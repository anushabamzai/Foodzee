# from ast import Return
# from crypt import methods
from urllib.request import Request
from flask import Flask, render_template, url_for, flash, redirect, request
import pandas as pd

# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
app = Flask(__name__)
#import pandas as pd
lko_rest = pd.read_csv("india.csv", encoding='unicode_escape')

def fav(lko_rest1):
    lko_rest1 = lko_rest1.reset_index()
    from sklearn.feature_extraction.text import CountVectorizer

    count1 = CountVectorizer(stop_words='english')
    count_matrix = count1.fit_transform(lko_rest1['highlights'])
    from sklearn.metrics.pairwise import cosine_similarity

    cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

    sim = list(enumerate(cosine_sim2[0]))
    sim = sorted(sim, key=lambda x: x[1], reverse=True)
    sim = sim[1:11]
    indi = [i[0] for i in sim]

    final = lko_rest1.copy().iloc[indi[0]]
    final = pd.DataFrame(final)
    final = final.T

    for i in range(1, len(indi)):
        final1 = lko_rest1.copy().iloc[indi[i]]
        final1 = pd.DataFrame(final1)
        final1 = final1.T
        final = pd.concat([final, final1])
    
    return final


def rest_rec( Locality=[], lko_rest=lko_rest):
    
    lko_rest1 = lko_rest.copy().loc[lko_rest['locality'] == Locality[0]]

    for i in range(1, len(Locality)):
        lko_rest2 = lko_rest.copy().loc[lko_rest['locality'] == Locality[i]]
        lko_rest1 = pd.concat([lko_rest1, lko_rest2])
        lko_rest1.drop_duplicates(subset='name', keep='last', inplace=True)

    lko_rest_locale = lko_rest1.copy()
    
    return lko_rest_locale
   

def rest_recrat(cost, people=2, min_cost=1, cuisine=[],Locality=[],rating=[], fav_rest="",lko_rest=lko_rest):
    cost = cost + 200
  
    x = cost / people
    y = min_cost / people

    lko_rest1 = lko_rest.copy().loc[lko_rest['locality'] == Locality[0]]

    for i in range(1, len(Locality)):
        lko_rest2 = lko_rest.copy().loc[lko_rest['locality'] == Locality[i]]
        lko_rest1 = pd.concat([lko_rest1, lko_rest2])
        lko_rest1.drop_duplicates(subset='name', keep='last', inplace=True)

    lko_rest_locale = lko_rest1.copy()

    lko_rest_locale = lko_rest_locale.loc[lko_rest_locale['average_cost_for_one'] <= x]
    lko_rest_locale = lko_rest_locale.loc[lko_rest_locale['average_cost_for_one'] >= y]

    lko_rest_locale['Start'] = lko_rest_locale['cuisines'].str.find(cuisine[0])
    lko_rest_cui = lko_rest_locale.copy().loc[lko_rest_locale['Start'] >= 0]
    
    for i in range(1, len(cuisine)):
       lko_rest_locale['Start'] = lko_rest_locale['cuisines'].str.find(cuisine[i])
       lko_rest_cu = lko_rest_locale.copy().loc[lko_rest_locale['Start'] >= 0]
       lko_rest_cui = pd.concat([lko_rest_cui, lko_rest_cu])
       lko_rest_cui.drop_duplicates(subset='name', keep='last', inplace=True)

    if fav_rest != "":

      favr = lko_rest.loc[lko_rest['name'] == fav_rest].drop_duplicates()
      favr = pd.DataFrame(favr)
      lko_rest3 = pd.concat([favr, lko_rest_cui])
      lko_rest3.drop('Start', axis=1, inplace=True)
      rest_selected = fav(lko_rest3)
    
    else:
       lko_rest_cui = lko_rest_cui.sort_values('scope', ascending=False)
       rest_selected = lko_rest_cui.head(10)
        
    if rating[0] =="yes":
       rest_selected=rest_selected.sort_values(['aggregate_rating'],ascending=[0])

    else:
        lko_rest_cui = lko_rest_cui.sort_values('scope', ascending=False)
        rest_selected = lko_rest_cui.head(10)

    return rest_selected


def rest_search(restaurant=[],Locality=[], fav_rest="",lko_rest=lko_rest):
    lko_rest1 = lko_rest.copy().loc[lko_rest['locality'] == Locality[0]]

    for i in range(1, len(Locality)):
        lko_rest2 = lko_rest.copy().loc[lko_rest['locality'] == Locality[i]]
        lko_rest1 = pd.concat([lko_rest1, lko_rest2])
        lko_rest1.drop_duplicates(subset='name', keep='last', inplace=True)

    lko_rest_locale = lko_rest1.copy()

    lko_rest_locale['Start'] = lko_rest_locale['name'].str.find(restaurant[0])
    lko_rest_cui = lko_rest_locale.copy().loc[lko_rest_locale['Start'] >= 0]
    
    for i in range(1, len(restaurant)):
       lko_rest_locale['Start'] = lko_rest_locale['name'].str.find(restaurant[i])
       lko_rest_cu = lko_rest_locale.copy().loc[lko_rest_locale['Start'] >= 0]
       lko_rest_cui = pd.concat([lko_rest_cui, lko_rest_cu])
       lko_rest_cui.drop_duplicates(subset='name', keep='last', inplace=True)
    
    return lko_rest_cui

def rest_like(age,Locality=[],fav_rest="",lko_rest=lko_rest):
    lko_rest1 = lko_rest.copy().loc[lko_rest['locality'] == Locality[0]]

    for i in range(1, len(Locality)):
        lko_rest2 = lko_rest.copy().loc[lko_rest['locality'] == Locality[i]]
        lko_rest1 = pd.concat([lko_rest1, lko_rest2])
        lko_rest1.drop_duplicates(subset='name', keep='last', inplace=True)

    lko_rest_locale = lko_rest1.copy()
    
    if age>=12 and age<18:
        group="G1"
        lko_rest_locale['Start'] = lko_rest_locale['group'].str.find(group)
        lko_rest_cui = lko_rest_locale.copy().loc[lko_rest_locale['Start'] >= 0]
       
    
    if age>=18 and age<30:
        group="G2"
        lko_rest_locale['Start'] = lko_rest_locale['group'].str.find(group)
        lko_rest_cui = lko_rest_locale.copy().loc[lko_rest_locale['Start'] >= 0]
       


    if age>=30 and age<60:
        group="G3"
        lko_rest_locale['Start'] = lko_rest_locale['group'].str.find(group)
        lko_rest_cui = lko_rest_locale.copy().loc[lko_rest_locale['Start'] >= 0]
    
    
    if age>=60:
        group="G4"
        lko_rest_locale['Start'] = lko_rest_locale['group'].str.find(group)
        lko_rest_cui = lko_rest_locale.copy().loc[lko_rest_locale['Start'] >= 0]
 
    return lko_rest_cui
def rest_order(Locality=[],name=[],fav_rest="",lko_rest=lko_rest):
    lko_rest1 = lko_rest.copy().loc[lko_rest['locality'] == Locality[0]]
     
    for i in range(1, len(Locality)):
        lko_rest2 = lko_rest.copy().loc[lko_rest['locality'] == Locality[i]]
        lko_rest1 = pd.concat([lko_rest1, lko_rest2])
        lko_rest1.drop_duplicates(subset='name', keep='last', inplace=True)

    lko_rest_locale = lko_rest1.copy()
    lko_rest_locale['Start'] = lko_rest_locale['name'].str.find(name[0])
    lko_rest_cui = lko_rest_locale.copy().loc[lko_rest_locale['Start'] >= 0]
    
    for i in range(1, len(name)):
       lko_rest_locale['Start'] = lko_rest_locale['name'].str.find(name[i])
       lko_rest_cu = lko_rest_locale.copy().loc[lko_rest_locale['Start'] >= 0]
       lko_rest_cui = pd.concat([lko_rest_cui, lko_rest_cu])
       lko_rest_cui.drop_duplicates(subset='name', keep='last', inplace=True)

def calc( locality):
    rest_sugg = rest_rec( [locality])
    rest_list1 = rest_sugg.copy().loc[:,
                 ['name', 'address', 'locality', 'timings', 'aggregate_rating','url', 'cuisines','feature']]
    rest_list = pd.DataFrame(rest_list1)
    rest_list = rest_list.reset_index()
    rest_list = rest_list.rename(columns={'index': 'res_id'})
    rest_list.drop('res_id', axis=1, inplace=True)
    rest_list = rest_list.T
    rest_list = rest_list
    ans = rest_list.to_dict()
    res = [value for value in ans.values()]
    return res
  
    
def calcr( max_Price,people ,min_Price, cuisine,locality, rating):
    rest_sugg = rest_recrat(max_Price, people, min_Price, [cuisine],[locality],[rating])
    rest_list1 = rest_sugg.copy().loc[:,
                 ['name', 'address', 'locality', 'timings', 'aggregate_rating', 'url', 'cuisines','feature']]
    rest_list = pd.DataFrame(rest_list1)
    rest_list = rest_list.reset_index()
    rest_list = rest_list.rename(columns={'index': 'res_id'})
    rest_list.drop('res_id', axis=1, inplace=True)
    rest_list = rest_list.T
    rest_list = rest_list
    ans = rest_list.to_dict()
    res = [value for value in ans.values()]
    return res

def calcrest(restaurant,locality):
    rest_sugg = rest_search([restaurant],[locality])
    rest_list1 = rest_sugg.copy().loc[:,
                 ['name', 'address', 'locality', 'timings', 'aggregate_rating', 'url', 'cuisines','feature']]
    rest_list = pd.DataFrame(rest_list1)
    rest_list = rest_list.reset_index()
    rest_list = rest_list.rename(columns={'index': 'res_id'})
    rest_list.drop('res_id', axis=1, inplace=True)
    rest_list = rest_list.T
    rest_list = rest_list
    ans = rest_list.to_dict()
    res = [value for value in ans.values()]
    return res
    
def calcrlike(age,locality):
    rest_sugg = rest_like(age,[locality])
    rest_list1 = rest_sugg.copy().loc[:,
                 ['name', 'address', 'locality', 'timings', 'aggregate_rating', 'url', 'cuisines','feature']]
    rest_list = pd.DataFrame(rest_list1)
    rest_list = rest_list.reset_index()
    rest_list = rest_list.rename(columns={'index': 'res_id'})
    rest_list.drop('res_id', axis=1, inplace=True)
    rest_list = rest_list.T
    rest_list = rest_list
    ans = rest_list.to_dict()
    res = [value for value in ans.values()]
    return res

def url(restname,add):
    a=restname+" "+add
    b=''
    for i in range(len(a)):
      if(a[i] == ' '):
        b = b + '-'
      else:
        b = b + a[i]
    b=b.lower()
    return b

def calcorder(locality,restname):
    rest_sugg = rest_order([locality],[restname])
    rest_list1 = rest_sugg.copy().loc[:,
                 ['name', 'address', 'locality', 'timings', 'aggregate_rating', 'url', 'cuisines','feature']]
    rest_list = pd.DataFrame(rest_list1)
    rest_list = rest_list.reset_index()
    rest_list = rest_list.rename(columns={'index': 'res_id'})
    rest_list.drop('res_id', axis=1, inplace=True)
    rest_list = rest_list.T
    rest_list = rest_list
    ans = rest_list.to_dict()
    res = [value for value in ans.values()]
    return res

@app.route("/")
@app.route("/home", methods=['POST'])
def home():
    return render_template('home.html')


@app.route("/search", methods=['POST'])
def search():
    if request.method == 'POST':
        locality1 = request.form['locality']
        res = calc( locality1)
        return render_template('search.html', title='Search', restaurants=res,location=locality1)
    else:
        return redirect(url_for('home'))

@app.route("/rating", methods=['POST'])
def rating():
    if request.method == 'POST':
        people = int(request.form['people'])
        min_Price = int(request.form['min_Price'])
        max_Price =int(request.form['max_Price'])
        cuisine1 = request.form['cuisine']
        locality12 = request.form['locality']
        rating1=request.form['rating']
        resr = calcr(max_Price,people,min_Price,cuisine1,locality12,rating1)
        return render_template('rating.html', title='Rating', restaurant=resr,location=locality12)
    else:
        return redirect(url_for('home'))

@app.route("/order",methods=['POST']) 
def order(): 
    if request.method=="POST":
        locality4 = request.form['locality']
        restname = request.form['resname']
        add2=request.form['address']
        return render_template('order.html',location=locality4,namerest=restname,address=add2)
   
@app.route("/res",methods=['POST'])
def res ():
       if request.method == 'POST':
         restaurant=request.form['input-search']
         locality13 = request.form['locality']
        
         resrs = calcrest(restaurant,locality13)
         return render_template('res.html', title='Restaurant', restaurants_name=resrs,location=locality13)

       else:
         return redirect(url_for('home'))

@app.route("/like",methods=['POST'])
def like ():
    if request.method=='POST':
        age = int(request.form['age'])
        locality13 = request.form['locality']
        restname1 = request.form['resname']
        add1=request.form['address']
        link=url(restname1,add1)
        restorder = calcrest(restname1,locality13)
        resrlike = calcrlike(age,locality13)
        return render_template('like.html', title='Restaurant',res_order=restorder,address=add1,restaurants_like=resrlike,location=locality13,namerest=restname1,links=link)
    else:
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
