window.addEventListener('DOMContentLoaded', () => {
    const lowres_upload = document.getElementById("lowres_upload");
    const lowres_name = document.getElementById("lowres_name");
  
    const ori_upload = document.getElementById("ori_upload");
    const ori_name = document.getElementById("ori_name");

    lowres_upload.onchange = function(){
      let reader = new FileReader();
      reader.readAsDataURL(lowres_upload.files[0]);
      console.log(lowres_upload.files[0]);
      lowres_name.textContent = lowres_upload.files[0].name;
    }

    ori_upload.onchange = function(){
      let reader = new FileReader();
      reader.readAsDataURL(ori_upload.files[0]);
      console.log(ori_upload.files[0]);
      ori_name.textContent = ori_upload.files[0].name;
    }
  });