import Vue from 'vue'
import Vuex from 'vuex'

import axios from 'axios'

const baseURL = 'http://localhost:5000/api/'

var axiosInstance = axios.create({
  baseURL: baseURL
})

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    n: 0,
    puzzle: null,
    start: 0,
    goal: 0,
    dist: null,
    pred: null
  },
  getters: {},
  mutations: {
    update_puzzle_size (state, n) {
      state.n = n
    },
    update_puzzle_start (state, start) {
      state.start = start
    },
    update_puzzle_goal (state, goal) {
      state.goal = goal
    },
    update_puzzle (state, puzzle) {
      state.puzzle = puzzle
    },
    update_puzzle_dist (state, dist) {
      state.dist = dist
    },
    update_puzzle_pred (state, pred) {
      state.pred = pred
    }
  },
  actions: {
    update_puzzle_size ({ commit }, n) {
      var url = '/puzzle/' + n
      axiosInstance.get(url)
        .then(function (response) {
          commit('update_puzzle_size', response.data.n)
          commit('update_puzzle_start', response.data.start)
          commit('update_puzzle_goal', response.data.goal)
          commit('update_puzzle', response.data.puzzle)
          commit('update_puzzle_dist', response.data.dist)
          commit('update_puzzle_pred', response.data.pred)
        })
        .catch(function (error) {
          console.log(error)
        }).then(function () {})
    },
    run_traverse_algorithm ({ commit, state }, algorithm) {
      var url = '/puzzle/' + algorithm
      axiosInstance.post(url, {
        n: state.n,
        start: state.start,
        goal: state.goal,
        puzzle: state.puzzle
      })
        .then(function (response) {
          commit('update_puzzle_dist', response.data.dist)
          commit('update_puzzle_pred', response.data.pred)
        })
        .catch(function (error) {
          console.log(error)
        }).then(function () {})
    },
    run_hill_climbing_algorithm ({ commit, state }, iterations) {
      var url = '/puzzle/hill-climbing'
      axiosInstance.post(url, {
        n: state.n,
        start: state.start,
        goal: state.goal,
        puzzle: state.puzzle,
        iterations: iterations
      })
        .then(function (response) {
          commit('update_puzzle_size', response.data.n)
          commit('update_puzzle_start', response.data.start)
          commit('update_puzzle_goal', response.data.goal)
          commit('update_puzzle', response.data.puzzle)
          commit('update_puzzle_dist', response.data.dist)
          commit('update_puzzle_pred', response.data.pred)
        })
        .catch(function (error) {
          console.log(error)
        }).then(function () {})
    },

    run_genetic_algorithm ({ commit, state }, dict) {
      var url = '/puzzle/genetic-algorithm'
      axiosInstance.post(url, {
        n: state.n,
        start: state.start,
        goal: state.goal,
        puzzle: state.puzzle,
        populationSize: dict.populationSize,
        survivalRate: dict.survivalRate,
        secondarySurvivalRate: dict.secondarySurvivalRate,
        mutationRate: dict.mutationRate,
        epochs: dict.epochs
      })
        .then(function (response) {
          commit('update_puzzle_size', response.data.n)
          commit('update_puzzle_start', response.data.start)
          commit('update_puzzle_goal', response.data.goal)
          commit('update_puzzle', response.data.puzzle)
          commit('update_puzzle_dist', response.data.dist)
          commit('update_puzzle_pred', response.data.pred)
        })
        .catch(function (error) {
          console.log(error)
        }).then(function () {})
    }
  }
})
