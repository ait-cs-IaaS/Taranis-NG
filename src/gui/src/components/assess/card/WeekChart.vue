<template>
  <div>
    <LineChart
      :chart-options="chartOptions"
      :chart-data="chartData"
      :height="chartHeight"
    />
  </div>
</template>

<script>
import { Line as LineChart } from 'vue-chartjs/legacy'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  CategoryScale,
  PointElement,
  Filler
} from 'chart.js'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  CategoryScale,
  PointElement,
  Filler
)

export default {
  name: 'WeekChart',
  components: {
    LineChart
  },
  props: {
    story: {
      type: Object,
      required: true
    },
    threshold: {
      type: Number,
      required: false,
      default: 20
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
      fillColors: ['rgb(121, 11, 27)', 'rgb(127, 116, 234)'],
      news_items_per_day: [],
      accumulated_chartData: [],
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        elements: { point: { radius: 0 } },
        scales: {
          x: {
            grid: {
              display: false
            }
          },
          y: {
            ticks: {
              min: 0,
              stepSize: 10
            },
            grid: {
              display: false
            }
          }
        },
        plugins: {
          filler: {
            propagate: false
          },
          legend: {
            display: false
          }
        }
      }
    }
  },
  computed: {
    last_seven_days() {
      return Array.from(Array(this.timespan).keys(), (i) => {
        const date = new Date()
        date.setDate(date.getDate() - i)
        return date.toLocaleDateString(undefined, {
          day: '2-digit',
          month: '2-digit'
        })
      }).reverse()
    },
    chartData() {
      return {
        labels: this.last_seven_days,
        datasets: [
          {
            data: this.threshold_line,
            borderWidth: 2,
            borderDash: [2, 3],
            borderColor: 'rgba(172, 0, 75, 1.0)',
            fill: false
          },
          {
            data: this.accumulated_chartData,
            showLine: false,
            fill: {
              target: { value: 20 },
              above: 'rgba(172, 0, 75, 1.0)',
              below: 'rgba(172, 0, 75, 0)'
            }
          },
          {
            data: this.accumulated_chartData,
            showLine: false,
            backgroundColor: 'rgba(127, 116, 234, 1.0)',
            fill: true
          }
        ]
      }
    },
    threshold_line() {
      return Array(this.timespan).fill(this.threshold)
    }
  },
  methods: {
    getChartData() {
      let sum = 0
      const accumulated_list = this.news_items_per_day.map(
        // (elem) => (sum = (sum || 0) + elem)
        // ################################################################################################
        // TODO: REMOVE following part for production and replace with line above
        // ################################################################################################
        (elem) => {
          sum =
            (sum || 0) +
            elem + // sum the amount of items in story
            Math.floor(Math.random() * 17) -
            Math.floor(Math.random() * 9) // In case items are too old (i.e. older than a week)
          if (sum < 0) {
            sum *= -1
          }
          return sum
        }
        // ################################################################################################
      )
      this.accumulated_chartData = accumulated_list
    }
  },
  updated() {
    // console.log('card rendered!')
  },
  mounted() {
    const days = this.last_seven_days
    const items_per_day = this.story.news_items.reduce((acc, item) => {
      const day = new Date(item.news_item_data.published).toLocaleDateString(
        undefined,
        { day: '2-digit', month: '2-digit' }
      )
      if (day in acc) {
        acc[day] += 1
      } else {
        acc[day] = 1
      }
      return acc
    }, {})

    this.news_items_per_day = days.map((day) => {
      if (day in items_per_day) return items_per_day[day]
      return 0
    })

    this.getChartData()
  }
}
</script>
