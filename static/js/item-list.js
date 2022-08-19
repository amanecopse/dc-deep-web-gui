function refreshList(containerId, url, data, createItemFunction, callback){
    $.ajax({
        type: "POST",
        url: url,
        data: data,
        success: function (res) {
            renderItemList(containerId, res.listData, createItemFunction);
            callback(res);
        }
    })
}

function renderItemList(containerId, listData, createItemFunction){//만든 jQ DOM을 컨테이너에 삽입
    const itemListObj = createItemList(containerId, listData, createItemFunction);
    $(`#${containerId}`).html(itemListObj)
}

function createItemList(containerId, listData, createItemFunction) {//리스트의 jQ DOM을 생성하고 리턴
    const itemListObj = $(`
        <ul id = "${containerId}-list" class="list-group" style="list-style:none;">
        </ul>
    `);
    const items = [];
    for (let i = 0; i < listData.length; i++) {
        items.push(createItemFunction(`${containerId}-item${i}`, listData[i]));
    }
    itemListObj.html(items);
    return itemListObj;
}

function createItem(itemId, contentObj) {
    const itemObj = $(`<li id="${itemId}"></li>`);
    itemObj.html(contentObj);
    return itemObj;
}

function createListGroupItem(itemId, contentObj) {
    const itemObj = $(`<li id="${itemId}" class="list-group-item"></li>`);
    itemObj.append(contentObj);
    return itemObj;
}

function createRackItem(itemId, content) {
    let rackContentObj = $(
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
                        <button class="btn btn-warning" id="${itemId}-rack-edit"><i class="fa-solid fa-pen-to-square"></i></button>
                        <button class="btn btn-danger"  id="${itemId}-rack-delete"><i class="fa-solid fa-trash-can"></i></button>
                    </form>
                    <div id="${itemId}-collapse" class="collapse">
                        <h6 class="card-subtitle mb-2 mt-2 text-muted">- ${content.rack.info}</h6>
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item" id="${itemId + '-pdu'}">
                                <h5>PDUs</h5>
                            </li>
                            <li class="list-group-item" id="${itemId + '-sensor'}">
                                <h5>Sensors</h5>
                            </li>
                            <li class="list-group-item" id="${itemId + '-server'}">
                                <h5>Servers</h5>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        `
    );

    const rackEditObj = rackContentObj.find(`#${itemId}-rack-edit`);
    const rackDeleteObj = rackContentObj.find(`#${itemId}-rack-delete`);

    // 리스트 구성 버튼들에 이벤트 할당
    rackEditObj.on('click', (e)=>{
        e.preventDefault();
        showModal(MODAL_FORM_NAME_RACK, MODAL_MODE_EDIT, content.rack);
    });

    rackDeleteObj.on('click', (e)=>{
        e.preventDefault();
        showModal(MODAL_FORM_NAME_RACK, MODAL_MODE_DELETE, content.rack);
    });

    rackContentObj.find(`#${itemId}-pdu`).append(createItemList(itemId + '-pdu', content.pdus, createPduItem));
    rackContentObj.find(`#${itemId}-sensor`).append(createItemList(itemId + '-sensor', content.sensors, createSensorItem));
    rackContentObj.find(`#${itemId}-server`).append(createItemList(itemId + '-server', content.servers, createServerItem));
    return createItem(itemId, rackContentObj);
}

function createPduItem(itemId, content) {
    let pduContentObj = $(`

        <button class="btn btn-outline-dark" type="button" data-bs-toggle="collapse" data-bs-target="#${itemId}-collapse">
            PDU number: ${content.pduNum}
        </button>
        <button class="btn btn-warning" id="${itemId}-pdu-edit"><i class="fa-solid fa-pen-to-square"></i></button>
        <button class="btn btn-danger"  id="${itemId}-pdu-delete"><i class="fa-solid fa-trash-can"></i></button>
        <div id="${itemId}-collapse" class="collapse">
            <hr>
            <h6 class="mb-2">PDU outputs: ${content.outputCount}</h6>
            <h6 class="mb-2 text-muted">- ${content.info}</h6>
        </div>
    `);

    const pduEditObj = pduContentObj.find(`#${itemId}-pdu-edit`);
    const pduDeleteObj = pduContentObj.find(`#${itemId}-pdu-delete`);

    debugger;
    // 편집, 삭제 버튼에 이벤트 할당
    pduEditObj.on('click', (e)=>{
        e.preventDefault();
        showModal(MODAL_FORM_NAME_PDU, MODAL_MODE_EDIT, content);
    });

    pduDeleteObj.on('click', (e)=>{
        e.preventDefault();
        showModal(MODAL_FORM_NAME_PDU, MODAL_MODE_DELETE, content);
    });

    return createListGroupItem(itemId, pduContentObj);
}

function createSensorItem(itemId, content) {
    let pduContentObj = $(`
        <button class="btn btn-outline-dark" type="button" data-bs-toggle="collapse" data-bs-target="#${itemId}-collapse">
            Sensor number: ${content.sensorNum}
        </button>
        <button class="btn btn-warning" id="${itemId}-sensor-edit"><i class="fa-solid fa-pen-to-square"></i></button>
        <button class="btn btn-danger"  id="${itemId}-sensor-delete"><i class="fa-solid fa-trash-can"></i></button>
        <div id="${itemId}-collapse" class="collapse">
            <hr>
            <h6 class="mb-2">Rack number: ${content.rack.rackNum}</h6>
            <h6 class="mb-2">PDU number: ${content.pdu.pduNum}, output: ${content.pduOutput}</h6>
            <h6 class="mb-2 text-muted">- ${content.info}</h6>
        </div>
    `)
    return createListGroupItem(itemId, pduContentObj);
}

function createServerItem(itemId, content) {
    let pduContentObj = $(`
        <button class="btn btn-outline-dark" type="button" data-bs-toggle="collapse" data-bs-target="#${itemId}-collapse">
            Server number: ${content.serverNum}
        </button>
        <button class="btn btn-warning" id="${itemId}-server-edit"><i class="fa-solid fa-pen-to-square"></i></button>
        <button class="btn btn-danger"  id="${itemId}-server-delete"><i class="fa-solid fa-trash-can"></i></button>
        <div id="${itemId}-collapse" class="collapse">
            <hr>
            <h6 class="mb-2">Rack number: ${content.rack.rackNum}</h6>
            <h6 class="mb-2">PDU1 number: ${content.pdu1.pduNum}, output: ${content.pdu1Output}</h6>
            <h6 class="mb-2">PDU2 number: ${content.pdu2.pduNum}, output: ${content.pdu2Output}</h6>
            <h6 class="mb-2 text-muted">- ${content.info}</h6>
        </div>
    `)
    return createListGroupItem(itemId, pduContentObj);
}
