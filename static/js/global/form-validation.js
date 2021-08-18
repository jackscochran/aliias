var formValidator = (function(){

    function validateField(fieldJSON){
        if (validateType(getFieldValue(fieldJSON), fieldJSON.validationType)){
            hideError(fieldJSON);
            return true;
        }else{
            displayError(fieldJSON);
            return false;
        }
    }

    const validationTypes = {
        'email': /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/,
        'ticker': undefined
    }

    function validateType(value, type){
        return validationTypes[type].test(value);
    }

    function getFieldValue(fieldJSON){
        return $('[name=' + fieldJSON.inputElementName +']').val();
    }

    function displayError(fieldJSON){
        $('[name=' + fieldJSON.inputElementName +']').addClass('error-field')
        $('#' + fieldJSON.errorID).show()
    }

    function hideError(fieldJSON){
        $('[name=' + fieldJSON.inputElementName +']').removeClass('error-field')
        $('#' + fieldJSON.errorID).hide()
    }

    return {
        // public methods
        validateField,
        getFieldValue
    }
})()