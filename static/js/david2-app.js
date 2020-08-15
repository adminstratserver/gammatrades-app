var id1 = document.getElementById('eproof_document_id');
var id2 = document.getElementById('eproof_title');

id1.addEventListener('change', doThing1);
//id2.addEventListener('change', doThing2);

function doThing1(){
   //alert('Horray! Someone wrote "' + this.value + '"!');
   console.log('this=',this.value);
   var title1 = this.value;
   var len1 = title1.lastIndexOf("\\")+1;
   var len2 = title1.indexOf(".");
   var new_title = title1.slice(len1, len2);
   console.log('new_title=',new_title);
   id2.value = new_title;
}
/*
function doThing2(){
   console.log('id2=', id2);
   console.log('id2.value=', id2.value);
} */
