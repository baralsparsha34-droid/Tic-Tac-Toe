try:  
    from flask import Flask,render_template,redirect,request
    from flask_sqlalchemy import SQLAlchemy
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///Tic-tac-toe_Storage.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    database=SQLAlchemy(app)
    class Tic_Tac_Toe (database.Model):
        sn=database.Column(database.Integer,primary_key=True)
        Winnner_pattern=database.Column(database.String,nullable=True)
        Winnner=database.Column(database.String,nullable=True)
        pass
except ModuleNotFoundError as mold:
    print("Module not found dude",mold)
except Exception as exe:
    print("Unknonuured!",exe)
player_won=None
win1=0
win2=0
tie=0
symbol_specifier=0 
Player_1_symbol="✓"
Player_2_symbol="✘"
deafult_symbol="O"
play_ground=[[deafult_symbol]*3 for _ in range (3)]
wining_points=[
    [(0,0),(0,1),(0,2)],[(1,0),(1,1),(1,2)],[(2,0),(2,1),(2,2)],
    [(0,0),(1,0),(2,0)],[(0,1),(1,1),(2,1)],[(0,2),(1,2),(2,2)],
    [(0,0),(1,1),(2,2)],[(0,2),(1,1),(2,0)],
]#We need to write it all beacuse if we use for i in play_ground and j in play_ground[i] we ant seperate the sets of winign points.
player_1_points=[]
player_2_points=[]
wininers=[]
start="No"
player_1_id=None
player_2_id=None
print(play_ground)#For making sure!
def reset_board():
    global symbol_specifier
    global play_ground
    global win2
    global win1
    global tie
    global tie
    global player_1_points
    global player_2_points
    play_ground=[[deafult_symbol]*3 for _ in range (3)]  
    win1=0
    win2=0
    tie=0
    player_2_points=[]
    player_1_points=[]
    symbol_specifier=0
#Running the web the main route:
@app.route("/",methods=["GET","POST"])
def maingame():
    global start
    global play_ground
    global wininers
    return render_template("index.html",play_ground=play_ground,start=start,wininers=wininers)
#The marking and winner deciding route for functionality:
@app.route("/marks/<int:i>/<int:j>")
def marker_on_click(i,j):
    global wininers
    global symbol_specifier
    global Player_2_symbol
    global Player_1_symbol
    global play_ground
    global win1
    global win2
    global tie
    global player_won
    global wining_points
    global player_1_points
    global player_2_points
    global player_1_id
    global player_2_id
    global start
    deafult_ground=[]
    if play_ground[i][j]==deafult_symbol:
        deafult_ground=[[i,j]for i in range(len(play_ground)) for j in range(len(play_ground[i])) if play_ground[i][j]==deafult_symbol]
        symbol_specifier+=1
        if symbol_specifier%2==0:
            play_ground[i][j]=Player_2_symbol
            player_2_points.append((i,j))
        else:
            play_ground[i][j]=Player_1_symbol
            player_1_points.append((i,j))
        for w in wining_points:
            if all(wl in player_1_points for wl in w):
                win1+=1
                wininers.append(player_1_id)
                print("{0} won".format(player_1_id))
                reset_board()
            elif all(wl in player_2_points for wl in w):
                win2+=1
                wininers.append(player_2_id)
                print("{0} won".format(player_2_id))
                reset_board()
            else:
                if len(deafult_ground)==0:
                    tie+=1
                    wininers.append("Tie")
                    print("None won")
                    reset_board()
        if win1 or win2 or tie:
            if win1 > win2 and tie:
                player_won=player_1_id
            elif win2 > win1 and tie:
                player_won=player_2_id
            elif tie > win1 and win2:
                player_won="Tie"
            else:
                pass
            print(player_won) 
    print(deafult_ground)
    print(w)
    print(symbol_specifier)
    return redirect("/")
@app.route("/reset")
def reset():
    reset_board()
    return redirect("/")
@app.route("/players",methods=["GET","POST"])
def player_names():
    global start
    global player_1_id
    global player_2_id
    if request.method=="POST":
        player_1_id=request.form.get("Player1_id")
        player_2_id=request.form.get("Player2_id")
        start="Yes"
        print(player_1_id)
        print(player_2_id)
        print(start)
    return redirect("/")
if __name__=="__main__":
    with app.app_context():
        database.create_all()
    app.run(debug=True,port=2130) 