$(document).ready(function(){

  $("#file").change(function(){
    var fd = new FormData(this.form);
    var files = $('#file')[0].files;

    // Check file selected or not
    if(files.length > 0 ){
        fd.append('file',files[0]);
        $.ajaxSetup({
          headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
          }
        });
        $.ajax({
          url: 'http://loc.relation.com/upload-file',
          type: 'POST',
          data: fd,
          dataType: 'json',
          cache: false,
          contentType: false,
          processData: false,
          success: function(response){
              if(response != 0){
                console.log("successed");
              }else{
                console.log("failed");
              }
          },
          error: function(error) {
            console.log('error');
          }
        });
    }else{
      alert("Please select a file.");
    }
  });
});