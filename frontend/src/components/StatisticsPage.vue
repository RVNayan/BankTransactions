<template>
  <div class="StatisticsPage">
    <h1>Statistics Page</h1>
    <p>Day-wise expenses visualized below:</p>
    
    <!-- Container for the chart -->
    <div class="chart-container">
      <canvas id="expensesChart"></canvas>
    </div>
    
    <!-- Placeholder for future charts/data plots -->
    <div class="future-charts">
      <p>Future charts and data plots will be added here.</p>
    </div>
  </div>
</template>

<script>
import { defineComponent } from "vue";
import Chart from "chart.js/auto";

export default defineComponent({
  name: "StatisticsPage",
  data() {
    return {
      statistics: null, // Raw statistics data
      chart: null, // Chart instance
    };
  },
  async created() {
    await this.fetchStatistics();
  },
  activated() {
    // Refetch statistics when navigating back to the page
    this.fetchStatistics();
  },
  methods: {
    async fetchStatistics() {
      try {
        const response = await fetch("http://localhost:8080/statistics", {
          method: "GET",
          credentials: "include", // Include cookies for session management if needed
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        this.statistics = data;
        this.createChart(data); // Create or update chart after fetching data
      } catch (error) {
        console.error("Failed to fetch statistics:", error);
      }
    },
    createChart(statistics) {
      const labels = Object.keys(statistics);
      const data = Object.values(statistics);

      // Destroy the existing chart instance if it exists
      if (this.chart) {
        this.chart.destroy();
      }

      // Create a new chart instance
      const ctx = document.getElementById("expensesChart").getContext("2d");
      this.chart = new Chart(ctx, {
        type: "bar",
        data: {
          labels,
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
                  family: "Arial, sans-serif", // Font family
                  size: 14, // Font size
                  weight: "bold", // Font weight
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
                  // Format the tooltip value as currency
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
                  // Format the y-axis values as currency
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
  width: 80%;  /* Set the width of the chart container */
  height: 300px;  /* Set the height of the chart */
  margin: 0 auto;
  border: 2px solid #1E88E5;  /* Border around the chart */
  border-radius: 10px;  /* Rounded corners for the box */
  padding: 20px;
  background-color: #f9f9f9;  /* Light background color */
}

.future-charts {
  margin-top: 30px;
  padding: 20px;
  border: 2px dashed #ccc;  /* Dashed border for the placeholder */
  border-radius: 10px;
  background-color: #f0f0f0;
  font-style: italic;
}
</style>
