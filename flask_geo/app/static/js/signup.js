(function(){

        var baseUrl = 'https://geomemoir.fun/api/'
        var url = window.location.toString().split('//')[1]
        var cur_lang = url.split('/')[1]
        var first_name = $('#first_name')
        var last_name = $('#last_name')
        var username = $('#username')
        var email = $('#email')
        var pwd = $('#pwd')
        var pwd_message = $('#pwd_message')
        var pwd_confirm = $('#pwd_confirm')
        var unameHelp = $('#unameHelp')
        var emailHelp = $('#emailHelp') 
        var pwdHelp = $('#pwdHelp')
        var uppercase = $('#capital')
        var lowercase = $('#lowercase')
        var number = $('#number')
        var pwd_length = $('#length')
        var show_pwd = $('#show_pwd')
        var hide_pwd = $('#hide_pwd')

        var token = ''

        geo_token = window.localStorage.getItem('geo_token')
        google_token = window.localStorage.getItem('google_token')
        if (geo_token){
                token = geo_token
                window.location.href = '/'+cur_lang+'/'
        }else if (google_token){
                token = google_token
                window.location.href = '/'+cur_lang+'/'
        }else{
                token = null
        }


        // username check
        username.keyup(function(){
                unameHelp.css('display', 'block')
        })
        username.keyup(function(){
                if (/^[a-zA-Z0-9]{6,}$/.test(username.val())){
                        unameHelp.removeClass('s_invalid');
                        unameHelp.addClass('s_valid');
                }else{
                        unameHelp.removeClass('s_valid');
                        unameHelp.addClass('s_invalid');
                }
        })


        // email check
        email.keyup(function() {
                emailHelp.css('display', 'block');
        })
        email.keyup(function(){
                if(/^[a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/.test(email.val())){
                        emailHelp.removeClass('s_invalid');
                        emailHelp.addClass('s_valid');
                }else{
                        emailHelp.removeClass('s_valid');
                        emailHelp.addClass('s_invalid');
                }
        })

        // pwd_message check
        pwd.keyup(function() {
                console.log('focus');
                pwd_message.css('display', 'block');
        }).blur(function(){
                console.log('focusout');
                pwd_message.css('display', 'none');
        })
        

        pwd.keyup(function(){

                var uppercase_reg = /[A-Z]/;
                if(uppercase_reg.test(pwd.val())){
                        uppercase.removeClass('invalid');
                        uppercase.addClass('valid');
                }else{
                        uppercase.removeClass('valid');
                        uppercase.addClass('invalid');
                }

                var lowercase_reg = /[a-z]/;
                if(lowercase_reg.test(pwd.val())){
                        lowercase.removeClass('invalid');
                        lowercase.addClass('valid');
                }else{
                        lowercase.removeClass('valid');
                        lowercase.addClass('invalid');
                }

                var number_reg = /[0-9]/;
                if(number_reg.test(pwd.val())){
                        number.removeClass('invalid');
                        number.addClass('valid');
                }else{
                        number.removeClass('valid');
                        number.addClass('invalid');
                }

                if(pwd.val().length >= 8){
                        pwd_length.removeClass('invalid');
                        pwd_length.addClass('valid');
                }else{
                        pwd_length.removeClass('valid');
                        pwd_length.addClass('invalid');
                }
        });

        // pwd_confirm check
        pwd_confirm.keyup(function(){
                pwdHelp.css('display', 'block');
        })

        pwd_confirm.keyup(function(){
                if (pwd_confirm.val() && pwd_confirm.val() == pwd.val()){
                        pwdHelp.removeClass('pwd_notmatch');
                        pwdHelp.addClass('pwd_match');
                }else{
                        pwdHelp.removeClass('pwd_match');
                        pwdHelp.addClass('pwd_notmatch');
                }
        })
        // when pwd changes 
        pwd.keyup(function(){
                if (pwd_confirm.val() && pwd_confirm.val() == pwd.val()){
                        pwdHelp.removeClass('pwd_notmatch');
                        pwdHelp.addClass('pwd_match');
                }else{
                        pwdHelp.removeClass('pwd_match');
                        pwdHelp.addClass('pwd_notmatch');
                }
        })

        // show and hide pwd
        hide_pwd.click(function(){
                hide_pwd.hide();
                show_pwd.show();
                pwd.attr('type', 'text');
                pwd_confirm.attr('type', 'text');
        })

        show_pwd.click(function(){
                show_pwd.hide();
                hide_pwd.show();
                pwd.attr('type', 'password');
                pwd_confirm.attr('type', 'password');
        })


        function usernameCheck(){
                return /^[a-zA-Z0-9]{6,}$/.test(username.val())
        }

        function emailCheck(){
                return /^[a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/.test(email.val())
        }

        function pwdCheck(){
                return (/[A-Z]/.test(pwd.val())&&/[a-z]/.test(pwd.val())&&/[0-9]/.test(pwd.val())&&pwd.val().length >= 8)
        }

        function pwdMatchCheck(){
                return pwd.val() == pwd_confirm.val()
        }

        $('#signup').click(function(){
                if (usernameCheck()&&emailCheck()&&pwdCheck()&&pwdMatchCheck()){                
                        $.ajax({
                                type: 'post',
                                url: baseUrl+ cur_lang +'/v1/users',
                                contentType: 'application/json',
                                dataType: 'json',
                                data: JSON.stringify({
                                        'first_name': first_name.val(),
                                        'last_name': last_name.val(),
                                        'username': username.val(),
                                        'email': email.val(),
                                        'password1': pwd.val(),
                                        'password2': pwd_confirm.val(),
                                }),
                                success: function(response){
                                        if (response.code == 200){
                                                window.localStorage.clear()
                                                window.localStorage.setItem('geo_token', response.token);
                                                window.localStorage.setItem('geo_username', response.username);
                                                window.location.href = '/'+cur_lang+'/';
                                        }else{
                                                alert (response.msg)
                                        }
                                },
                        })   
                }else{
                        message = signup_messages[0][cur_lang]
                        alert(message)
                }     
        })
       
        // sign in by google
        window.onload = function () {
                google.accounts.id.initialize({
			client_id: "831853056186-mp01j21dn4mcgaigju4co3f0lqio2o2d",
                callback: handleCredentialResponse,
                });
                google.accounts.id.renderButton(
                document.getElementById("googleDiv"),
                { theme: "standard", size: "large", shape: "pill"}
                );
                google.accounts.id.prompt(); // also display the One Tap dialog
        
        }


        function handleCredentialResponse(response) {
                window.google_token = response.credential 
                $.ajax({
                        type: 'post',
                        url: baseUrl+ cur_lang +"/v1/tokens/google_login",
                        contentType: 'application/json',
                        data: JSON.stringify({'google_token': response.credential}),
                        success: function(response){
                                if (response.code==200){
                                        window.localStorage.clear()
                                        window.localStorage.setItem('google_token', response.token);
                                        window.localStorage.setItem('geo_username', response.username);
                                        window.location.href = '/'+cur_lang+'/'
                                }else{
                                        alert(response.msg)
                                }
                        }
                })
        }

        const signup_messages = [
                {
                'en': 'Please confirm your information again before continuing.',
                'zh_Hant_TW': '請再次確認您的訊息是否完整無誤',
                'zh_Hans_CN': '请再次确认您的讯息是否完整无误'        
                },
        ]




})(jQuery);






