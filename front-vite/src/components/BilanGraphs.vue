<template>
  <vue-highcharts
    :options="config"
    ref="currentGraphs"
  />
</template>

<script lang="ts">
import {Chart} from 'highcharts-vue'
import { getGraphStats } from '@/utils/appli_api'

export default {
  components: {
    VueHighcharts: Chart
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
      const { chart } = this.$refs.currentGraphs as any;
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
            const { currentGraphs } = this.$refs as any;
            this.cleanGraph();
            currentGraphs.delegateMethod('showLoading', 'Loading...');
            setTimeout(() => {
              data.forEach((serie: any) => {
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
