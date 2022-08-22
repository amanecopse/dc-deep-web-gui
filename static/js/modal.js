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

const MODAL_SHOW = "showModal";

function showModal(modalFormName, modalMode, modalData){
    let modalId;
    let modalObj;
    let formObj;

    if(modalMode === MODAL_MODE_DELETE){//삭제인 경우

        modalObj = $("#"+MODAL_ID_DELETE_FORM);
        formObj = modalObj.find("form");
        formObj.attr("data-submit-mode", modalMode);
        formObj.attr("data-form-name", modalFormName);

        if(modalFormName === MODAL_FORM_NAME_RACK){
            formObj.attr("data-rack-num", modalData.rackNum);
            modalObj.find(".modal-title").html(modalData.rackNum+"번 랙 삭제");
        }
        else if(modalFormName === MODAL_FORM_NAME_PDU){
            formObj.attr("data-rack-num", modalData.rackNum);
            formObj.attr("data-device-num", modalData.deviceNum);
            modalObj.find(".modal-title").html(modalData.deviceNum+"번 PDU 삭제");
        }
        else if(modalFormName === MODAL_FORM_NAME_SENSOR){
            formObj.attr("data-rack-num", modalData.rackNum);
            formObj.attr("data-device-num", modalData.deviceNum);
            modalObj.find(".modal-title").html(modalData.deviceNum+"번 센서 삭제");
        }
        else if(modalFormName === MODAL_FORM_NAME_SERVER){
            formObj.attr("data-rack-num", modalData.rackNum);
            formObj.attr("data-device-num", modalData.deviceNum);
            modalObj.find(".modal-title").html(modalData.deviceNum+"번 서버 삭제");
        }
        modalObj.modal('show');
    }
    else{//삭제가 아닌 나머지

        if(modalFormName === MODAL_FORM_NAME_RACK){
            modalId = MODAL_ID_RACK_FORM;
        }
        else if(modalFormName === MODAL_FORM_NAME_PDU){
            modalId = MODAL_ID_PDU_FORM;
        }
        else if(modalFormName === MODAL_FORM_NAME_SENSOR){
            modalId = MODAL_ID_SENSOR_FORM;
        }
        else if(modalFormName === MODAL_FORM_NAME_SERVER){
            modalId = MODAL_ID_SERVER_FORM;
        }
        modalObj = $("#"+modalId);
        formObj = modalObj.find("form");
        formObj.attr("data-submit-mode", modalMode);
        formObj.attr("data-form-name", modalFormName);

        $.ajax({
            type: "GET",
            url: URL_ENV_INDEX + `?mode=${modalMode}&formName=${modalFormName}`,
            data: modalData,
            success: function (res) {
                renderModalBody(modalId, createModalFormBody(res.form));
                if(modalMode === MODAL_MODE_ADD){
                    if(modalFormName === MODAL_FORM_NAME_RACK){
                        modalObj.find(".modal-title").html("새로운 랙 추가");
                        modalObj.modal('show');
                    }
                    else if(modalFormName === MODAL_FORM_NAME_PDU){
                        modalObj.find(".modal-title").html("새로운 PDU 추가");
                        modalObj.modal('show');
                    }
                    else if(modalFormName === MODAL_FORM_NAME_SENSOR){
                        modalObj.find(".modal-title").html("새로운 센서 추가");
                        modalObj.modal('show');
                    }
                    else if(modalFormName === MODAL_FORM_NAME_SERVER){
                        modalObj.find(".modal-title").html("새로운 서버 추가");
                        modalObj.modal('show');
                    }
                }
                else if(modalMode === MODAL_MODE_EDIT){
                    formObj.attr("data-rack-num", modalData.rackNum);
                    formObj.attr("data-device-num", modalData.deviceNum);
                    if(modalFormName === MODAL_FORM_NAME_RACK){
                        modalObj.find(".modal-title").html(modalData.rackNum+"번 랙 수정");
                        modalObj.modal('show');
                    }
                    else if(modalFormName === MODAL_FORM_NAME_PDU){
                        modalObj.find(".modal-title").html(modalData.deviceNum+"번 PDU 수정");
                        modalObj.modal('show');
                    }
                    else if(modalFormName === MODAL_FORM_NAME_SENSOR){
                        modalObj.find(".modal-title").html(modalData.deviceNum+"번 센서 수정");
                        modalObj.modal('show');
                    }
                    else if(modalFormName === MODAL_FORM_NAME_SERVER){
                        modalObj.find(".modal-title").html(modalData.deviceNum+"번 서버 수정");
                        modalObj.modal('show');
                    }
                }
            }
        })
    }
}

function renderModalBody(modalId, modalBodyObj){
    $('#'+modalId).find('div.modal-body').html(modalBodyObj);
}

function createModalFormBody(htmlText){
    const modalBodyObj = htmlText.replace(/<tr>/gi,"<div class='fieldWrapper mb-3'>")
                .replace(/<\/tr>/gi,"</div>")
                .replace(/<label/gi,"<label class='col-5 text-nowrap'")
                .replace(/<th>/gi,"")
                .replace(/<\/th>/gi,"")
                .replace(/<td>/gi,"")
                .replace(/<\/td>/gi,"");
    return modalBodyObj
}