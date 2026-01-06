from flask import Flask,render_template,redirect,request
app=Flask(__name__)
symbol_specifier=0 
deafult_symbol="O"
player_1_points=[]
player_2_points=[]
start="No"
player_1_id=None
player_2_id=None
play_ground=[[deafult_symbol]*3 for _ in range (3)]
wininers=[]
player_won=None#Storing the id of the winnner
win1=0
win2=0
match_rounds="" 
turn=""
#Putting win1 and win2 global to make them staic and don't change when route is called.
def reset_all():#To rset the whole game.
    global win1
    global win2
    global start
    global player_won
    global wininers
    win1=0
    win2=0
    start="No"
    player_won=None
    wininers=[]
    reset_board()#Inheritance of functions.Hehe
def reset_board():#It is decleared globally so all routes can use it.To resret the board(playground and items)
    global symbol_specifier
    global play_ground
    global player_1_points
    global player_2_points
    play_ground=[[deafult_symbol]*3 for _ in range (3)] 
    player_1_points=[] 
    player_2_points=[] 
    symbol_specifier=0
#Running the web the main route:
@app.route("/",methods=["GET","POST"])
def maingame():
    global start
    global play_ground
    global wininers
    global player_won
    global turn
    return render_template("index.html",play_ground=play_ground,start=start,wininers=wininers,player_won=player_won,turn=turn)
#The marking and winner deciding route for functionality:
@app.route("/marks/<int:i>/<int:j>")
def marker_on_click(i,j):
    #Initializing variables!
    global play_ground
    global wininers
    global symbol_specifier
    global player_1_points
    global player_2_points
    global player_1_id
    global player_2_id
    global start
    global player_won
    global win1
    global win2
    global match_rounds
    global turn
    #Local Variables!
    Player_1_symbol="✓"
    Player_2_symbol="✘"
    wining_points=[#The winning points.(2d list)
    [(0,0),(0,1),(0,2)],[(1,0),(1,1),(1,2)],[(2,0),(2,1),(2,2)],
    [(0,0),(1,0),(2,0)],[(0,1),(1,1),(2,1)],[(0,2),(1,2),(2,2)],
    [(0,0),(1,1),(2,2)],[(0,2),(1,1),(2,0)],
    ]#We need to write it all beacuse if we use for i in play_ground and j in play_ground[i] we ant seperate the sets of winign points.
    #Main Program!
    if play_ground[i][j]==deafult_symbol and len(wininers) < int(match_rounds):#int of str.
        symbol_specifier+=1
        if symbol_specifier%2==0:#Chaning the icon on the click.
            play_ground[i][j]=Player_2_symbol
            turn=player_1_id
            player_2_points.append((i,j))#Adding the points to player2's list
        else:
            play_ground[i][j]=Player_1_symbol
            turn=player_2_id
            player_1_points.append((i,j))#Adding the points to player1's list
        deafult_ground=[[i,j]for i in range(len(play_ground)) for j in range(len(play_ground[i])) if play_ground[i][j]==deafult_symbol]#Storing remaining points on the (board/playgroud)
        for w in wining_points:#Iterating over inner cells w is 1d list.
            if all(wl in player_1_points for wl in w):#(If all of the tuples indexes of ->wl(,) are in player1's list then declearing winner.
                win1+=1
                wininers.append(player_1_id)
                reset_board()
                break
            elif all(wl in player_2_points for wl in w):#(If all of the tuples indexes of ->wl(,) are in player1's list then declearing winner.
                win2+=1
                wininers.append(player_2_id)#Storing in the list.
                reset_board()
                break
            elif len(deafult_ground)==0:#To check if it's a tie.
                wininers.append("Tie")#Storing in the list.
                reset_board()
                break
        if len(wininers)==int(match_rounds):#int of str
            if win1 > win2:
                player_won=player_1_id
            elif win2 > win1:
                player_won=player_2_id
            else: 
                player_won="Tie"
    return redirect("/")
@app.route("/reset")
def reset():
    global player_won
    if player_won:
        reset_all()
    else:
        reset_board()
    return redirect("/")
@app.route("/players",methods=["GET","POST"])
def player_names():
    global start
    global player_1_id
    global player_2_id
    global match_rounds
    global turn
    if request.method=="POST":
        player_1_id=request.form.get("Player1_id")
        player_2_id=request.form.get("Player2_id")
        rounds=request.form.get("Field")#None Type
        match_rounds=str(rounds)#None type->str and saving in str.
        start="Yes"
        turn=player_1_id
    return redirect("/")
if __name__=="__main__":
    app.run(debug=True,port=2130) 