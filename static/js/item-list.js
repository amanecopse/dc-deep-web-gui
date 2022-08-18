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
                        <input class="btn btn-warning" type="submit" name="edit" value="Edit"</input>
                        <input class="btn btn-danger" type="submit"  name="delete" value="Delete"></input>
                    </form>
                    <div id="${itemId}-collapse" class="collapse">
                        <h6 class="card-subtitle mb-2 mt-2 text-muted">- ${content.rack.info}</h6>
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item" id="${itemId + '-pdu'}">
                                <h5>PDUs
                                    <button
                                        id="${itemId}-add-pdu"
                                        class="btn btn-primary ms-1" type="button"
                                    >
                                        Add
                                    </button>
                                </h5>
                            </li>
                            <li class="list-group-item" id="${itemId + '-sensor'}">
                                <h5>Sensors
                                    <button
                                        id="${itemId}-add-sensor"
                                        class="btn btn-primary ms-1" type="button"
                                    >
                                        Add
                                    </button>
                                </h5>
                            </li>
                            <li class="list-group-item" id="${itemId + '-server'}">
                                <h5>Servers
                                    <button
                                        id="${itemId}-add-server"
                                        class="btn btn-primary ms-1" type="button"
                                    >
                                        Add
                                    </button>
                                </h5>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        `
    );

    const rackFormObj = rackContentObj.find(`#${itemId}-form`);
    const rackAddPdu = rackContentObj.find(`#${itemId}-add-pdu`);
    const rackAddSensor = rackContentObj.find(`#${itemId}-add-sensor`);
    const rackAddServer = rackContentObj.find(`#${itemId}-add-server`);

    rackFormObj.children('input[name = "edit"]').on('click', (e)=>{
        e.preventDefault();
        console.log("edit rack:", e.target.form.dataset.rackNum, e.target.form.dataset.info);
        showModal(MODAL_FORM_NAME_RACK, MODAL_MODE_EDIT, e.target.form.dataset);
    })

    rackFormObj.children('input[name = "delete"]').on('click', (e)=>{
        e.preventDefault();
        console.log("delete rack:");
        showModal(MODAL_FORM_NAME_RACK, MODAL_MODE_DELETE, e.target.form.dataset);
    })

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
        `);
    return createListGroupItem(itemId, pduContentObj);
}

function createSensorItem(itemId, content) {
    let pduContentObj = $(`
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
    `)
    return createListGroupItem(itemId, pduContentObj);
}

function createServerItem(itemId, content) {
    let pduContentObj = $(`
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
    `)
    return createListGroupItem(itemId, pduContentObj);
}


//modal functions
const MODAL_FORM_NAME_RACK = "RackForm";
const MODAL_FORM_NAME_PDU = "PduForm";
const MODAL_FORM_NAME_SENSOR = "SensorForm";
const MODAL_FORM_NAME_SERVER = "ServerForm";

const MODAL_ID_RACK_FORM = "rackFormModal";
const MODAL_ID_PDU_FORM = "pduFormModal";
const MODAL_ID_SENSOR_FORM = "sensorFormModal";
const MODAL_ID_SERVER_FORM = "serverFormModal";
const MODAL_ID_DELETE_FORM = "deleteFormModal";

const MODAL_MODE_ADD = "formSubmitAdd";
const MODAL_MODE_EDIT = "formSubmitEdit";
const MODAL_MODE_DELETE = "formSubmitDelete";
function showModal(modalFormName, modalMode, modalData){
    let modalObj;
    if(modalFormName === MODAL_FORM_NAME_RACK){
        if(modalMode === MODAL_MODE_ADD){
            modalObj = $("#"+MODAL_ID_RACK_FORM);
            modalObj.find(".modal-title").html("새로운 랙 추가");
            modalObj.find("input[name='rackNum']").val("");
            modalObj.find("input[name='info']").val("");
            const formObj = modalObj.find("form");
            formObj.attr("data-submit-mode", MODAL_MODE_ADD);
            formObj.attr("data-form-name", MODAL_FORM_NAME_RACK);
        }
        else if(modalMode === MODAL_MODE_EDIT){
            modalObj = $("#"+MODAL_ID_RACK_FORM);
            modalObj.find(".modal-title").html(modalData.rackNum+"번 랙 수정");
            modalObj.find("input[name='rackNum']").val(modalData.rackNum);
            modalObj.find("input[name='info']").val(modalData.info);
            const formObj = modalObj.find("form");
            formObj.attr("data-submit-mode", MODAL_MODE_EDIT);
            formObj.attr("data-form-name", MODAL_FORM_NAME_RACK);
        }
        else if(modalMode === MODAL_MODE_DELETE){
            modalObj = $("#"+MODAL_ID_DELETE_FORM);
            modalObj.find(".modal-title").html(modalData.rackNum+"번 랙 삭제");
            const formObj = modalObj.find("form");
            formObj.attr("data-submit-mode", MODAL_MODE_DELETE);
            formObj.attr("data-form-name", MODAL_FORM_NAME_RACK);
            formObj.attr("data-rack-num", modalData.rackNum);
            
        }
    }
    modalObj.modal('show');
}