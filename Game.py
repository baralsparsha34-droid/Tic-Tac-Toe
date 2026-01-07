from flask import Flask,render_template,redirect,request,session
import os
app=Flask(__name__)
app.secret_key="Boar@2130"
#This is a session based variable game sessiona are global but acts as local. they cna be accesed anywhere
deafult_symbol="O"#This is only global because it is needed for many functions and routes but never chnages.
#Putting win1 and win2 global to make them staic and don't change when route is called.
def reset_all():#To rset the whole game.
    session["win1"]=0
    session["win2"]=0
    session["permission"]="No"
    session["player_won"]=None
    session["winners"]=[]
    session["symbol_specifier"]=0
    reset_board()#Inheritance of functions.Hehe
def reset_board():#It is decleared globally so all routes can use it.To resret the board(playground and items)
    session["The_Board"]=[[deafult_symbol]*3 for _ in range (3)] 
    session["player_1_points"]=[]
    session["player_2_points"]=[]
 
#Running the web the main route:
@app.route("/",methods=["GET","POST"])
def maingame():
    #Making variables of the session key if becuase in the first the game is not started.
    play_ground=session.get("The_Board")
    start=session.get("permission") if session.get("permission") else "No"#checking if permisiion is updated or not if not it is no by deafult.
    champs=session.get("winners")
    champion=session.get("player_won")
    turn=session.get("offer") 
    return render_template("index.html",play_ground=play_ground,start=start,champs=champs,champion=champion,turn=turn)
#The marking and winner deciding route for functionality:
@app.route("/marks/<int:i>/<int:j>")
def marker_on_click(i,j):
    #Initializing variables!
    #Local Variables!
    Player_1_symbol="✓"
    Player_2_symbol="✘"
    check=0
    wining_points=[#The winning points.(2d list)
    [(0,0),(0,1),(0,2)],[(1,0),(1,1),(1,2)],[(2,0),(2,1),(2,2)],
    [(0,0),(1,0),(2,0)],[(0,1),(1,1),(2,1)],[(0,2),(1,2),(2,2)],
    [(0,0),(1,1),(2,2)],[(0,2),(1,1),(2,0)],
    ]#We need to write it all beacuse if we use for i in play_ground and j in play_ground[i] we ant seperate the sets of winign points.
    #Main Program!
    #Symbol Logic adn exchanging turns!
    if session["The_Board"][i][j]==deafult_symbol and len(session["winners"]) < session["match_rounds"]:#int of str.
        session["symbol_specifier"]+=1
        if session["symbol_specifier"]%2==0:#Chaning the icon on the click.
            session["The_Board"][i][j]=Player_2_symbol
            session["offer"]=session['player_1_id']
            session["player_2_points"].append((i,j))#Adding the points to player1's list
        else:
            session["The_Board"][i][j]=Player_1_symbol
            session["offer"]=session['player_2_id']
            session["player_1_points"].append((i,j))#Adding the points to player2's list
        deafult_ground=[[i,j]for i in range(len(session["The_Board"])) for j in range(len(session["The_Board"][i])) if session["The_Board"][i][j]==deafult_symbol]#Storing remaining points on the (board/playgroud)
        #Winning Logic!
        for w in wining_points:#Iterating over inner cells w is 1d list.
            if all(wl in session["player_1_points"] for wl in w):#(If all of the tuples indexes of ->wl(,) are in player1's list then declearing winner.
                session["win1"]+=1
                session["winners"].append(session['player_1_id'])
                reset_board()
                check=1#Checking for win.
                break
            elif all(wl in session["player_2_points"] for wl in w):#(If all of the tuples indexes of ->wl(,) are in player1's list then declearing winner.
                session["win2"]+=1
                check=1#Checking for win.
                session["winners"].append(session['player_2_id'])#Storing in the list.
                reset_board()
                break
        if len(deafult_ground)==0 and  not check :#To check if it's a tie if check is false.
            session["winners"].append("Tie")#Storing in the list.
            reset_board()
        #Finial winner logic!
        if len(session["winners"])==session["match_rounds"]:#int of str
            if session["win1"] > session["win2"]:
                session["player_won"]=session['player_1_id']
            elif session["win2"] > session["win1"]:
                session["player_won"]=session['player_2_id']
            else: 
                session["player_won"]="Tie"
    return redirect("/")
#Route for html buttons.
@app.route("/reset")
def reset():
    if session["player_won"]:
        reset_all()#To restart all
    else:
        reset_board()#To reset board and turn to deafult
    return redirect("/")
@app.route("/players",methods=["GET","POST"])
def player_names():
    global deafult_symbol
    #Asking the player's name and deatils.
    if request.method=="POST":
        session["player_1_id"]=request.form.get("Player1_id")
        session["player_2_id"]=request.form.get("Player2_id")
        session["rounds"]=request.form.get("Field")#None Type
        if session["rounds"] and str(session["rounds"]).isdigit():
            session["match_rounds"]=int(session["rounds"])
        #None type->str and saving in str.
    #Checking
    if session["match_rounds"]>=1:#Declearing all session keys after game starts
        session["permission"]="Yes"
        session["offer"]=session["player_1_id"]
        session["The_Board"]=[[deafult_symbol for _ in range(3)] for _ in range(3)]
        session["winners"]=[]
        session["player_won"]=None
        session["symbol_specifier"]=0
        session["player_1_points"]=[]
        session["player_2_points"]=[]
        session["win2"]=0
        session['win1']=0
    return redirect("/")
#logic to run the app!
if __name__=="__main__":
    ported=int(os.environ.get("PORT",2130))
    app.run(debug=True,port=ported,host="0.0.0.0") 