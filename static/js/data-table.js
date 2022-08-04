function refreshTable(rowLabel, colLabel, tableId) {
    $.ajax({
        type: "GET",
        url: "/",
        data: { "type": "table render"},
        success: function (tableData) {
            renderTable(tableData, rowLabel, colLabel, tableId);
            console.log('table re-render');
        }
    });
}

function renderTable(tableData, rowLabel, colLabel, tableId){
    let tHeader = '';
    let tRows = '';

    for (let i = 0; i < rowLabel.length; i++) {
        let tRow = `<th scope="row">${rowLabel[i]}</th>`;
        for (let j = 0; j < colLabel.length - 1; j++) {
            tRow += `<td>${tableData[i][j]}</td>`;
        }
        tRows += `
            <tr id="data-table-row-${i}">
                ${tRow}
            </tr>
        `
    }
    for (let i = 0; i < colLabel.length; i++) {
        tHeader += `
            <th scope="col">${colLabel[i]}</th>
        `
    }

    let tableContent = `
        <thead>
            <tr>
                ${tHeader}
            </tr>
        </thead>
        <tbody class="table-group-divider">
            ${tRows}
        </tbody>
    `
    $(`#${tableId}`).html(tableContent)
}