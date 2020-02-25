<template>
  <b-modal id="optimize_param_modal" @ok="handleOk">
    <b-form>
      <b-form-select id="optimize-method" v-model="method" :options="methods"></b-form-select>
      <div class="mt-2" v-if="method == 'hill_climbing'">Iterations: {{ hillClimbingIterations }}</div>
      <b-form-input
        id="hill-climbing-iterations"
        v-model="hillClimbingIterations"
        v-if="method == 'hill_climbing'"
        type="range"
        min="10"
        max="350"
      ></b-form-input>
      <div class="mt-2" v-if="method == 'genetic'">Population Size: {{ geneticPopulationSize }}</div>
      <b-form-input
        id="genetic_population_size"
        v-model="geneticPopulationSize"
        v-if="method == 'genetic'"
        type="range"
        min="100"
        max="1000"
      ></b-form-input>
      <div class="mt-2" v-if="method == 'genetic'">Survival Rate: {{ geneticSurvivalRate }}%</div>
      <b-form-input
        id="genetic_survival_rate"
        v-model="geneticSurvivalRate"
        v-if="method == 'genetic'"
        type="range"
        min="1"
        max="75"
      ></b-form-input>
      <div
        class="mt-2"
        v-if="method == 'genetic'"
      >Secondary Survival Rate: {{ geneticSecondarySurvivalRate }}%</div>
      <b-form-input
        id="genetic_secondary_survival_rate"
        v-model="geneticSecondarySurvivalRate"
        v-if="method == 'genetic'"
        type="range"
        min="1"
        max="20"
      ></b-form-input>
      <div class="mt-2" v-if="method == 'genetic'">Mutation Rate: {{ geneticMutationRate }}%</div>
      <b-form-input
        id="genetic_mutation_rate"
        v-model="geneticMutationRate"
        v-if="method == 'genetic'"
        type="range"
        min="1"
        max="50"
      ></b-form-input>
      <div class="mt-2" v-if="method == 'genetic'">Epochs: {{ geneticEpochs }}</div>
      <b-form-input
        id="genetic_epochs"
        v-model="geneticEpochs"
        v-if="method == 'genetic'"
        type="range"
        min="10"
        max="100"
      ></b-form-input>
    </b-form>
  </b-modal>
</template>

<script>
export default {
  data () {
    return {
      hillClimbingIterations: 100,
      geneticPopulationSize: 350,
      geneticSurvivalRate: 20,
      geneticSecondarySurvivalRate: 5,
      geneticMutationRate: 5,
      geneticEpochs: 25,
      method: 'hill_climbing',
      methods: [
        { value: 'hill_climbing', text: 'Hill Climbing' },
        { value: 'genetic', text: 'Genetic Algorithm' }
      ]
    }
  },
  computed: {},
  methods: {
    handleOk () {
      if (this.method === 'hill_climbing') {
        this.$store.dispatch('run_hill_climbing_algorithm', this.hillClimbingIterations)
      }
      if (this.method === 'genetic') {
        var dict = {
          populationSize: this.geneticPopulationSize,
          survivalRate: this.geneticSurvivalRate / 100,
          secondarySurvivalRate: this.geneticSecondarySurvivalRate / 100,
          mutationRate: this.geneticMutationRate / 100,
          epochs: this.geneticEpochs
        }
        this.$store.dispatch('run_genetic_algorithm', dict)
      }
    }
  }
}
</script>
