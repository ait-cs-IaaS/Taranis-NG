<template>
  <Bar
    :chart-options="chartOptions"
    :chart-data="chart_data"
    :height="chartHeight"
  />
</template>

<script>
import { Bar } from 'vue-chartjs/legacy'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  Filler,
  LineElement,
  BarElement,
  LinearScale,
  CategoryScale,
  PointElement,
  LineController
} from 'chart.js'
import { mapGetters } from 'vuex'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  Filler,
  LineElement,
  BarElement,
  LinearScale,
  CategoryScale,
  PointElement,
  LineController
)

export default {
  name: 'WeekChart',
  components: {
    Bar
  },
  props: {
    story: {
      type: Object,
      required: false,
      default: () => {}
    },
    timespan: {
      type: Number,
      required: false,
      default: 7
    },
    chartHeight: {
      type: Number,
      required: false,
      default: 150
    }
  },
  data: function () {
    return {
      chartOptions: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
          y1: {
            position: 'left',
            beginAtZero: true
          },
          y2: {
            position: 'right',
            beginAtZero: true,
            max: parseInt(this.getY2max()),
            grid: {
              // display gridlines only for y1
              drawOnChartArea: false
            }
          }
        },
        plugins: {
          filler: {
            propagate: false
          },
          legend: {
            display: false
          },
          tooltip: {
            mode: 'index',
            intersect: false
          }
        }
      }
    }
  },
  watch: {
    getY2MaxFromStore: {
      handler(newValue) {
        this.chartOptions.scales.y2.max = parseInt(newValue)
      },
      immediate: true
    }
  },
  computed: {
    getY2MaxFromStore() {
      return this.getY2max()
    },
    last_n_days() {
      return Array.from(Array(this.timespan).keys(), (i) => {
        const date = new Date()
        date.setDate(date.getDate() - i)
        return date.toLocaleDateString(undefined, {
          day: '2-digit',
          month: '2-digit'
        })
      }).reverse()
    },
    story_items() {
      return this.story.news_items.reduce((acc, item) => {
        const day = new Date(item.news_item_data.published).toLocaleDateString(
          undefined,
          { day: '2-digit', month: '2-digit' }
        )
        acc[day] = (acc[day] || 0) + 1
        return acc
      }, {})
    },
    news_items_per_day() {
      let items_per_day = {}
      items_per_day = this.story_items

      const days = this.last_n_days

      return days.map((day) => {
        if (day in items_per_day) {
          return items_per_day[day]
        } else {
          return 0
        }
      })
    },
    chart_colors() {
      return this.news_items_per_day.map((item) => {
        if (item >= this.getThreshold()) {
          return 'rgba(255, 0, 0, 1.0)'
        } else {
          return 'rgba(127, 116, 234, 1.0)'
        }
      })
    },
    chart_data() {
      return {
        labels: this.last_n_days,
        datasets: [
          {
            label: 'items/day',
            data: this.news_items_per_day,
            backgroundColor: this.chart_colors,
            type: 'bar',
            yAxisID: 'y1',
            order: 2
          },
          {
            label: 'items/day',
            type: 'line',
            data: this.news_items_per_day,
            borderColor: '#000',
            backgroundColor: '#000',
            yAxisID: 'y2',
            order: 1
          }
        ]
      }
    }
  },
  methods: {
    ...mapGetters('filter', ['getThreshold', 'getY2max'])
  },
  updated() {
    //console.log('card rendered!')
  },
  mounted() {
    if (!this.story) {
      console.error('No data provided to WeekChart')
    }
  }
}
</script>
