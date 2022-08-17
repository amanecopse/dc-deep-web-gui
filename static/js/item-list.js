function refreshList(containerId, url, data, createItemFunction, callback){
    $.ajax({
        type: "POST",
        url: url,
        data: data,
        success: function (res) {
            renderItemList(containerId, res.listData, createItemFunction);
            callback();
        }
    })
}

function createItemList(containerId, listData, createItemFunction){//리스트의 html을 생성하고 리턴
    /*
        containerId: 리스트의 부모가 될 컨테이너의 id. 이걸 기반으로 리스트의 id 결정.
        itemData: 리스트의 데이터.
        createItemFunction: 각각의 아이템 html 내용을 구성하는 함수.
    */
   
    let items = ''
    for(let i=0;i<listData.length;i++){
        items += createItemFunction(`${containerId}-item${i}`, listData[i])
    }
    const listHtml = `
        <ul id = "${containerId}-list" class="list-group" style="list-style:none;">
            ${items}
        </ul>
    `
    return listHtml;
}

function renderItemList(containerId, listData, createItemFunction){//만든 html을 컨테이너에 렌더링함
    const listHtml = createItemList(containerId, listData, createItemFunction);
    $(`#${containerId}`).html(listHtml)
}

function createItem(itemId, content){
    return `<li id="${itemId}">${content}`
}

function createListGroupItem(itemId, content){
    return `<li id="${itemId}" class="list-group-item">${content}`
}

function createRackItem(itemId, content){
    let rackContent =
    `
        <div class="card mt-3">
            <div class="card-body">
                <form
                    id="${itemId}-form"
                    data-rack-num="${content.rack.rackNum}" data-info="${content.rack.info}"
                >
                    <button class="btn btn-outline-dark" type="button" data-bs-toggle="collapse" data-bs-target="#${itemId}-collapse">
                    Rack number: ${content.rack.rackNum}
                    </button>
                    <input class="btn btn-warning" type="submit" name="edit" value="Edit"</input>
                    <input class="btn btn-danger" type="submit"  name="delete" value="Delete"></input>
                </form>
                <div id="${itemId}-collapse" class="collapse">
                    <h6 class="card-subtitle mb-2 mt-2 text-muted">- ${content.rack.info}</h6>
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item">
                            <h5>PDUs
                                <button
                                    id="${itemId}-add-pdu"
                                    class="btn btn-primary ms-1" type="button"
                                >
                                    Add
                                </button>
                            </h5>
                            ${createItemList(itemId+"-pdu", content.pdus, createPduItem)}
                        </li>
                        <li class="list-group-item">
                            <h5>Sensors
                                <button
                                    id="${itemId}-add-sensor"
                                    class="btn btn-primary ms-1" type="button"
                                >
                                    Add
                                </button>
                            </h5>
                            ${createItemList(itemId+"-sensor", content.sensors, createSensorItem)}
                        </li>
                        <li class="list-group-item">
                            <h5>Servers
                                <button
                                    id="${itemId}-add-server"
                                    class="btn btn-primary ms-1" type="button"
                                >
                                    Add
                                </button>
                            </h5>
                            ${createItemList(itemId+"-server", content.servers, createServerItem)}
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    `;
    return createItem(itemId, rackContent);
}

function createPduItem(itemId, content){
    let pduContent =
    `
        <button class="btn btn-outline-dark" type="button" data-bs-toggle="collapse" data-bs-target="#${itemId}-collapse">
            PDU number: ${content.pduNum}
        </button>
        <button class="btn btn-warning" type="button">
            Edit
        </button>
        <button class="btn btn-danger" type="button">
            Delete
        </button>
        <div id="${itemId}-collapse" class="collapse">
            <hr>
            <h6 class="mb-2">PDU outputs: ${content.outputCount}</h6>
            <h6 class="mb-2 text-muted">- ${content.info}</h6>
        </div>
    `;
    return createListGroupItem(itemId, pduContent);
}

function createSensorItem(itemId, content){
    let pduContent =
    `
        <button class="btn btn-outline-dark" type="button" data-bs-toggle="collapse" data-bs-target="#${itemId}-collapse">
            Sensor number: ${content.sensorNum}
        </button>
        <button class="btn btn-warning" type="button">
            Edit
        </button>
        <button class="btn btn-danger" type="button">
            Delete
        </button>
        <div id="${itemId}-collapse" class="collapse">
            <hr>
            <h6 class="mb-2">Rack number: ${content.rack.rackNum}</h6>
            <h6 class="mb-2">PDU number: ${content.pdu.pduNum}, output: ${content.pduOutput}</h6>
            <h6 class="mb-2 text-muted">- ${content.info}</h6>
        </div>
    `;
    return createListGroupItem(itemId, pduContent);
}

function createServerItem(itemId, content){
    let pduContent =
    `
        <button class="btn btn-outline-dark" type="button" data-bs-toggle="collapse" data-bs-target="#${itemId}-collapse">
            Server number: ${content.serverNum}
        </button>
        <button class="btn btn-warning" type="button">
            Edit
        </button>
        <button class="btn btn-danger" type="button">
            Delete
        </button>
        <div id="${itemId}-collapse" class="collapse">
            <hr>
            <h6 class="mb-2">Rack number: ${content.rack.rackNum}</h6>
            <h6 class="mb-2">PDU1 number: ${content.pdu1.pduNum}, output: ${content.pdu1Output}</h6>
            <h6 class="mb-2">PDU2 number: ${content.pdu2.pduNum}, output: ${content.pdu2Output}</h6>
            <h6 class="mb-2 text-muted">- ${content.info}</h6>
        </div>
    `;
    return createListGroupItem(itemId, pduContent);
}