<template>
  <b-modal id="traverse_algorithm_modal" @ok="handleOk">
    <b-form>
      <b-form-select
        id="traverse-method"
        v-model="method"
        :options="methods"
      ></b-form-select>
    </b-form>
  </b-modal>
</template>

<script>
export default {
  data () {
    return {
      method: 'bfs',
      methods: [
        { value: 'bfs', text: 'Breadth-First Search (BFS)' },
        { value: 'spf', text: 'Shortest Path First (SPF)' },
        { value: 'a-star', text: 'A*' }
      ]
    }
  },
  computed: {
  },
  methods: {
    handleOk () {
      if (this.method) {
        this.$store.dispatch('run_traverse_algorithm', this.method)
      }
    }
  }
}
</script>
