<template>
  <div>
    <vue-highcharts :options="config" ref="currentGraphs"></vue-highcharts>
  </div>
</template>

<script>
import VueHighcharts from 'vue2-highcharts'
import { getGraphStats } from '@/services/appli_api.js'

export default {
  components: {
    VueHighcharts
  },
  data() {
    return {

    }
  },
  props: ['config', 'filters'],
  watch: {
    filters: {
      handler(newvalue, oldvalue) {
        if (
          Object.entries(newvalue).sort().toString() !== Object.entries(oldvalue).sort().toString()
        ) {
          console.log('Change', newvalue)
          this.getSeriesData();
        }
      },
      deep: true
    }
  },
  methods: {
    cleanGraph() {
      // Clear graph before update series
      const { chart } = this.$refs.currentGraphs;
      while (chart.series.length > 0) {
        chart.series[0].remove(true)
      }
      chart.redraw()
    },
    getSeriesData() {
      // Get data if api_url is set
      if ('api_url' in this.config) {
        getGraphStats(this.config.api_url, this.filters).then(
          (data) => {
            const { currentGraphs } = this.$refs;
            this.cleanGraph();
            this.loading = false;
            currentGraphs.delegateMethod('showLoading', 'Loading...');
            setTimeout(() => {
              data.forEach((serie) => {
                currentGraphs.addSeries(serie);
              });
              currentGraphs.hideLoading();
            }, 100)
          },
          (error) => {
            console.error('There was an error!', error);
          }
        )
      }
    }
  },
  mounted() {
    this.getSeriesData()
  }
}
</script>

<style>
</style>
