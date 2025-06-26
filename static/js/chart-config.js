
const ctx = document.getElementById('resumeChart').getContext('2d');
const resumeChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Approved', 'Pending', 'Rejected'],
    datasets: [{
      label: 'Resumes',
      data: [0, 0, 0], // Replace with actual data in your template or inject via JS
      backgroundColor: ['#34d399', '#fbbf24', '#f87171'],
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { display: false },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1
        }
      }
    }
  }
});
