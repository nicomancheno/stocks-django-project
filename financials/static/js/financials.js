function createTrendChart(id, data) {
    const ctx = document.getElementById(id).getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.values,
                borderColor: '#007bff',
                backgroundColor: 'rgba(0,123,255,0.2)',
                tension: 0.3,
                fill: false,
                pointRadius: 0,
                borderWidth: 2
            }]
        },
        options: {
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: { display: false },
                y: { display: false }
            },
            elements: {
                line: {
                    borderCapStyle: 'round'
                }
            }
        }
    });
}

// Data for each chart (example structure)
// You'll replace these with your real Django-generated data dynamically
const incomeData = {
    "total_revenue": {labels: ["2021", "2022", "2023"], values: [100, 120, 140]},
    "cost_of_revenue": {labels: ["2021", "2022", "2023"], values: [50, 60, 70]},
    // Add more fields...
};

const balanceData = {
    "total_assets": {labels: ["2021", "2022", "2023"], values: [500, 550, 580]},
    // Add more fields...
};

const cashflowData = {
    "free_cash_flow": {labels: ["2021", "2022", "2023"], values: [30, 35, 40]},
    // Add more fields...
};

// Render all income statement trends
for (const key in incomeData) {
    createTrendChart(`income-${key}`, incomeData[key]);
}

// Render all balance sheet trends
for (const key in balanceData) {
    createTrendChart(`balance-${key}`, balanceData[key]);
}

// Render all cashflow statement trends
for (const key in cashflowData) {
    createTrendChart(`cashflow-${key}`, cashflowData[key]);
}
