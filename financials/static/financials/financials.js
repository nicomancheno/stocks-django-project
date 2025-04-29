document.addEventListener('DOMContentLoaded', function () {
    const incomeReports = JSON.parse(document.getElementById('incomeReportsData').textContent);
    const cashflowReports = JSON.parse(document.getElementById('cashflowReportsData').textContent);

    const extractData = (reports, field) => reports.map(r => r[field]).reverse();
    const extractLabels = reports => reports.map(r => r.fiscal_date_ending).reverse();

    const calculateGrowth = (latest, earliest) => {
        if (earliest && earliest !== 0) {
            const growth = ((latest - earliest) / Math.abs(earliest)) * 100;
            return growth.toFixed(1);
        }
        return null;
    };

    const createChartWithGrowth = (ctxId, label, data, borderColor, growthContainerId) => {
        const ctx = document.getElementById(ctxId).getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: extractLabels(incomeReports).map(date => new Date(date).getFullYear()),
                datasets: [{
                    label: label,
                    data: data,
                    borderColor: borderColor,
                    fill: false,
                    tension: 0.3,
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false, position: 'top' },
                    title: {
                        display: true,
                        text: label,
                        font: {
                            size: 18,
                            weight: 'bold'
                        }
                    }
                },
                scales: { y: { beginAtZero: false } }
            }
        });

        // Add growth below chart
        const growth = calculateGrowth(data.at(-1), data[0]);
        const growthContainer = document.createElement('div');
        growthContainer.classList.add('growth-text');

        if (growth !== null) {
            const isSharesChart = ctxId.toLowerCase().includes('shares'); // adjust if needed
            const isPositive = parseFloat(growth) >= 0;
            const color = isSharesChart
                ? (isPositive ? 'red' : 'green')  // for shares, increase = red
                : (isPositive ? 'green' : 'red'); // for other charts, increase = green

            growthContainer.innerHTML = `Growth over 4 years: <strong style="color:${color}">${growth}%</strong>`;
        } else {
            growthContainer.textContent = 'Growth data not available';
        }

        document.getElementById(ctxId).parentElement.appendChild(growthContainer);
    };

    createChartWithGrowth('totalRevenueChart', 'Total Revenue', extractData(incomeReports, 'total_revenue'), 'blue');
    createChartWithGrowth('netIncomeChart', 'Net Income', extractData(incomeReports, 'net_income'), 'green');
    createChartWithGrowth('freeCashFlowChart', 'Free Cash Flow', extractData(cashflowReports, 'free_cash_flow'), 'purple');
    createChartWithGrowth('basicSharesChart', 'Basic Average Shares', extractData(incomeReports, 'basic_average_shares'), 'orange');
});
