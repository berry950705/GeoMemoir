(function(){

        var imgUrl = 'https://geomemoir.fun/media/'
        var baseUrl = 'https://geomemoir.fun/api/';
        var url = window.location.toString().split('//')[1]
        var cur_lang = url.split('/')[1]

        var username = window.localStorage.getItem('geo_username')
        var geo_token = window.localStorage.getItem('geo_token')
        var google_token = window.localStorage.getItem('google_token')
        if (geo_token){
                var token = geo_token
        }else if (google_token){
                var token = google_token
        }
        
        var avatar_img = $('#avatar_img')
        var avatar = $('#avatar')
        var bg_img = $('#bg_img')
        var background = $('#background')
        var profile_name = $('#profile_name')
        var motto = $('#motto')
        var self_introduction = $('#self_introduction')


        $.ajax({
                type:'get',
                url:baseUrl+ cur_lang + '/v1/users/' + username,
                dataType:'json',
                beforeSend: function(request){
                        request.setRequestHeader('Authorization', token)
                },
                success: function(response){
                        if (response.code==200){
                                author = response.data['author']
                                profile_name.val(author['profile_name'])
                                motto.val(author['motto'])
                                self_introduction.text(author['self_intro'])
                                if (author['avatar']){
                                        avatar_img.attr('src', imgUrl+author['avatar'])
                                }
                                if (author['background_img']){
                                        bg_img.attr('src', imgUrl+author['background_img']) 
                                } 
                        }
                }   
        })

        $('#update_submit').click(function(){

                if (profile_name.val() && motto.val()&&self_introduction.val()){
                        formdata = new FormData();

                        if (avatar[0].files[0]){
                                formdata.append("avatar", avatar[0].files[0]);
                        }
                        if (background[0].files[0]){
                                formdata.append("background", background[0].files[0]);
                        }
                        formdata.append( 'profile_name', profile_name.val())
                        formdata.append('motto', motto.val())
                        formdata.append('self_intro', self_introduction.val())

                        $.ajax({
                                processData:false,
                                contentType:false,
                                type: 'post',
                                url: baseUrl+ cur_lang + '/v1/users/' + username+'/edit_profile' ,
                                data: formdata,
                                beforeSend: function(request){
                                        request.setRequestHeader("Authorization", token)
                                },
                                success:function(response){
                                        if (response.code==200){
                                                message = editProfile_messages[0][cur_lang]
                                                alert('Profile has been successfully updated.')
                                        }else{
                                                alert(response.msg)
                                        }
                                }       
                        })
                
                }else{
                        message = editProfile_messages[1][cur_lang]
                        alert('Please complete your profile before uploading.')
                }                                
        })
      

        const editProfile_messages = [
                {
                'en': 'Profile has been successfully updated.',
                'zh_Hant_TW': '您已成功更新簡介',
                'zh_Hans_CN': '您已成功更新简介' 
                },
                {
                'en': 'Please complete your profile before uploading.',
                'zh_Hant_TW': '請您完成簡介內容再行上傳',
                'zh_Hans_CN': '请您完成简介内容再行上传'        
                },
        ]

})(jQuery);
