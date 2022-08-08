function setSwitch(url, switchIndex, switchId, containerId) {
    
    let switchState;

    if($(`#${switchId}`).attr('checked') === 'checked') switchState = 0;
    else switchState = 1;

    $.ajax({
        type: "POST",
        url: url,
        data: { "type": "switch setting", "switchIndex":switchIndex,"switchState":switchState},
        success: function (checks) {
            renderSwitch(url, checks, containerId);
            console.log('switch re-render');
        }
    });
}

function renderSwitch(url, checks, containerId){
    let content = '';

    for (let i = 0; i < checks.length; i++) {
        let checked;
        if(checks[i] === Number(1))
            checked = 'checked'
        else
            checked = ''

        content += `
            <div class="col form-check form-switch">
                <input class="form-check-input" type="checkbox" role="switch"
                    id="o${i+1}-check" name="o${i+1}-check"
                    ${checked} onclick="setSwitch('${url}', ${i}, 'o${i+1}-check', 'output-form');">
                <label class="form-check-label"
                    for="o${i+1}-check">output${i+1}</label>
            </div>
        `
    }
    $(`#${containerId}`).html(content)
}