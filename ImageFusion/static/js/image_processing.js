// $(document).on('click','#button_image_fusion', function() {
//     $('#loading_image_fusion').removeClass('visually-hidden');
//     $('#start_image_fusion').addClass('visually-hidden');
//     // $(this).attr('disabled', true);
// });

function countCheckbox(){
    var CheckBox = document.getElementsByName("image_checkbox");
    var count = 0;
    for(i = 0; i < CheckBox.length; i++){
        if(CheckBox[i].checked){
            count++;
        }
    }
    return count;
}

$(document).on('click', '#button_image_fusion_avg_min_max', function(){
    $('#form_image_fusion').attr('action', '/image_fusion/avg_min_max/');
    var count = countCheckbox();
    if(count == 2){
        $('#loading_image_fusion_avg_min_max').removeClass('visually-hidden');
        $('#start_image_fusion_avg_min_max').addClass('visually-hidden');
        $('#button_image_fusion_avg_min_max').attr('disabled', true);
        $('#form_image_fusion')[0].submit();
    }else{
        e.preventDefault();
        alert("Please select only Two Images to proceed.");
    }
});

$(document).on('click', '#button_image_fusion_wavelet', function(){
    $('#form_image_fusion').attr('action', '/image_fusion/wavelet/');
    var count = countCheckbox();
    if(count == 2){
        $('#loading_image_fusion_wavelet').removeClass('visually-hidden');
        $('#start_image_fusion_wavelet').addClass('visually-hidden');
        $('#button_image_fusion_wavelet').attr('disabled', true);
        $('#form_image_fusion')[0].submit();
    }else{
        e.preventDefault();
        alert("Please select only Two Images to proceed.");
    }
});

$(document).on('click', '#button_image_fusion_sift_matching', function(){
    $('#form_image_fusion').attr('action', '/image_fusion/sift_matching/');
    var count = countCheckbox();
    if(count == 2){
        $('#loading_image_fusion_sift_matching').removeClass('visually-hidden');
        $('#start_image_fusion_sift_matching').addClass('visually-hidden');
        $('#button_image_fusion_sift_matching').attr('disabled', true);
        $('#form_image_fusion')[0].submit();
    }else{
        e.preventDefault();
        alert("Please select only Two Images to proceed.");
    }
});

$(document).on('click', '#button_image_fusion_gcf', function(){
    $('#form_image_fusion').attr('action', '/image_fusion/gaussian_curvature_filter/');
    var count = countCheckbox();
    if(count == 2){
        $('#loading_image_fusion_gcf').removeClass('visually-hidden');
        $('#start_image_fusion_gcf').addClass('visually-hidden');
        $('#button_image_fusion_gcf').attr('disabled', true);
        $('#form_image_fusion')[0].submit();
    }else{
        e.preventDefault();
        alert("Please select only Two Images to proceed.");
    }
});