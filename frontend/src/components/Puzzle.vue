<template>
  <div class="container">
    <canvas id="canvas"></canvas>
    <div class="row">
      <div class="mx-auto" id="container"></div>
      <div class="mx-auto" id="container2"></div>
    </div>
  </div>
</template>

<script>

function fillPuzzle (container, puzzle, start, goal) {
  var n = puzzle.length
  container.innerHTML = ''
  container.style.setProperty('--grid-rows', n)
  container.style.setProperty('--grid-cols', n)
  for (var i = 0; i < n; i++) {
    for (var j = 0; j < n; j++) {
      let cell = document.createElement('div')
      var idx = i * n + j
      cell.id = idx
      cell.style.height = '1.5em'
      cell.style.width = '1.5em'
      cell.innerText = puzzle[i][j]
      cell.classList.add('grid-item')
      if (idx === start) {
        cell.classList.add('bg-success')
      }
      if (idx === goal) {
        cell.classList.add('bg-danger')
      }
      container.appendChild(cell)
    }
  }
}

function fillPathMatrix (cont, dist) {
  var n = Math.sqrt(dist.length)
  cont.innerHTML = ''
  cont.style.setProperty('--grid-rows', n)
  cont.style.setProperty('--grid-cols', n)
  for (var i = 0; i < n; i++) {
    for (var j = 0; j < n; j++) {
      let cell = document.createElement('div')
      var idx = i * n + j
      cell.id = idx
      cell.style.height = '1.5em'
      cell.style.width = '1.5em'
      if (dist[idx]) {
        cell.innerText = dist[idx]
      } else {
        cell.innerText = 'X'
      }
      cell.classList.add('grid-item')
      cont.appendChild(cell)
    }
  }
}

function getCellCenterX (container, idx) {
  return container.childNodes[idx].offsetLeft + container.childNodes[idx].offsetWidth / 2 - container.offsetLeft
}

function getCellCenterY (container, idx) {
  return container.childNodes[idx].offsetTop + container.childNodes[idx].offsetHeight / 2 - container.offsetTop
}

function fillCanvas (canvas, container, pred) {
  var ctx = canvas.getContext('2d')
  ctx.canvas.style.position = 'absolute'
  ctx.canvas.style.top = container.offsetTop + 'px'
  ctx.canvas.style.left = container.offsetLeft + 'px'
  ctx.canvas.height = container.offsetHeight
  ctx.canvas.width = container.offsetWidth

  var path = []
  var idx = pred.length - 1
  if (!pred[idx]) {
    return
  }
  while (pred[idx]) {
    path.push(idx)
    idx = pred[idx]
  }
  path.push(idx)
  path = path.reverse()

  var firstElX = getCellCenterX(container, 0)
  var firstElY = getCellCenterY(container, 0)
  var secondElX = 0
  var secondElY = 0

  ctx.beginPath()
  ctx.moveTo(firstElX, firstElY)

  for (var i = 0; i < path.length; i++) {
    secondElX = getCellCenterX(container, path[i])
    secondElY = getCellCenterY(container, path[i])
    ctx.lineTo(secondElX, secondElY)
    ctx.stroke()
    firstElX = secondElX
    firstElY = secondElY
  }
}

export default {
  data: function () {
    return {}
  },
  components: {
  },
  computed: {
    start: function () {
      return this.$store.state.start
    },
    goal: function () {
      return this.$store.state.goal
    },
    pred: function () {
      return this.$store.state.pred
    }
  },
  created () {
    this.$store.dispatch('update_puzzle_size', 5)
  },
  mounted () {
    var container = document.getElementById('container')
    var container2 = document.getElementById('container2')
    var canvas = document.getElementById('canvas')
    this.$store.watch(
      (state, getters) => state.puzzle,
      (newValue, oldValue) => {
        fillPuzzle(container, newValue, this.start, this.goal)
        fillPathMatrix(container2, this.$store.state.dist)
        fillCanvas(canvas, container, this.pred)
      }
    )
  }
}
</script>

<style scoped>
  #container {
    display: grid;
    grid-gap: 1em;
    grid-template-rows: repeat(var(--grid-rows), 0fr);
    grid-template-columns: repeat(var(--grid-cols), 0fr);
  }
  .grid-item {
    padding: 1em;
    border: 1px solid #ddd;
    text-align: center;
  }
  #container2 {
    display: grid;
    grid-gap: 1em;
    grid-template-rows: repeat(var(--grid-rows), 0fr);
    grid-template-columns: repeat(var(--grid-cols), 0fr);
  }
</style>
