var hide = {
    loginbutton: function(){
      $('.signInButton').hide();
      $('#user_info').show();
      $('#logout_button1').show();
    },
    userinfo: function(){
      $('#user_info').hide();
      $('.signInButton').show();
      $('#logout_button1').hide();
    }
}

if((logged == 'null')||(logged=='')){
  hide.userinfo();
}
else{
  hide.loginbutton();
}

// if ( $('.error').length > 0 ) {
//   var error=document.getElementsByClassName('error').innerHTML;
//   document.location.href = "/";
//
// }
