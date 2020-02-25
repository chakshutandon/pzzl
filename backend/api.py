from flask import Blueprint, jsonify, request
from random import randint

from .puzzle import Puzzle
from .graph import Graph

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/random')
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)

@bp.route('/puzzle/<int:n>', methods=['GET'])
def random_puzzle(n):
    p = Puzzle(n)
    g = p.convert_to_graph()
    dist, pred = g.BFS(p.start)
    dist = [None if el == float("inf") else el for el in dist]
    response = {
        'n': p.n,
        'start': p.start,
        'goal': p.goal,
        'puzzle': p.puzzle,
        'dist': dist,
        'pred': pred
    }
    return jsonify(response)

@bp.route('/puzzle/bfs', methods=['POST'])
def bfs():
    data = request.json
    p = Puzzle(puzzle=data["puzzle"])
    g = p.convert_to_graph()
    dist, pred = g.BFS(data["start"])
    dist = [None if el == float("inf") else el for el in dist]
    response = {
        'dist': dist,
        'pred': pred
    }
    return jsonify(response)

@bp.route('/puzzle/spf', methods=['POST'])
def spf():
    data = request.json
    p = Puzzle(puzzle=data["puzzle"])
    g = p.convert_to_graph()
    dist, pred = g.dijkstra(data["start"], data["goal"])
    dist = [None if el == float("inf") else el for el in dist]
    response = {
        'dist': dist,
        'pred': pred
    }
    return jsonify(response)

@bp.route('/puzzle/a-star', methods=['POST'])
def a_star():
    response = {}
    return jsonify(response)

@bp.route('/puzzle/hill-climbing', methods=['POST'])
def hill_climbing():
    data = request.json
    iterations = int(data["iterations"])
    p = Puzzle(puzzle=data["puzzle"])
    p.hill_climbing(iterations)
    g = p.convert_to_graph()
    dist, pred = g.BFS(data["start"])
    dist = [None if el == float("inf") else el for el in dist]
    response = {
        'n': p.n,
        'start': p.start,
        'goal': p.goal,
        'puzzle': p.puzzle,
        'dist': dist,
        'pred': pred
    }
    return jsonify(response)

@bp.route('/puzzle/genetic-algorithm', methods=['POST'])
def genetic_algorithm():
    data = request.json

    population_size = int(data["populationSize"])
    survival_rate = float(data["survivalRate"])
    secondary_survival_rate = float(data["secondarySurvivalRate"])
    mutation_rate = float(data["mutationRate"])
    epochs = int(data["epochs"])

    p = Puzzle(puzzle=data["puzzle"])
    p.genetic_algorithm(population_size, survival_rate, secondary_survival_rate, mutation_rate, epochs)

    g = p.convert_to_graph()
    dist, pred = g.BFS(data["start"])
    dist = [None if el == float("inf") else el for el in dist]

    response = {
        'n': p.n,
        'start': p.start,
        'goal': p.goal,
        'puzzle': p.puzzle,
        'dist': dist,
        'pred': pred
    }
    return jsonify(response)
