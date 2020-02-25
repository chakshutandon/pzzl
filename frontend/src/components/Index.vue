<template>
  <div>
    <Header></Header>
    <Puzzle class="p-4"></Puzzle>
    <Footer></Footer>
  </div>
</template>

<script>
import Header from './Header'
import Footer from './Footer'
import Puzzle from './Puzzle'

export default {
  data: function () {
    return {}
  },
  components: {
    Header,
    Footer,
    Puzzle
  },
  computed: {
    puzzle_size () {
      return this.$store.state.puzzle_size
    }
  }
}
</script>
