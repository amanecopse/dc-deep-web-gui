// const xVal = JSON.parse('{{xVal|safe}}');
//         const yVals = JSON.parse('{{yVals|safe}}');

let dataChart;

function refreshChart(url, fieldName, chartId) {
    $.ajax({
        type: "GET",
        url: url,
        data: { "type": "chart render", "fieldName": fieldName },
        success: function (res) {
            renderChart(res.xVal, res.yVals, 10, chartId);
            console.log('chart re-render');
        }
    });
}

function renderChart(xVal, yVals, maxXValCount, chartId){

    if(dataChart !== undefined) dataChart.destroy();

    const datasets = [];
    const colorset = [
        'rgba(0, 0, 0, 1)',
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)',
        'rgba(100, 120, 100, 1)',
        'rgba(200, 50, 64, 1)',
    ];

    xVal = xVal.slice(Math.max(xVal.length - maxXValCount, 0))
    for (let i in yVals) {
        yVals[i] = yVals[i].slice(Math.max(yVals[i].length - maxXValCount, 0))
        let label;
        if (Number(i) === 0)
            label = 'total';
        else
            label = `output${i}`;

        datasets.push({
            label: label, //그래프 제목
            fill: false, // line 형태일 때, 선 안쪽을 채우는지 안채우는지
            data: yVals[i],
            backgroundColor: [
                //색상
                colorset[i]
            ],
            borderColor: [
                //경계선 색상
                colorset[i]
            ],
            borderWidth: 1 //경계선 굵기
        });
    }

    var context = document
        .getElementById(chartId)
        .getContext('2d');
    dataChart = new Chart(context, {
        type: 'line', // 차트의 형태
        data: { // 차트에 들어갈 데이터
            labels: xVal.map((x) => `${x.hour}시${x.minute}분`),
            datasets: datasets
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}