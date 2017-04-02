from flask import Flask, render_template, request, session, url_for, redirect, Markup
import json, os, random

app = Flask(__name__)

@app.route('/')
def homeFunction():
	if session.get('wrong_password'):
		return "wrong password"
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return redirect('/prizes/')

@app.route('/profile/')
def profileFunction():

    if not session.get('logged_in'):
        return render_template('login.html')

    else:



        index = int(session.get('id_user'))

        users = readJson("users.json")['users']


        generatedBody = '''

                        <div class="maxicenter row row2">
                            <div class="col-sm-4 panel">
                                <div class="frontpage_square thumbnail">
                                  <div class="cntr afterDiv">
                                      <p class="lessSpace"><b>'''+users[index]['name']+'''</b></p>
                                      <p class="lessSpace"><b>'''+users[index]['email']+'''</b></p>
                                      <p class="lessSpace">'''+str(users[index]['coins'])+'''<img class="coin" src="/static/media/coin.png"></p>
                                  </div>
                                </div>
                            </div>
                        </div>



                        '''

        generatedBody = Markup(generatedBody)


        return render_template('profile.html', cool_body = generatedBody)






@app.route('/prizes/')
def prizesFunction():

    generatedBody = '<div class="row row2">'

    # A list of the prizes
    prizes = readJson("prizes.json")['prizes']




    for prize in prizes:

        generatedBody += '''


    <div class="col-sm-4 panel">
            <a style="text-decoration:none" href="/prizes/'''+prize['id']+'''">
                <div class="frontpage_square thumbnail">

                  <div class="prizeimg" align="center">
                    <img src="'''+prize['img_url']+'''" class="imgSize"">
                  </div>
                  <div class="cntr afterDiv">
                  <p class="lessSpace"><b>'''+prize['name']+'''</b></p>
                  <p class="lessSpace">'''+prize['price']+'''<img class="coin" src="/static/media/coin.png"></p>
                  </div>
                </div>
            </a>

    </div>

                         '''

    generatedBody += '</div>'
    generatedBody = Markup(generatedBody)


    return render_template('prizes.html', cool_body = generatedBody)

@app.route('/prizes/<id>')
def singlePrizeFunction(id):


        prizes = readJson("prizes.json")['prizes']


        generatedBody = '''
                        <div class="maxicenter row row2">
                            <div class="col-sm-4 panel">
                                        <div class="frontpage_square thumbnail">

                                          <div class="prizeimg" align="center">
                                            <img src="'''+prizes[int(id)]['img_url']+'''" class="imgSize"">
                                          </div>
                                          <div class="cntr afterDiv">
                                              <p class="lessSpace"><b>'''+prizes[int(id)]['name']+'''</b></p>
                                              <p class="lessSpace">'''+prizes[int(id)]['price']+'''<img class="coin" src="/static/media/coin.png"></p>
                                          <div class="topDistance">
                                                <a href="/prizes/redeem/'''+id+'''">
                                                    <input type="submit" class="btn btn-primary" value="Redeem" />
                                                </a>

                                          </div>
                                         </div>
                                         </div>

                                </div>
                            </div>


                     '''


        generatedBody = Markup(generatedBody)


        return render_template('prizes.html', cool_body = generatedBody)




@app.route('/prizes/redeem/<id>')
def redeemFunction(id):

    if not session.get('logged_in'):
        return render_template('login.html')
    else:

        index = int(session.get('id_user'))

        users = readJson("users.json")

        prizes = readJson("prizes.json")['prizes']

        capital = users['users'][int(index)]['coins']

        if capital < int(prizes[int(id)]['price']):
            generatedBody = '''
                            <div class="maxicenter row row2">
                                <div class="col-sm-4 panel">
                                            <div class="frontpage_square thumbnail">

                                              <div class="prizeimg" align="center">
                                                <img src="'''+prizes[int(id)]['img_url']+'''" class="imgSize"">
                                              </div>
                                              <div class="cntr afterDiv">
                                                  <p class="lessSpace"><b>'''+prizes[int(id)]['name']+'''</b></p>
                                                  <p class="lessSpace">'''+prizes[int(id)]['price']+'''<img class="coin" src="/static/media/coin.png"></p>
                                                  <p style="color:red">You don't have enough coins</p>
                                              <div class="topDistance">
                                                    <a href="/prizes/redeem/'''+id+'''">
                                                        <input type="submit" class="btn btn-primary" value="Redeem" />
                                                    </a>

                                              </div>
                                             </div>
                                             </div>

                                    </div>
                                </div>


                         '''
        else:

                    users['users'][int(index)]['coins'] = int(users['users'][int(index)]['coins']) - int(prizes[int(id)]['price'])

                    with open('users.json', 'w') as f:
                        json.dump(users, f)



                    generatedBody = '''
                                    <div class="maxicenter row row2">
                                        <div class="col-sm-4 panel">
                                                    <div class="frontpage_square thumbnail">

                                                      <div class="prizeimg" align="center">
                                                        <img src="'''+prizes[int(id)]['img_url']+'''" class="imgSize"">
                                                      </div>
                                                      <div class="cntr afterDiv">
                                                          <p class="lessSpace"><b>'''+prizes[int(id)]['name']+'''</b></p>
                                                          <p class="lessSpace">'''+prizes[int(id)]['price']+'''<img class="coin" src="/static/media/coin.png"></p>
                                                          <p style="color:green">The item has been succesfully redeemed</p>
                                                      <div class="topDistance">
                                                            <a href="/prizes/redeem/'''+id+'''">
                                                                <input type="submit" class="btn btn-primary" value="Redeem" />
                                                            </a>

                                                      </div>
                                                     </div>
                                                     </div>

                                            </div>
                                        </div>


                                 '''

        generatedBody = Markup(generatedBody)


        return render_template('prizes.html', cool_body = generatedBody)



@app.route('/exercises/')
def exercisesFunction():

    generatedBody = '<div class="row row2">'

    # A list of the prizes
    categories = readJson("questions.json")
    for category in categories:
        generatedBody += '''

    <div class="col-sm-4 panel">
                <a style="text-decoration:none" href="/exercises/'''+str(categories[category]["id"])+'''">
                <div class="frontpage_square thumbnail">
                  <div class="prizeimg" align="center">
                    <img src="/static/media/'''+str(category).lower()+'''.jpg" class="imgSize"">
                    <p class="space"><b>'''+str(category)+'''</b></p>
                  </div>
                </div>
                </a>
            </a>

    </div>

                         '''

    generatedBody += '</div>'
    generatedBody = Markup(generatedBody)


    return render_template('exercises.html', cool_body = generatedBody)


@app.route('/exercises/<id>')
def singleExercisesFunction(id):

    categories = readJson("questions.json")
    for category in categories:
        if str(categories[category]["id"]) == str(id):
            numQ = str(len(categories[category]["questions"]))
            return str(categories[category]["questions"][str(random.randint(1,int(numQ)))])


@app.route('/about_us/')
def about_usFunction():
	return render_template('about_us.html')

@app.route('/test/<variable>')
def hello_name(variable):
    return render_template('test.html', message = variable)

@app.route('/login', methods=['POST'])
def login():
    users = readJson("users.json")['users']

    for user in users:
        if request.form['password'] == user['password'] and request.form['username'] ==  user['username']:
            session['logged_in'] = True
            session['id_user'] = user['id']
            return homeFunction()

    session['wrong_password'] = True
    return homeFunction()

@app.route('/logout')
def logout():
		session.clear()
		return redirect(url_for("homeFunction"))

def readJson(path):
	with open(path) as json_data:
		return json.load(json_data)




if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
