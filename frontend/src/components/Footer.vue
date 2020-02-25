<template>
  <div>
    <footer class="navbar-dark bg-dark fixed-bottom">
      <div class="container p-2">
        <b-form inline class="justify-content-center">
          <label class="text-light" for="puzzle-size">Puzzle Size:</label>
          <b-form-select class="ml-sm-2 mr-sm-2" id="puzzle-size" v-model="size" :options="sizes" v-on:change="update_puzzle_size($event)"></b-form-select>
          <b-button class="ml-sm-2 mr-sm-2" v-b-modal="'traverse_algorithm_modal'">Traverse Puzzle</b-button>
          <b-button class="ml-sm-2 mr-sm-2" v-b-modal="'optimize_param_modal'">Optimize Puzzle</b-button>
        </b-form>
        <TraverseModal></TraverseModal>
        <OptimizeModal></OptimizeModal>
      </div>
    </footer>
  </div>
</template>

<script>
import TraverseModal from './TraverseModal'
import OptimizeModal from './OptimizeModal'

export default {
  data () {
    return {
      size: 5,
      sizes: [
        { value: 5, text: '5' },
        { value: 7, text: '7' },
        { value: 9, text: '9' },
        { value: 11, text: '11' }
      ]
    }
  },
  components: {
    TraverseModal,
    OptimizeModal
  },
  computed: {
    isShowPathLengthDisabled: function () {
      return !(this.$store.state.dist)
    }
  },
  methods: {
    update_puzzle_size (event) {
      this.$store.dispatch('update_puzzle_size', event)
    }
  }
}
</script>
