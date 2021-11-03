// $(document).on('click','#button_image_fusion', function() {
//     $('#loading_image_fusion').removeClass('visually-hidden');
//     $('#start_image_fusion').addClass('visually-hidden');
//     // $(this).attr('disabled', true);
// });

$(document).on('submit','#form_image_fusion', function(e) {
    var CheckBox = document.getElementsByName("image_checkbox");
    var count = 0;
    for(i = 0; i < CheckBox.length; i++){
        if(CheckBox[i].checked){
            count++;
        }
    }
    if(count == 2){
        $('#loading_image_fusion').removeClass('visually-hidden');
        $('#start_image_fusion').addClass('visually-hidden');
        $('#button_image_fusion').attr('disabled', true);
    }else{
        e.preventDefault();
        alert("Please select only Two Images to proceed.");
    }
});

