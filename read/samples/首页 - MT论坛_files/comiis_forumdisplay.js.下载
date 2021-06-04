function succeedhandle_forum_fav(a, b, c){
	if(b.indexOf("收藏成功") >= 0){
		b = '版块关注成功';
		$('.comiis_forum_fav').attr('href', 'home.php?mod=spacecp&ac=favorite&op=delete&type=forum&formhash='+formhash+'&favid=' + c['favid'] + '&handlekey=forum_fav').text('已关注').removeClass('bg_c f_f').addClass("bg_b f_d");
	}
	popup.open(b, 'alert');
}
function errorhandle_forum_fav(a, b){
	if(a.indexOf("重复收藏") >= 0){
		a = '版块已关注';
	}else if(a.indexOf("不存在") >= 0){
		a = '您还没有关注此版块';
	}
	popup.open(a, 'alert');
}
function succeedhandle_favorite_del(a, b, c){
	if(b.indexOf("成功") >= 0){
		b = '已取消关注此版块';
	}
	$('.comiis_forum_fav').attr('href', 'home.php?mod=spacecp&ac=favorite&type=forum&id=' + c['id'] + '&formhash='+formhash+'&handlekey=forum_fav').text('+ 关注').removeClass('bg_b f_d').addClass("bg_c f_f");
	popup.open(b, 'alert');
}
function errorhandle_favorite_del(a, b){
	if(a.indexOf("不存在") >= 0){
		a = '您还没有关注此版块';
	}
	popup.open(a, 'alert');
}
function upzhanlist(tid){
	$.ajax({
		type : 'GET',
		url : 'plugin.php?id=comiis_app&comiis=re_forum_list_zhan&tid='+tid,
		dataType : 'xml',
	}).success(function(s) {
		$('#comiis_wxlist_showbox_'+tid).html(s.lastChild.firstChild.nodeValue);
	});
}
var comiis_recommend_key = 0;
function comiis_recommend_addkey(){
	if($('.comiis_recommend_addkey').length > 0) {
		$('.comiis_recommend_addkey').off('click').on('click', function() {
		if(comiis_recommend_key == 0){
			comiis_recommend_key = 1;
			var comiis_zhankeys = $('.wxlist_bottom_box').length;
			var re_tids = $(this).attr('tid');
			var re_tid = $('.num-all_'+ re_tids);
			var comiis_retidbox = $(this);
			$.ajax({
				type : 'GET',
				url : $(this).attr('href') + '&inajax=1',
				dataType : 'xml',
			})
			.success(function(s) {
				var s = s.lastChild.firstChild.nodeValue;
				if(s.indexOf("您已评价过本主题") >= 0){
				$.ajax({
					type : 'GET',
					url : 'plugin.php?id=comiis_app&comiis=re_recommend&tid='+re_tids+'&inajax=1',
					dataType : 'xml',
				}).success(function(v) {
					if(comiis_zhankeys){
						upzhanlist(re_tids);
						$('#comiis_zhan_key'+ re_tids).text('赞');
					}else{
						var recommend_num = Number(re_tid.text());
						if(recommend_num > 1){
							re_tid.text((recommend_num - Number(allowrecommend)));
						}else{
							re_tid.text('');
						}
					}
					comiis_retidbox.removeClass('f_wb');
					$('#comiis_listzhan_' + re_tids + ' i').html('&#xe63b;');
					popup.open('已取消点赞', 'alert');					
				});
				}else if(s.indexOf("您不能评价自己的帖子") >= 0){
					popup.open('不能点赞自己的帖子', 'alert');
				}else if(s.indexOf("今日评价机会已用完") >= 0){
					popup.open('您今日的点赞机会已用完', 'alert');
				}else if(s.indexOf("'recommendv':'+" + allowrecommend + "'") >= 0){
					var b = [], r;
					r = s.match(/\'recommendc\':\'(.*?)\'/);
					if(r != null){
						b['recommendc'] = r[1];
					}else{
						b['recommendc'] = 0;
					}
					r = s.match(/\'daycount\':\'(.*?)\'/);
					if(r != null){
						b['daycount'] = r[1];
					}else{
						b['daycount'] = 0;
					}
					if(comiis_zhankeys){
						upzhanlist(re_tids);
						$('#comiis_zhan_key'+ re_tids).text('取消');
					}else{
						re_tid.text(Number(re_tid.text()) + Number(allowrecommend));
					}
					comiis_retidbox.addClass('f_wb');
					$('#comiis_listzhan_' + re_tids + ' i').html('&#xe654;');
					popup.open('点赞成功' + (b['daycount'] ? ', 您今天还能点赞 ' + (b['daycount'] - 1) + ' 次' : ''), 'alert');					
				}else if(s.indexOf("window.location.href = 'member.php?mod=logging&action=login&mobile=2'") >= 0){
					window.location.href = 'member.php?mod=logging&action=login&mobile=2';
				}else{
					popup.open('没有点赞权限或帖子不存在', 'alert');
				}
				setTimeout(function() {
					comiis_recommend_key = 0;
				}, 500);
			});
			}
			return false;
		});
	}
}