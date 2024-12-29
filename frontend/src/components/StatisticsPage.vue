<template>
  <div class="StatisticsPage">
    <h1>Statistics Page</h1>
    <p>Day-wise expenses visualized below:</p>
    
    <div class="chart-container">
      <canvas id="expensesChart"></canvas>
    </div>
  </div>
</template>

<script>
import { defineComponent, watch } from 'vue';
import Chart from 'chart.js/auto';

export default defineComponent({
  name: 'StatisticsPage',
  props: {
    statistics: {
      type: Object,
      required: true,
    },
  },
  watch: {
    // Watch for changes in the statistics prop
    statistics(newStats) {
      if (newStats) {
        this.createChart(newStats);
      }
    }
  },
  methods: {
    createChart(statistics) {
      // Convert the date strings to Date objects for sorting
      const labels = Object.keys(statistics).map(date => {
        const [day, month] = date.split(' ');
        const monthIndex = new Date(Date.parse(month +" 1, 2021")).getMonth(); // Convert month name to month index
        return new Date(2021, monthIndex, parseInt(day)); // Reconstruct the full date as a Date object
      });

      // Sort the labels array
      labels.sort((a, b) => a - b); // Sort by date

      // Convert the sorted labels back to the format 'DD MMM'
      const sortedLabels = labels.map(date => {
        const options = { day: '2-digit', month: 'short' };
        return date.toLocaleDateString('en-GB', options); // Format as 'DD MMM'
      });

      const data = sortedLabels.map(label => statistics[label]);

      // Destroy the existing chart instance if it exists
      if (this.chart) {
        this.chart.destroy();
      }

      // Create a new chart instance
      const ctx = document.getElementById("expensesChart").getContext("2d");
      this.chart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: sortedLabels, // Use sorted and formatted date labels
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
    }
  },
});
</script>

<style scoped>
/* Styling for the statistics page */
.StatisticsPage {
  padding: 20px;
  text-align: center;
}

h1 {
  margin-bottom: 20px;
}

.chart-container {
  width: 80%;  /* Set the width of the chart container */
  height: 300px;  /* Set the height of the chart */
  margin: 0 auto;
  border: 2px solid #1E88E5;  /* Border around the chart */
  border-radius: 10px;  /* Rounded corners for the box */
  padding: 20px;
  background-color: #f9f9f9;  /* Light background color */
}
</style>
