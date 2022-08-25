const chartDict = {};

function refreshChart(url, fieldName, chartId, maxItemCount = 50, labels) {
    $.ajax({
        type: "GET",
        url: url,
        data: { "type": "chart render", "fieldName": fieldName },
        success: function (res) {
            renderChart(res.xVal, res.yVals, chartId, maxItemCount, labels);
            console.log('chart re-render');
        }
    });
}

function renderChart(xVal, yVals, chartId, maxItemCount = 50, labels){

    if(chartDict[chartId] !== undefined) chartDict[chartId].destroy();

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

    if(labels === undefined){
        labels = []
        for (let i in yVals) {
            let label = `output${i}`;
            labels.push(label);
        }
    }

    xVal = xVal.slice(Math.max(xVal.length - maxItemCount, 0))
    for (let i in yVals) {
        //x축 데이터 개수를 maxItemCount만큼 제한
        yVals[i] = yVals[i].slice(Math.max(yVals[i].length - maxItemCount, 0))

        datasets.push({
            label: labels[i], //그래프 제목
            fill: false, // line 형태일 때, 선 안쪽을 채우는지 안채우는지
            data: yVals[i],
            backgroundColor: [
                //색상
                colorset[i%9]
            ],
            borderColor: [
                //경계선 색상
                colorset[i%9]
            ],
            borderWidth: 1 //경계선 굵기
        });
    }

    var context = document
        .getElementById(chartId)
        .getContext('2d');
    chartDict[chartId] = new Chart(context, {
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