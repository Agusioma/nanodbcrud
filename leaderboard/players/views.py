from django.shortcuts import render
from django.http import JsonResponse
from nanodb.parser import parse
from nanodb.engine import Engine

engine = Engine()

try:
    engine.execute(parse("CREATE TABLE leaderboard (id INT PRIMARY KEY, name TEXT, score INT);"))
except:
    pass


def index(request):
    # return all players
    rows = engine.execute(parse("SELECT * FROM leaderboard;"))
    rows.sort(key = lambda x: int(x["score"]), reverse = True)
    return render(request, "players/index.html", {"players": rows})


def add_player(request):
    if request.method == "POST":
        name = request.POST.get("name")
        score = request.POST.get("score")
        try:
            # auto-increment id
            rows = engine.execute(parse("SELECT * FROM leaderboard;"))
            next_id = str(len(rows) + 1)
            sql = f"INSERT INTO leaderboard VALUES ({next_id}, '{name}', '{score}');"
            engine.execute(parse(sql))
            return JsonResponse({"status": "ok"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


def update_score(request):
    if request.method == "POST":
        player_id = request.POST.get("id")
        score = request.POST.get("score")
        sql = f"UPDATE leaderboard SET score = '{score}' WHERE id = '{player_id}';"
        engine.execute(parse(sql))
        return JsonResponse({"status": "ok"})


def delete_player(request):
    if request.method == "POST":
        player_id = request.POST.get("id")
        sql = f"DELETE FROM leaderboard WHERE id = '{player_id}';"
        engine.execute(parse(sql))
        return JsonResponse({"status": "ok"})
