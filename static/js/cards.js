function assetPickerOpen(parent_target_id){
  window.open("/asset/picker?parent_target_id=" + parent_target_id, "picker", "directories=0,titlebar=0,toolbar=0,location=0,status=0,menubar=0,scrollbars=no,width=800, height=400");
  return false;
}

function assetPickerChoose(parent_target_id, val){
//  el = window.opener.document.getElementById(parent_target_id);
//  el.value = val;
    var allElements = window.opener.document.getElementsByTagName("*");
    for(i = 0; i < allElements.length; i++){
        if (allElements[i].id == parent_target_id){
        	allElements[i].value = val;
        }
    }
  this.close();
}

function fieldToggle(el){
  id = el.prop("id");
  if (el.prop("checked")){
    $("#ul" + id).fadeIn();
    $("#img" + id).fadeIn();
  } else {
    $("#ul" + id).hide();
    $("#img" + id).hide();
    $("#ul" + id).find("input").val("");
  }
}

function mfToggle(el){
  id_this = el.prop("id");
  $.each($(".mf-group"), function(index, value){
    mf_id = $(value).prop("id");
    id = mf_id.substring(2);
    if (id != id_this){
      $(value).hide();
      $("#img" + id).hide();
    } else {
      $(value).show();
      $("#img" + id).show();
    }
  });
}

function postToggle(el){
  if (el.prop("checked")){
    $("#postTweetAction").fadeIn();
  } else {
    $("#postTweetAction").hide();
  }
}

function copyToClipboard(text) {
  window.prompt("Copy to clipboard: Ctrl+C, Enter", text);
}
