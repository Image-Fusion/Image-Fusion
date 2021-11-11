function UploadSearchFunction(){
    var filter = document.getElementById('search').value.toUpperCase();
    var CardElement = document.getElementsByClassName('photo');
    var PhotoNameElement = document.getElementsByClassName('photoName');
    for(i = 0; i < CardElement.length; i++){
        var PhotoName = PhotoNameElement[i].innerText.toUpperCase();
        if(PhotoName.indexOf(filter)>-1){
            CardElement[i].style.display = "";
        }else{
            CardElement[i].style.display = "none";
        }
    }
}

function SelectAll(){
    var CheckBox = document.getElementsByName("image_checkbox");
    for(i = 0; i < CheckBox.length; i++){
        CheckBox[i].checked = true;
    }
}

function UnSelectAll(){
    var CheckBox = document.getElementsByName("image_checkbox");
    for(i = 0; i < CheckBox.length; i++){
        CheckBox[i].checked = false;
    }
}

function ImageSearchFunction(){
    var filter = document.getElementById('search').value.toUpperCase();
    var CardElement = document.getElementsByClassName('photo');
    var PhotoNameElement = document.getElementsByClassName('photoName');
    var CheckBox = document.getElementsByName("image_checkbox");
    var SelectSearched = document.getElementById('flexCheckChecked').checked;
    for(i = 0; i < CardElement.length; i++){
        var PhotoName = PhotoNameElement[i].innerText.toUpperCase();
        if(PhotoName.indexOf(filter)>-1){
            CardElement[i].style.display = "";
            if (SelectSearched&&filter!=""){
                CheckBox[i].checked = true;
            }
        }else{
            CardElement[i].style.display = "none";
        }
    }
}

function validateFileType(){
    var fileName = document.getElementById("fileName").value;
    var idxDot = fileName.lastIndexOf(".") + 1;
    var extFile = fileName.substr(idxDot, fileName.length).toLowerCase();
    if (extFile=="png"){
        //
    }else{
        fileName = "";
        alert("Only PNG files are allowed !");
    }   
}

var file = $("#fileName");
file.removeAttr('src');
var fileClone = file.clone();
fileClone.insertAfter(file);
file.remove();