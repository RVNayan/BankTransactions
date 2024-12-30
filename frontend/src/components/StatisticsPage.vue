<template>
  <div class="StatisticsPage">
    <h1>Statistics Page</h1>
    <p>Chart 1 (Bar Chart)</p>
    <div class="chart-container">
      <canvas id="expensesChart"></canvas>
    </div>
    
    <p>Chart 2 (Pie Chart)</p>
    <div class="chart-container">
      <canvas id="PieChart1"></canvas>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import axios from 'axios';
import Chart from 'chart.js/auto';

export default defineComponent({
  name: 'StatisticsPage',
  props: {
    statistics: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      barstats: null, // Data for the bar chart
      pieStats: null, // Data for the pie chart
    };
  },
  watch: {
    // Watch for changes in the statistics prop
    statistics(newStats) {
      if (newStats) {
        this.barstats = newStats.barStats;  // Update barStats
        this.pieStats = newStats.pieStats;  // Update pieStats
        this.createBarChart(this.barstats); // Re-create the bar chart
        this.createPieChart(this.pieStats); // Re-create the pie chart
      }
    },
  },
  methods: {
    createBarChart(statistics) {
      const labels = Object.keys(statistics).map(date => {
        const [day, month] = date.split(' ');
        const monthIndex = new Date(Date.parse(month + " 1, 2021")).getMonth(); // Convert month name to month index
        return new Date(2021, monthIndex, parseInt(day)); // Reconstruct the full date as a Date object
      });

      labels.sort((a, b) => a - b); // Sort by date

      const sortedLabels = labels.map(date => {
        const options = { day: '2-digit', month: 'short' };
        return date.toLocaleDateString('en-GB', options); // Format as 'DD MMM'
      });

      const data = sortedLabels.map(label => statistics[label]);

      if (this.barChart) {
        this.barChart.destroy();
      }

      const ctx = document.getElementById("expensesChart").getContext("2d");
      this.barChart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: sortedLabels,
          datasets: [
            {
              label: "Total Expenses",
              data,
              backgroundColor: "#42A5F5",
              borderColor: "#1E88E5",
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: "top",
              labels: {
                font: {
                  family: "Arial, sans-serif",
                  size: 14,
                  weight: "bold",
                },
              },
            },
            title: {
              display: true,
              text: "Day-Wise Expenses",
              font: {
                family: "Arial, sans-serif",
                size: 18,
                weight: "bold",
              },
              color: "#333",
            },
            tooltip: {
              callbacks: {
                label: function (context) {
                  const value = context.raw;
                  return `₹${value.toFixed(2)}`;
                },
              },
              backgroundColor: "rgba(66, 165, 245, 0.8)",
              titleFont: {
                family: "Arial, sans-serif",
                size: 14,
                weight: "bold",
              },
              bodyFont: {
                family: "Arial, sans-serif",
                size: 12,
              },
            },
          },
          scales: {
            x: {
              ticks: {
                font: {
                  family: "Arial, sans-serif",
                  size: 12,
                },
                color: "#333",
              },
            },
            y: {
              ticks: {
                callback: function (value) {
                  return `₹${value}`;
                },
                font: {
                  family: "Arial, sans-serif",
                  size: 12,
                },
                color: "#333",
              },
              title: {
                display: true,
                text: "Amount (₹)",
                font: {
                  family: "Arial, sans-serif",
                  size: 14,
                  weight: "bold",
                },
                color: "#333",
              },
            },
          },
        },
      });
    },
    createPieChart(statistics) {
      const labels = Object.keys(statistics);
      const data = labels.map(label => statistics[label]);

      if (this.pieChart) {
        this.pieChart.destroy();
      }

      const ctx = document.getElementById("PieChart1").getContext("2d");
      this.pieChart = new Chart(ctx, {
        type: "pie",
        data: {
          labels: labels,
          datasets: [{
            label: "Expense Distribution",
            data: data,
            backgroundColor: ["#42A5F5", "#FF7043", "#66BB6A", "#FFEB3B"],
            hoverOffset: 4,
          }],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: "top",
            },
            tooltip: {
              callbacks: {
                label: function (context) {
                  const value = context.raw;
                  return `₹${value.toFixed(2)}`;
                },
              },
            },
          },
        },
      });
    },
  },
  mounted() {
    // This will be triggered when statistics are passed as a prop
    if (this.statistics) {
      this.barstats = this.statistics.barStats;
      this.pieStats = this.statistics.pieStats;
      this.createBarChart(this.barstats);
      this.createPieChart(this.pieStats);
    }
  },
});
</script>

<style scoped>
.StatisticsPage {
  padding: 20px;
  text-align: center;
}

h1 {
  margin-bottom: 20px;
}

.chart-container {
  width: 80%;
  height: 300px;
  margin: 20px auto;
  border: 2px solid #1E88E5;
  border-radius: 10px;
  padding: 20px;
  background-color: #f9f9f9;
}
</style>
