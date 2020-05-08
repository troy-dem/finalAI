import cherrypy
import json
import random
import sys


class Server:
    @cherrypy . expose
    @cherrypy.tools.json_in()
    @cherrypy . tools . json_out ()
    def move (self):
        # Deal with CORS
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        if cherrypy.request.method == "OPTIONS":
            return ''
        #get game status
        body = cherrypy.request.json
        board= body["game"]
        if body["you"]==body["players"][0]:
            me = 0
        else:
            me=1

        #création liste des directions 
        i=-1
        j=-1
        directions=[]
        for i in range(-1,2):
            for j in range(-1,2):
                if i!=0 or j!=0:
                    directions.append((i,j))
                j+=1
            i+=1
        
        
        #statégie
        def compute_score(line, tower):
            line= line
            tower= tower
            score=0
            if len(board[line][tower]) != 0:
                owner= board[line][tower][-1]
                ownlen= len(board[line][tower])
                for direction in directions:
                    if line+direction[0] not in [-1,9] and tower+direction[1] not in [-1,9]:
                        target = board[line+direction[0]][tower+direction[1]]
                        if len(target) != 0:
                            if len(target) == 5-ownlen:
                                if target[-1] != owner:
                                    score+=1
                                else:
                                    score-=5
                            else:
                                if target[-1] != owner:
                                    score+=6
                                else:
                                    score-=2
                            if owner!= me:
                                score= (score*(-1))
            return(score)

        def spotscore(board):
            board = board
            spotList=[]
            i=0
            for line in board:
                j=0
                spotLine=[]
                for tower in line:
                    if len(board[i][j]) !=0:
                        spotLine.append(compute_score(i,j))
                    else:
                        spotLine.append(100)
                    j+=1
                """ with open("spotline.txt", "a") as f:
                                data= "{}\n".format(spotLine)
                                f.write(data)  """
                spotList.append(spotLine)
                i+=1
            with open("spotlist.txt", "a") as f:
                                data= "{}\n".format(spotList)
                                f.write(data) 
            return (spotList)
        
        def choose_spot(L):
            spt_list= L
            choice = spt_list[0][0]
            i=0
            for line in spt_list:
                j=0
                for score in line:
                    if abs(score)<abs(choice):
                        choice = score
                        out = (i,j)
                    j+=1
                i+=1
            return(out)
        
        def choose_move(a):
            line, tower= a
            coup={}
            if len(board[line][tower]) != 0:
                owner= board[line][tower][-1]
                ownlen= len(board[line][tower])
                for direction in directions:
                    try:
                        target = board[line+direction[0]][tower+direction[1]]
                        if owner != me:
                            if me == target[-1]:
                                coup = {"move": {"from": [line+direction[0], tower+direction[1]],"to": [line, tower]},"message": "smart move"}
                        else:
                            if me != target[-1]:
                                coup = {"move": {"from": [line, tower],"to": [line+direction[0], tower+direction[1]]},"message": "smart move"}
                    except:
                        pass
                for direction in directions:
                    try:
                        target = board[line+direction[0]][tower+direction[1]]
                        if len(target) == 5-ownlen:
                            if owner != me:
                                if me == target[-1]:
                                    coup = {"move": {"from": [line+direction[0], tower+direction[1]],"to": [line, tower]},"message": "smart move"}
                            else:
                                if me != target[-1]:
                                    coup = {"move": {"from": [line, tower],"to": [line+direction[0], tower+direction[1]]},"message": "smart move"}
                    except:
                        pass
                
            return(coup)
        
        def check_move(move):
            coup = move
            try:
                originLine = coup["move"]["from"][0]
                originCol = coup["move"]["from"][1]
                destLine= coup["move"]["to"][0]
                destCol= coup["move"]["to"][1]
                total_length=len(body["game"][originLine][originCol]) + len(body["game"][destLine][destCol])
                if total_length <5 and total_length>0:
                    return(True)
            except:
                return(False)

        def random_move():
            bad=True
            while bad:
                #génératuer de coup aléatoire
                line = random.randint(0, 8)
                col = random.randint(0, 8)
                destdir=random.choice(directions)
                coup = {"move": {"from": [line, col],"to": [line+destdir[0], col+destdir[1]]},"message": "random move"}

                #vérification du coup
                try:
                    originlen=len(body["game"][line][col])
                    owner = body["game"][line][col][-1]
                    if originlen != 0:
                        destlen=len(body["game"][line+destdir[0]][col+destdir[1]])
                        if destlen != 0 and line+destdir[0] not in [-1,9] and col+destdir[1] not in [-1,9]:
                            if (originlen+destlen <= 5 and owner==me):
                                bad=False
                                return(coup)
                except:
                    bad=True
        def safe_move():
            bad=True
            while bad:
                #génératuer de coup aléatoire
                line = random.randint(0, 8)
                col = random.randint(0, 8)
                destdir=random.choice(directions)
                coup = {"move": {"from": [line, col],"to": [line+destdir[0], col+destdir[1]]},"message": "random move"}

                #vérification du coup
                try:
                    originlen=len(body["game"][line][col])
                    if originlen != 0:
                        destlen=len(body["game"][line+destdir[0]][col+destdir[1]])
                        if destlen != 0 and line+destdir[0] not in [-1,9] and col+destdir[1] not in [-1,9]:
                            if (originlen+destlen <= 5):
                                bad=False
                                return(coup)
                except:
                    bad=True
        #appel des fonctions
        spot_list = spotscore(board)
        spot = choose_spot(spot_list)
        move = choose_move(spot)
        rmove=random_move()
        if check_move(move):
            return(move)
        elif check_move(rmove):
            return(rmove)
        return safe_move()
        

    @cherrypy . expose
    def ping (self):
        return("pong")



port = int(sys.argv[1])
cherrypy.config.update({'server.socket_port': port})
cherrypy.quickstart(Server())