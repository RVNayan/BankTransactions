<template>
  <div class="StatisticsPage">
    <h1>Statistics Page</h1>
    <div class="charts">
      <div class="chart-container">
        <h3>Day-Wise Expenses (Bar Chart)</h3>
        <canvas id="expensesChart"></canvas>
      </div>
      <div class="chart-container">
        <h3>Expense Distribution (Pie Chart)</h3>
        <canvas id="PieChart1"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from "vue";
import Chart from "chart.js/auto";

export default defineComponent({
  name: "StatisticsPage",
  props: {
    statistics: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      barChart: null,
      pieChart: null,
    };
  },
  watch: {
    statistics(newStats) {
      if (newStats) {
        // Create or update Bar and Pie Charts with new statistics data
        this.createBarChart(newStats.barStats);
        this.createPieChart(newStats.pieStats);
      }
    },
  },
  methods: {
    createBarChart(statistics) {
      // Ensure statistics is a valid object and contains necessary data
      if (!statistics || Object.keys(statistics).length === 0) return;

      const parseDate = (label) => {
      const [day, month] = label.split(" ");
      const months = {
        Jan: 0, Feb: 1, Mar: 2, Apr: 3, May: 4, Jun: 5,
        Jul: 6, Aug: 7, Sep: 8, Oct: 9, Nov: 10, Dec: 11,
      };
      return new Date(0,months[month], parseInt(day));
    };

      const labels = Object.keys(statistics).sort((a, b) => {
      return parseDate(a) - parseDate(b);
    });
      const data = labels.map(label => statistics[label]);

      if (this.barChart) {
        this.barChart.destroy();
      }

      const ctx = document.getElementById("expensesChart").getContext("2d");
      this.barChart = new Chart(ctx, {
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
            legend: { position: "top" },
            title: { display: true, text: "Day-Wise Expenses" },
          },
        },
      });
    },
    createPieChart(statistics) {
  const filteredData = statistics.filter(item => parseFloat(item.sent) > 0);
  const labels = filteredData.map(item => item.updated_name);
  const data = filteredData.map(item => parseFloat(item.sent));
  const colors = filteredData.map(
    (_, index) => `hsl(${(index * 360) / filteredData.length}, 70%, 60%)`
  );

  if (this.pieChart) {
    this.pieChart.destroy();
  }

  const ctx = document.getElementById("PieChart1").getContext("2d");
  this.pieChart = new Chart(ctx, {
    type: "pie",
    data: {
      labels,
      datasets: [
        {
          label: "Expense Distribution",
          data,
          backgroundColor: colors,
          hoverOffset: 4,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "bottom", // Move the legend below the pie chart
          labels: {
            padding: 20, // Add padding between the chart and legend
            boxWidth: 20, // Set box size for the legend items
            font: {
              size: 14, // Adjust the font size for legend labels
            },
          },
        },
        tooltip: {
          callbacks: {
            label: function(tooltipItem) {
              return '₹' + tooltipItem.raw.toFixed(2); // Format tooltip values as currency
            },
          },
        },
      },
      layout: {
        padding: {
          top: 20, // Add space between the chart and the top container
          bottom: 40, // Add space between the chart and the bottom container
        },
      },
    },
  });
},
  },
  mounted() {
    if (this.statistics) {
      this.createBarChart(this.statistics.barStats);
      this.createPieChart(this.statistics.pieStats);
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

.charts {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
}

.chart-container {
  flex: 1 1 45%; /* Adjusts to 50% of the available space */
  max-width: 600px;
  min-width: 300px;
  padding: 20px;
  border: 2px solid #1E88E5;
  border-radius: 10px;
  background-color: #f9f9f9;
}

.chart-container h3 {
  margin-bottom: 10px;
  color: #1E88E5;
}
</style>
