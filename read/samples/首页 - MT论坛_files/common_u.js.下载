var platform = navigator.platform;
var ua = navigator.userAgent;
var ios = /iPhone|iPad|iPod/.test(platform) && ua.indexOf( "AppleWebKit" ) > -1;
var andriod = ua.indexOf( "Android" ) > -1;
var comiis_scrollTop = 0;
var Comiis_Touch_on = 1;
var Comiis_Touch_openleftnav = 0;
var Comiis_Touch_endtime = 0;
var comiis_load_yes_on = 0;
var Comiis_MENU_on = 0;
var Comiis_MENUS_on = 0;
var Comiis_MENU_Data = new Object;
var comiis_group = 0;
/* 腾讯电脑管家 数据 */
var score_config = {
	1: ['安全性未知', 'unknow', '//pc1.gtimg.com/pcmgr/online_server/images/webadmin/6.png'],
	2: ['危险', 'danger', '//pc1.gtimg.com/pcmgr/online_server/images/webadmin/3.png'],
	3: ['安全网站', 'safe', '//pc1.gtimg.com/pcmgr/online_server/images/webadmin/1.png'],
	4: ['安全网站', 'safe', '//pc1.gtimg.com/pcmgr/online_server/images/webadmin/1.png'],
	13: ['可信度低', 'low', '//pc1.gtimg.com/pcmgr/online_server/images/webadmin/2.png'],
	2001: ['可能涉及钱财，交易需谨慎', 'money', '//pc1.gtimg.com/pcmgr/online_server/images/webadmin/48_money.png']
};
(function($, window, document, undefined) {
	var dataPropertyName = "virtualMouseBindings",
		touchTargetPropertyName = "virtualTouchID",
		virtualEventNames = "vmouseover vmousedown vmousemove vmouseup vclick vmouseout vmousecancel".split(" "),
		touchEventProps = "clientX clientY pageX pageY screenX screenY".split( " " ),
		mouseHookProps = $.event.mouseHooks ? $.event.mouseHooks.props : [],
		mouseEventProps = $.event.props.concat( mouseHookProps ),
		activeDocHandlers = {},
		resetTimerID = 0,
		startX = 0,
		startY = 0,
		didScroll = false,
		clickBlockList = [],
		blockMouseTriggers = false,
		blockTouchTriggers = false,
		eventCaptureSupported = "addEventListener" in document,
		$document = $(document),
		nextTouchID = 1,
		lastTouchID = 0, threshold;
	$.vmouse = {
		moveDistanceThreshold: 10,
		clickDistanceThreshold: 10,
		resetTimerDuration: 1500
	};
	function getNativeEvent(event) {
		while( event && typeof event.originalEvent !== "undefined" ) {
			event = event.originalEvent;
		}
		return event;
	}
	function createVirtualEvent(event, eventType) {
		var t = event.type, oe, props, ne, prop, ct, touch, i, j, len;
		event = $.Event(event);
		event.type = eventType;
		oe = event.originalEvent;
		props = $.event.props;
		if(t.search(/^(mouse|click)/) > -1 ) {
			props = mouseEventProps;
		}
		if(oe) {
			for(i = props.length, prop; i;) {
				prop = props[ --i ];
				event[ prop ] = oe[ prop ];
			}
		}
		if(t.search(/mouse(down|up)|click/) > -1 && !event.which) {
			event.which = 1;
		}
		if(t.search(/^touch/) !== -1) {
			ne = getNativeEvent(oe);
			t = ne.touches;
			ct = ne.changedTouches;
			touch = (t && t.length) ? t[0] : (( ct && ct.length) ? ct[0] : undefined);
			if(touch) {
				for(j = 0, len = touchEventProps.length; j < len; j++) {
					prop = touchEventProps[j];
					event[prop] = touch[prop];
				}
			}
		}
		return event;
	}
	function getVirtualBindingFlags(element) {
		var flags = {},
			b, k;
		while(element) {
			b = $.data(element, dataPropertyName);
			for(k in b) {
				if(b[k]) {
					flags[k] = flags.hasVirtualBinding = true;
				}
			}
			element = element.parentNode;
		}
		return flags;
	}
	function getClosestElementWithVirtualBinding(element, eventType) {
		var b;
		while(element) {
			b = $.data( element, dataPropertyName );
			if(b && (!eventType || b[eventType])) {
				return element;
			}
			element = element.parentNode;
		}
		return null;
	}
	function enableTouchBindings() {
		blockTouchTriggers = false;
	}
	function disableTouchBindings() {
		blockTouchTriggers = true;
	}
	function enableMouseBindings() {
		lastTouchID = 0;
		clickBlockList.length = 0;
		blockMouseTriggers = false;
		disableTouchBindings();
	}
	function disableMouseBindings() {
		enableTouchBindings();
	}
	function startResetTimer() {
		clearResetTimer();
		resetTimerID = setTimeout(function() {
			resetTimerID = 0;
			enableMouseBindings();
		}, $.vmouse.resetTimerDuration);
	}
	function clearResetTimer() {
		if(resetTimerID ) {
			clearTimeout(resetTimerID);
			resetTimerID = 0;
		}
	}
	function triggerVirtualEvent(eventType, event, flags) {
		var ve;
		if((flags && flags[eventType]) ||
					(!flags && getClosestElementWithVirtualBinding(event.target, eventType))) {
			ve = createVirtualEvent(event, eventType);
			$(event.target).trigger(ve);
		}
		return ve;
	}
	function mouseEventCallback(event) {
		var touchID = $.data(event.target, touchTargetPropertyName);
		if(!blockMouseTriggers && (!lastTouchID || lastTouchID !== touchID)) {
			var ve = triggerVirtualEvent("v" + event.type, event);
			if(ve) {
				if(ve.isDefaultPrevented()) {
					event.preventDefault();
				}
				if(ve.isPropagationStopped()) {
					event.stopPropagation();
				}
				if(ve.isImmediatePropagationStopped()) {
					event.stopImmediatePropagation();
				}
			}
		}
	}
	function handleTouchStart(event) {
		var touches = getNativeEvent(event).touches,
			target, flags;
		if(touches && touches.length === 1) {
			target = event.target;
			flags = getVirtualBindingFlags(target);
			if(flags.hasVirtualBinding) {
				lastTouchID = nextTouchID++;
				$.data(target, touchTargetPropertyName, lastTouchID);
				clearResetTimer();
				disableMouseBindings();
				didScroll = false;
				var t = getNativeEvent(event).touches[0];
				startX = t.pageX;
				startY = t.pageY;
				triggerVirtualEvent("vmouseover", event, flags);
				triggerVirtualEvent("vmousedown", event, flags);
			}
		}
	}
	function handleScroll(event) {
		if(blockTouchTriggers) {
			return;
		}
		if(!didScroll) {
			triggerVirtualEvent("vmousecancel", event, getVirtualBindingFlags(event.target));
		}
		didScroll = true;
		startResetTimer();
	}
	function handleTouchMove(event) {
		if(blockTouchTriggers) {
			return;
		}
		var t = getNativeEvent(event).touches[0],
			didCancel = didScroll,
			moveThreshold = $.vmouse.moveDistanceThreshold,
			flags = getVirtualBindingFlags(event.target);
			didScroll = didScroll ||
				(Math.abs(t.pageX - startX) > moveThreshold ||
					Math.abs(t.pageY - startY) > moveThreshold);
		if(didScroll && !didCancel) {
			triggerVirtualEvent("vmousecancel", event, flags);
		}
		triggerVirtualEvent("vmousemove", event, flags);
		startResetTimer();
	}
	function handleTouchEnd(event) {
		if(blockTouchTriggers) {
			return;
		}
		disableTouchBindings();
		var flags = getVirtualBindingFlags(event.target), t;
		triggerVirtualEvent("vmouseup", event, flags);
		if(!didScroll) {
			var ve = triggerVirtualEvent("vclick", event, flags);
			if(ve && ve.isDefaultPrevented()) {
				t = getNativeEvent(event).changedTouches[0];
				clickBlockList.push({
					touchID: lastTouchID,
					x: t.clientX,
					y: t.clientY
				});
				blockMouseTriggers = true;
			}
		}
		triggerVirtualEvent("vmouseout", event, flags);
		didScroll = false;
		startResetTimer();
	}
	function hasVirtualBindings(ele) {
		var bindings = $.data( ele, dataPropertyName ), k;
		if(bindings) {
			for(k in bindings) {
				if(bindings[k]) {
					return true;
				}
			}
		}
		return false;
	}
	function dummyMouseHandler() {}
	function getSpecialEventObject(eventType) {
		var realType = eventType.substr(1);
		return {
			setup: function(data, namespace) {
				if(!hasVirtualBindings(this)) {
					$.data(this, dataPropertyName, {});
				}
				var bindings = $.data(this, dataPropertyName);
				bindings[eventType] = true;
				activeDocHandlers[eventType] = (activeDocHandlers[eventType] || 0) + 1;
				if(activeDocHandlers[eventType] === 1) {
					$document.bind(realType, mouseEventCallback);
				}
				$(this).bind(realType, dummyMouseHandler);
				if(eventCaptureSupported) {
					activeDocHandlers["touchstart"] = (activeDocHandlers["touchstart"] || 0) + 1;
					if(activeDocHandlers["touchstart"] === 1) {
						$document.bind("touchstart", handleTouchStart)
							.bind("touchend", handleTouchEnd)
							.bind("touchmove", handleTouchMove)
							.bind("scroll", handleScroll);
					}
				}
			},
			teardown: function(data, namespace) {
				--activeDocHandlers[eventType];
				if(!activeDocHandlers[eventType]) {
					$document.unbind(realType, mouseEventCallback);
				}
				if(eventCaptureSupported) {
					--activeDocHandlers["touchstart"];
					if(!activeDocHandlers["touchstart"]) {
						$document.unbind("touchstart", handleTouchStart)
							.unbind("touchmove", handleTouchMove)
							.unbind("touchend", handleTouchEnd)
							.unbind("scroll", handleScroll);
					}
				}
				var $this = $(this),
					bindings = $.data(this, dataPropertyName);
				if(bindings) {
					bindings[eventType] = false;
				}
				$this.unbind(realType, dummyMouseHandler);
				if(!hasVirtualBindings(this)) {
					$this.removeData(dataPropertyName);
				}
			}
		};
	}
	for(var i = 0; i < virtualEventNames.length; i++) {
		$.event.special[virtualEventNames[i]] = getSpecialEventObject(virtualEventNames[i]);
	}
	if(eventCaptureSupported) {
		document.addEventListener("click", function(e) {
			var cnt = clickBlockList.length,
				target = e.target,
				x, y, ele, i, o, touchID;
			if(cnt) {
				x = e.clientX;
				y = e.clientY;
				threshold = $.vmouse.clickDistanceThreshold;
				ele = target;
				while(ele) {
					for(i = 0; i < cnt; i++) {
						o = clickBlockList[i];
						touchID = 0;
						if((ele === target && Math.abs(o.x - x) < threshold && Math.abs(o.y - y) < threshold) ||
									$.data(ele, touchTargetPropertyName) === o.touchID) {
							e.preventDefault();
							e.stopPropagation();
							return;
						}
					}
					ele = ele.parentNode;
				}
			}
		}, true);
	}
})(jQuery, window, document);
(function($, window, undefined) {
	function triggercustomevent(obj, eventtype, event) {
		var origtype = event.type;
		event.type = eventtype;
		$.event.handle.call(obj, event);
		event.type = origtype;
	}
	$.event.special.tap = {
		setup : function() {
			var thisobj = this;
			var obj = $(thisobj);
			obj.on('vmousedown', function(e) {
				if(e.which && e.which !== 1) {
					return false;
				}
				var origtarget = e.target;
				var origevent = e.originalEvent;
				var timer;
				function cleartaptimer() {
					clearTimeout(timer);
				}
				function cleartaphandlers() {
					cleartaptimer();
					obj.off('vclick', clickhandler)
						.off('vmouseup', cleartaptimer);
					$(document).off('vmousecancel', cleartaphandlers);
				}
				function clickhandler(e) {
					cleartaphandlers();
					if(origtarget === e.target) {
						triggercustomevent(thisobj, 'tap', e);
					}
					return false;
				}
				obj.on('vmouseup', cleartaptimer)
					.on('vclick', clickhandler)
				$(document).on('touchcancel', cleartaphandlers);
				timer = setTimeout(function() {
					triggercustomevent(thisobj, 'taphold', $.Event('taphold', {target:origtarget}));
				}, 750);
				return false;
			});
		}
	};
	$.each(('tap').split(' '), function(index, name) {
		$.fn[name] = function(fn) {
			return this.on(name, fn);
		};
	});
})(jQuery, this);
var page = {
	converthtml : function() {
		var prevpage = $('div.pg .prev').prop('href');
		var nextpage = $('div.pg .nxt').prop('href');
		var lastpage = $('div.pg label span').text().replace(/[^\d]/g, '') || 0;
		var curpage = $('div.pg input').val() || 1;
		if(!lastpage) {
			prevpage = $('div.pg .pgb a').prop('href');
		}
		var prevpagehref = nextpagehref = '';
		if(prevpage == undefined) {
			prevpagehref = 'javascript:;" class="bg_f b_ok f_d';
		} else {
			prevpagehref = prevpage;
		}
		if(nextpage == undefined) {
			nextpagehref = 'javascript:;" class="bg_f b_ok f_d';
		} else {
			nextpagehref = nextpage;
		}
		var selector = '';
		if(lastpage) {
			selector += '<a id="select_a" class="bg_f b_ok"><i class="comiis_font bg_e b_l">&#xe620;</i>';
			selector += '<select id="dumppage" style="position:absolute;left:0;top:0;height:27px;opacity:0;width:100px;">';
			for(var i=1; i<=lastpage; i++) {
				selector += '<option value="'+i+'" '+ (i == curpage ? 'selected' : '') +'>第'+i+'页</option>';
			}
			selector += '</select>';
			selector += '第 '+curpage+' 页';
		}
		$('div.pg').removeClass('pg').addClass('comiis_page bg_f').html('<a href="'+ prevpagehref +'" class="bg_f b_ok">上一页</a>'+ selector +'<a href="'+ nextpagehref +'" class="bg_f b_ok">下一页</a>');
		$('#dumppage').on('change', function() {
			var href = (prevpage || nextpage);
			if(href.indexOf('page=') > 0){
				window.location.href = href.replace(/page=\d+/, 'page=' + $(this).val());
			}else{
				var comiis_pnum = (href.split('-')).length - 1;
				if(comiis_pnum == 3){				
					window.location.href = href.replace(/-(\d+)-(\d+)-(\d+)\.html/, "-$1-" + $(this).val() + "-$3.html");
				}else{
					window.location.href = href.replace(/-(\d+)-(\d+)\.html/, "-$1-" + $(this).val() + ".html");
				}
			}
		});
	},
};
var atap = {
	init : function() {
		$('.atap').on('tap', function() {
			var obj = $(this);
			obj.css({'background':'#6FACD5', 'color':'#FFFFFF', 'font-weight':'bold', 'text-decoration':'none', 'text-shadow':'0 1px 1px #3373A5'});
			return false;
		});
		$('.atap a').off('click');
	}
};
var comiis_date_style = 0;
var POPMENU = new Object;
var popup = {
	init : function() {
		var $this = this;
		$('.popup').each(function(index, obj) {
			obj = $(obj);
			var pop = $(obj.attr('href'));
			if(pop && pop.attr('popup')) {
				pop.css({'display':'none'});
				obj.on('click', function(e) {
					$this.open(pop);
					return false;
				});
			}
		});
		this.maskinit();
	},
	maskinit : function() {
		var $this = this;
		$('#mask').off().on('tap', function() {
			$this.close();
		});
	},
	open : function(pop, type, url) {
		if(typeof pop == 'string' && pop.indexOf("messagetext") >= 0){
			var output = $(pop).find('#messagetext p').html();
			var output_no = output.indexOf("if(typeof");
			pop = (output_no > 0 ? output.substring(0, output_no) : output);
			converter = null;
			type = 'alert';
		}
		if(typeof pop == 'string' && pop.indexOf("comiis_date_style f_c cl") >= 0 && $('#mask').css("display") == 'block') {
			comiis_date_style = 1;
		}else{
			comiis_date_style = 0;
		}
		if(Comiis_MENUS_on == 1){
			this.comiis_close();
		}
		comiis_menu_hide();
		if(!comiis_date_style){
			this.close();
		}
		if(type == 'alert') {
			if(pop.indexOf("非常感谢，您的主题已发布") >= 0){
				pop = '发布成功';
			}
			var comiis_indexOf = pop.indexOf("if($(");
			if(comiis_indexOf >= 0){
				pop = pop.substr(0, comiis_indexOf);
			}
			pop = pop.replace('[ 点击这里转入主题列表 ]', '');
			$('#comiis_alert').off().css({'display' : 'none', 'left' : '0'}).attr('class', '').text($('<div>'+pop+'</div>').text()).css({'display' : 'block', 'left' : (($(window).width() - $('#comiis_alert').outerWidth()) / 2)})
			setTimeout(function() {
				$('#comiis_alert').addClass("comiis_alert_show").on('webkitTransitionEnd transitionend', function() {
					$(this).off();
					setTimeout(function() {
						$('#comiis_alert').removeClass('comiis_alert_show').addClass("comiis_alert_hide").on('webkitTransitionEnd transitionend', function() {
							$(this).off().removeClass('comiis_alert_hide').text('').css({'display' : 'none', 'left' : '0'});
						});		
					}, '20');
				});
			}, '20');
			return false;
		}
		if(!comiis_date_style){
			this.maskinit();
		}
		if(typeof pop == 'string') {
			if(!comiis_date_style){
				$('#ntcmsg').remove();
			}else{
				$('#comiis_date_style').remove();
			}
			if(type == 'alerts') {
				pop = '<div class="comiis_tip bg_f cl"><dt class="f_b"><p>'+ pop +'</p></dt><dd class="b_t cl"><a href="javascript:;" onclick="popup.close();" class="tip_btn tip_all bg_f f_b">确定</a></dd></div>'
			} else if(type == 'confirm') {			
			if(comiis_post_btnwz == 1){
				pop = '<div class="comiis_tip bg_f cl"><dt class="f_b"><p>'+ pop +'</p></dt><dd class="b_t cl"><a href="javascript:;" onclick="popup.close();" class="tip_btn bg_f f_b">取消</a><a href="'+ url +'" class="tip_btn bg_f f_0"><span class="tip_lx">确定</span></a></dd></div>'
			}else{
				pop = '<div class="comiis_tip bg_f cl"><dt class="f_b"><p>'+ pop +'</p></dt><dd class="b_t cl"><a href="'+ url +'" class="tip_btn bg_f f_0">确定</a><a href="javascript:;" onclick="popup.close();" class="tip_btn bg_f f_b"><span class="tip_lx">取消</span></a></dd></div>'
			}			
			}
			$('body').append('<div id="'+(comiis_date_style ? 'comiis_date_style' : 'ntcmsg')+'" style="display:none;">'+ pop +'</div>');
			pop = $((comiis_date_style ? '#comiis_date_style' : '#ntcmsg'));
		}
		if(pop.attr('comiis_popup') == "comiis"){
			var $this = this;
			Comiis_MENUS_on = 1;
			$('.comiis_glclose').off().on('tap', function() {
				$this.comiis_close();
				return false;
			});
			$('#comiis_bgbox').off().on('tap', function() {
				$this.comiis_close();
				return false;
			}).css({
				'display':'block',
				'width':'100%',
				'height':'100%',
				'position':'fixed',
				'top':'0',
				'left':'0',
				'background':'#000',
				'opacity' : '.7',
				'z-index':'101'
			});
			pop.css('display','block');
			setTimeout(function() {
				pop.addClass("comiis_share_box_show");
			}, 20);
			return false;
		}
		var comiis_textarea = $('#' + pop.attr('id') + ' textarea').length > 0 ? 1 : 0;
		var html_box = pop.html().replace(/-comiis_htmlid-/gm, "newid_");
		
		if(POPMENU[pop.attr('id')]) {
			$('#' + pop.attr('id') + '_popmenu').html(html_box).css({'height':pop.height()+'px', 'width':comiis_textarea ? '90%' : pop.width()+'px'});
		} else {
			pop.parent().append('<div class="dialogbox" id="'+ pop.attr('id') +'_popmenu" style="height:'+ pop.height() +'px;width:'+ (comiis_textarea ? '90%' : pop.width()) +'px;">'+ html_box +'</div>');
		}
		var popupobj = $('#' + pop.attr('id') + '_popmenu');
		var left = comiis_textarea ? '5%' : (window.innerWidth - popupobj.width()) / 2;
		var top = comiis_textarea ? '70px' : (document.documentElement.clientHeight - popupobj.height()) / 2;
		var z_index = comiis_date_style ? '125' : '120'
		popupobj.css({'display':'block','position':'fixed','left':left,'top':top,'z-index':z_index,'opacity':1});
		
		comiis_textarea ? (popupobj.hasClass("comiis_textarea_box") ? '' : popupobj.addClass('comiis_textarea_box')) : popupobj.removeClass('comiis_textarea_box');
		
		if(comiis_date_style){
			$('#comiis_menu_bg').off().on('touchstart', function() {
				comiis_closedate();
				$(this).css('display','none');
				return false;
			}).css({
				'display':'block',
				'width':'100%',
				'height':'100%',
				'position':'fixed',
				'top':'0',
				'left':'0',
				'background':'transparent',
				'z-index':'121'
			});
		}else{
			$('#mask').css({'display':'block','width':'100%','height':'100%','position':'fixed','top':'0','left':'0','background':'black','opacity':'0.6','z-index':'100'});
		}
		POPMENU[pop.attr('id')] = pop;
		$('#ntcmsg').remove();
		
		Comiis_Touch_on = 0;
	},
	comiis_close : function() {
		Comiis_Touch_on = 1;
		Comiis_MENUS_on = 0;
		$('#comiis_bgbox').css('display', 'none');
		$('.comiis_popup').removeClass("comiis_share_box_show");
	},
	close : function() {
		Comiis_Touch_on = 1;
		$('#mask').css('display', 'none');
		$.each(POPMENU, function(index, obj) {
			$('#' + index + '_popmenu').css('display','none');
		});
		comiis_date_style = 0;
	}
};
var dialog = {
	init : function() {
		$(document).on('click', '.dialog', function() {
			var obj = $(this);
			if(obj.attr('href').indexOf("&repquote=") > 0 && $('#fastpostsubmitline input').length >1){
				window.location.href = obj.attr('href');
				return false;
			}
			if(!obj.attr('comiis')){
				popup.open('<img src="' + IMGDIR + '/imageloading.gif" class="comiis_loading">');
			}else{
				popup.close();
			}
			$.ajax({
				type : 'GET',
				url : obj.attr('href') + '&inajax=1',
				dataType : 'xml'
			})
			.success(function(s) {
				if(obj.attr('comiis') == 'handle'){
					if(comiis_ishandle(s.lastChild.firstChild.nodeValue)){
						return false;
					}
				}
				popup.open(s.lastChild.firstChild.nodeValue);
				evalscript(s.lastChild.firstChild.nodeValue);
			})
			.error(function() {
				window.location.href = obj.attr('href');
				popup.close();
			});
			return false;
		});
	},
};
function comiis_ishandle(s) {
	if(s.indexOf("typeof succeedhandle_") > 0 || s.indexOf("typeof errorhandle_") > 0){
		var r = s.match(/<script.*>if(.*?)<\/script>/);
		if(r != null){
			appendscript('', 'if'+r[1], true);
			return true;
		}
	}
	return false;
}
var formdialog = {
	init : function() {
		$(document).on('click', '.formdialog', function() {
			comiis_prevent_post('button,:button,:submit', 1);
			var obj = $(this);
			if(obj.attr('onsubmit')){
				eval('var $return_data=' + obj.attr('onsubmit') + ';');
				if($return_data == 1){
					return false;
				}
			}
			if(!obj.attr('comiis')){
				popup.open('<img src="' + IMGDIR + '/imageloading.gif" class="comiis_loading">');
			}else{
				popup.close();
			}
			var formobj = $(this.form);
			$.ajax({
				type:'POST',
				url:formobj.attr('action') + '&handlekey='+ formobj.attr('id') +'&inajax=1',
				data:formobj.serialize(),
				dataType:'xml'
			})
			.success(function(s) {
				comiis_prevent_post('button,:button,:submit', 0);
				if(obj.attr('comiis') == 'handle'){
					if(comiis_ishandle(s.lastChild.firstChild.nodeValue)){
						return false;
					}
				}
				if(obj.attr('comiis') == 'pay'){
					if(s.lastChild.firstChild.nodeValue){
						s.lastChild.firstChild.nodeValue = s.lastChild.firstChild.nodeValue.replace('$(\'payform\')','$(\'#payform\')');
					}
				}	
				popup.open(s.lastChild.firstChild.nodeValue);
				evalscript(s.lastChild.firstChild.nodeValue);
			})
			.error(function() {
				popup.open('Ajax 出错!', 'alert');
				popup.close();
				comiis_prevent_post('button,:button,:submit', 0);
			});
			return false;
		});
	}
};
var redirect = {
	init : function() {
		$(document).on('click', '.redirect', function() {
			var obj = $(this);
			popup.close();
			window.location.href = obj.attr('href');
		});
	}
};
var DISMENU = new Object;
var display = {
	init : function() {
		var $this = this;
		$('.display').each(function(index, obj) {
			obj = $(obj);
			var dis = $(obj.attr('href'));
			if(dis && dis.attr('display')) {
				dis.css({'display':'none'});
				dis.css({'z-index':'102'});
				DISMENU[dis.attr('id')] = dis;
				obj.on('click', function(e) {
					if(in_array(e.target.tagName, ['A', 'IMG', 'INPUT'])) return;
					$this.maskinit();
					if(dis.attr('display') == 'true') {
						comiis_menu_hide();
						dis.css('display', 'block');
						dis.attr('display', 'false');
						$('#mask').css({'display':'block','width':'100%','height':'100%','position':'fixed','top':'0','left':'0','background':'transparent','z-index':'100'});
					}
					return false;
				});
			}
		});
	},
	maskinit : function() {
		var $this = this;
		$('#mask').off().on('touchstart', function() {
			$this.hide();
			return false;
		});
	},
	hide : function() {
		$('#mask').css('display', 'none');
		$.each(DISMENU, function(index, obj) {
			obj.css('display', 'none');
			obj.attr('display', 'true');
		});
	}
};
var geo = {
	latitude : null,
	longitude : null,
	loc : null,
	errmsg : null,
	timeout : 5000,
	getcurrentposition : function() {
		if(!!navigator.geolocation) {
			navigator.geolocation.getCurrentPosition(this.locationsuccess, this.locationerror, {
				enableHighAcuracy : true,
				timeout : this.timeout,
				maximumAge : 3000
			});
		}
	},
	locationerror : function(error) {
		geo.errmsg = 'error';
		switch(error.code) {
			case error.TIMEOUT:
				geo.errmsg = "获取位置超时，请重试";
				break;
			case error.POSITION_UNAVAILABLE:
				geo.errmsg = '无法检测到您的当前位置';
			    break;
		    case error.PERMISSION_DENIED:
		        geo.errmsg = '请允许能够正常访问您的当前位置';
		        break;
		    case error.UNKNOWN_ERROR:
		        geo.errmsg = '发生未知错误';
		        break;
		}
	},
	locationsuccess : function(position) {
		geo.latitude = position.coords.latitude;
		geo.longitude = position.coords.longitude;
		geo.errmsg = '';
		$.ajax({
			type:'POST',
			url:'http://maps.google.com/maps/api/geocode/json?latlng=' + geo.latitude + ',' + geo.longitude + '&language=zh-CN&sensor=true',
			dataType:'json'
		})
		.success(function(s) {
			if(s.status == 'OK') {
				geo.loc = s.results[0].formatted_address;
			}
		})
		.error(function() {
			geo.loc = null;
		});
	}
};
jQuery.cookie = function(name, value, options) {
	if (typeof value != 'undefined') {
		options = options || {};
		if (value === null) {
			value = '';
			options.expires = -1;
		}
		var expires = '';
		if (options.expires && (typeof options.expires == 'number' || options.expires.toUTCString)) {
			var date;
			if (typeof options.expires == 'number') {
				date = new Date();
				date.setTime(date.getTime() + (options.expires * 24 * 60 * 60 * 1000));
			} else {
				date = options.expires;
			}
			expires = '; expires=' + date.toUTCString();
		}
		var path = options.path ? '; path=' + options.path : '';
		var domain = options.domain ? '; domain=' + options.domain : '';
		var secure = options.secure ? '; secure' : '';
		document.cookie = [name, '=', encodeURIComponent(value), expires, path, domain, secure].join('');
	} else {
		var cookieValue = null;
		if (document.cookie && document.cookie != '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				if (cookie.substring(0, name.length + 1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
};
var Comiis_Touch = {
	init : function(a, b){
		this.TouchStartX = 0;
		this.TouchStartY = 0;
		this.TouchendX = 0;
		this.TouchendY = 0;	
		this.TouchMoves = 0;
		this.TouchDirection = 'n';
		this.Touchstime = 0;
		this.Touchon = 0;
		this.Toucha = $(a);
		this.TouchscrollTop = 0;
		this.TouchStart = b.TouchStart;
		this.TouchMove = b.TouchMove;
		this.TouchEnd = b.TouchEnd;
		this.Toucha.on("touchstart", this.onTouchStart);
	},
	onTouchStart : function(e){
		if(Comiis_Touch_on == 1){
			Comiis_Touch_on = 2;
		}
		var n = e.originalEvent.changedTouches[0];
		Comiis_Touch.TouchStartX = (n.pageX).toFixed(2);
		Comiis_Touch.TouchStartY = (n.pageY).toFixed(2);
		Comiis_Touch.TouchDirection = 'n';
		Comiis_Touch.TouchendX = 0;
		Comiis_Touch.TouchendY = 0;
		Comiis_Touch.Touchon = 0;
		Comiis_Touch.TouchscrollTop = $(window).scrollTop();
		Comiis_Touch.Touchstime = new Date().getTime();
		if(Comiis_Touch_on != 0){
			Comiis_Touch.Toucha.on("touchmove", Comiis_Touch.onTouchMove);
		}
		Comiis_Touch.Toucha.on("touchend", Comiis_Touch.onTouchEnd);
		if(typeof Comiis_Touch.TouchStart == 'function') {
			Comiis_Touch.TouchStart();
		}
	},
	onTouchMove : function(e){
		if(Comiis_Touch_on == 0){
			return;
		}
		var n = e.originalEvent.changedTouches[0];
		Comiis_Touch.TouchendX = (n.pageX).toFixed(2);
		Comiis_Touch.TouchendY = (n.pageY).toFixed(2);
		X = (n.pageX - Comiis_Touch.TouchStartX).toFixed(2);
		Y = (n.pageY - Comiis_Touch.TouchStartY).toFixed(2);
		if (Math.abs(Y) > Math.abs(X) && Y > 0 && $(window).scrollTop() <= 0 && (Comiis_Touch.Touchon ==0 || Comiis_Touch.Touchon == 1) && !$('.comiis_body').hasClass('comiis_showleftnv') && Comiis_Touch_on != 2) {
			e.preventDefault();
			Comiis_Touch.TouchDirection = 'top';
			Comiis_Touch.TouchMoves = Y;
		}else if (Math.abs(Y) > Math.abs(X) && Y < 0 && ($(window).scrollTop() + $(window).height()) >= $(document).height() && (Comiis_Touch.Touchon ==0 || Comiis_Touch.Touchon == 2) && !$('.comiis_body').hasClass('comiis_showleftnv') && Comiis_Touch_on != 2) {
			e.preventDefault();
			Comiis_Touch.TouchDirection = 'bottom';
			Comiis_Touch.TouchMoves = -Y;
		}else if (Math.abs(X) > Math.abs(Y) && X > 0 && $(document).scrollLeft() <= 0 && Comiis_Touch.TouchscrollTop == $(window).scrollTop() && (Comiis_Touch.Touchon ==0 || Comiis_Touch.Touchon == 3) && !$('.comiis_body').hasClass('comiis_showleftnv') && Comiis_Touch_on != 3) {
			e.preventDefault();
			Comiis_Touch.TouchDirection = 'left';
			Comiis_Touch.TouchMoves = X;
		}else if (Math.abs(X) > Math.abs(Y) && X < 0 && ($(document).scrollLeft() + $(window).width()) >= $(document).width() && Comiis_Touch.TouchscrollTop == $(window).scrollTop() && (Comiis_Touch.Touchon ==0 || Comiis_Touch.Touchon == 4) && Comiis_Touch_on != 3) {
			e.preventDefault();
			Comiis_Touch.TouchDirection = 'right';
			Comiis_Touch.TouchMoves = -X;
		}
		if(typeof Comiis_Touch.TouchMove == 'function') {
			Comiis_Touch.TouchMove();
		}
	},
	onTouchEnd : function(){
		if(typeof Comiis_Touch.TouchEnd == 'function') {
			Comiis_Touch.TouchEnd();
		}
		Comiis_Touch.Toucha.off("touchmove", Comiis_Touch.onTouchMove);
		Comiis_Touch.Toucha.off("touchend", Comiis_Touch.onTouchEnd);
	},
	ontouchcancel : function(){
		if(typeof Comiis_Touch.TouchEnd == 'function') {
			Comiis_Touch.TouchEnd();
		}
		Comiis_Touch.Toucha.off("touchmove", Comiis_Touch.onTouchMove);
		Comiis_Touch.Toucha.off("touchend", Comiis_Touch.onTouchEnd);
	}
};
(function($){
	$.fn.extend({
		comiis_insert: function(a){
			var $comiis=$(this)[0];
			if ($comiis.selectionStart || $comiis.selectionStart == '0') {
				var startPos = $comiis.selectionStart;
				var endPos = $comiis.selectionEnd;
				$comiis.value = $comiis.value.substring(0, startPos) + a + $comiis.value.substring(endPos, $comiis.value.length);
				$comiis.selectionStart = $comiis.selectionEnd = startPos + a.length;
			}else {
				this.value += a;
			}
			$comiis.focus();
		},
		comiis_delete: function(){
			var $comiis=$(this)[0];
			var is_smilies = -1;
			if ($comiis.selectionStart && ($comiis.selectionStart == $comiis.selectionEnd)) {
				var startPos = $comiis.selectionStart;
				var startText = $comiis.value.substring(0, startPos);
				var endText = $comiis.value.substring(startPos, $comiis.value.length);
				var comiis_smilies_len = 0, delStart = 0, comiis_startText_lendata = '';
				for(i in comiis_smilies_array) {
					comiis_smilies_len = comiis_smilies_array[i][0].length;
					comiis_startText_lendata = startText.substring(startText.length - comiis_smilies_len, startText.length);
					if(in_array(comiis_startText_lendata, comiis_smilies_array[i])){
						delStart = startText.length - comiis_smilies_len;
						$comiis.value = startText.substring(0, delStart)  + endText;
						$comiis.selectionStart = $comiis.selectionEnd = delStart;
						is_smilies = 1;
						break;
					}
				}
				if(is_smilies == 1){
					return false;
				}else{
					var comiis_sall_Text = comiis_sleft_Text = comiis_sright_Text = '';
					var comiis_smilies_len = comiis_sleft_length = 0;
					for(o in comiis_smilies_array) {
						comiis_smilies_len = comiis_smilies_array[o][0].length;
						comiis_sleft_Text = $comiis.value.substring(startPos - comiis_smilies_len + 1, startPos);
						comiis_sright_Text = $comiis.value.substring(startPos, startPos + comiis_smilies_len - 1);
						comiis_sleft_length = comiis_sleft_Text.length;
						comiis_sall_Text = comiis_sleft_Text + comiis_sright_Text;
						for(p in comiis_smilies_array[o]) {
							is_smilies = comiis_sall_Text.indexOf(comiis_smilies_array[o][p]);
							if(is_smilies >= 0){
								var startText = $comiis.value.substring(0, startPos - comiis_sleft_length + is_smilies);
								var endText = $comiis.value.substring(startPos - comiis_sleft_length + is_smilies + comiis_smilies_len, $comiis.value.length);
								$comiis.value = startText + endText;
								$comiis.selectionStart = $comiis.selectionEnd = startText.length;	
								return false;
							}
						}
					}
				}
			}
		}
	})
})(jQuery);
function mygetnativeevent(event) {
	while(event && typeof event.originalEvent !== "undefined") {
		event = event.originalEvent;
	}
	return event;
}
function evalscript(s) {
	if(s.indexOf('<script') == -1) return s;
	var p = /<script[^\>]*?>([^\x00]*?)<\/script>/ig;
	var arr = [];
	while(arr = p.exec(s)) {
		var p1 = /<script[^\>]*?src=\"([^\>]*?)\"[^\>]*?(reload=\"1\")?(?:charset=\"([\w\-]+?)\")?><\/script>/i;
		var arr1 = [];
		arr1 = p1.exec(arr[0]);
		if(arr1) {
			appendscript(arr1[1], '', arr1[2], arr1[3]);
		} else {
			p1 = /<script(.*?)>([^\x00]+?)<\/script>/i;
			arr1 = p1.exec(arr[0]);
			appendscript('', arr1[2], arr1[1].indexOf('reload=') != -1);
		}
	}
	return s;
}
var safescripts = {}, evalscripts = [];
function appendscript(src, text, reload, charset) {
	var id = hash(src + text);
	if(!reload && in_array(id, evalscripts)) return;
	if(reload && $('#' + id)[0]) {
		$('#' + id)[0].parentNode.removeChild($('#' + id)[0]);
	}
	evalscripts.push(id);
	var scriptNode = document.createElement("script");
	scriptNode.type = "text/javascript";
	scriptNode.id = id;
	scriptNode.charset = charset ? charset : (!document.charset ? document.characterSet : document.charset);
	try {
		if(src) {
			scriptNode.src = src;
			scriptNode.onloadDone = false;
			scriptNode.onload = function () {
				scriptNode.onloadDone = true;
				JSLOADED[src] = 1;
			};
			scriptNode.onreadystatechange = function () {
				if((scriptNode.readyState == 'loaded' || scriptNode.readyState == 'complete') && !scriptNode.onloadDone) {
					scriptNode.onloadDone = true;
					JSLOADED[src] = 1;
				}
			};
		} else if(text){
			scriptNode.text = text;
		}
		document.getElementsByTagName('head')[0].appendChild(scriptNode);
	} catch(e) {}
}
function hash(string, length) {
	var length = length ? length : 32;
	var start = 0;
	var i = 0;
	var result = '';
	filllen = length - string.length % length;
	for(i = 0; i < filllen; i++){
		string += "0";
	}
	while(start < string.length) {
		result = stringxor(result, string.substr(start, length));
		start += length;
	}
	return result;
}
function stringxor(s1, s2) {
	var s = '';
	var hash = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
	var max = Math.max(s1.length, s2.length);
	for(var i=0; i<max; i++) {
		var k = s1.charCodeAt(i) ^ s2.charCodeAt(i);
		s += hash.charAt(k % 52);
	}
	return s;
}
function in_array(needle, haystack) {
	if(typeof needle == 'string' || typeof needle == 'number') {
		for(var i in haystack) {
			if(haystack[i] == needle) {
					return true;
			}
		}
	}
	return false;
}
function isUndefined(variable) {
	return typeof variable == 'undefined' ? true : false;
}
function setcookie(cookieName, cookieValue, seconds, path, domain, secure) {
	if(cookieValue == '' || seconds < 0) {
		cookieValue = '';
		seconds = -2592000;
	}
	if(seconds) {
		var expires = new Date();
		expires.setTime(expires.getTime() + seconds * 1000);
	}
	domain = !domain ? cookiedomain : domain;
	path = !path ? cookiepath : path;
	document.cookie = escape(cookiepre + cookieName) + '=' + escape(cookieValue)
		+ (expires ? '; expires=' + expires.toGMTString() : '')
		+ (path ? '; path=' + path : '/')
		+ (domain ? '; domain=' + domain : '')
		+ (secure ? '; secure' : '');
}
function getcookie(name, nounescape) {
	name = cookiepre + name;
	var cookie_start = document.cookie.indexOf(name);
	var cookie_end = document.cookie.indexOf(";", cookie_start);
	if(cookie_start == -1) {
		return '';
	} else {
		var v = document.cookie.substring(cookie_start + name.length + 1, (cookie_end > cookie_start ? cookie_end : document.cookie.length));
		return !nounescape ? unescape(v) : v;
	}
}
function comiis_input_style(){
	setTimeout(function(){
		$(document).on('change', '.comiis_input_style :checkbox,.comiis_input_style :radio,.comiis_input_style select', function(){
			comiis_input_set_style($(this));
	   });
		if($('.comiis_input_style :checkbox,.comiis_input_style :radio,.comiis_input_style select').length > 0) {
			$(".comiis_input_style :checkbox,.comiis_input_style :radio,.comiis_input_style select").each(function(){
				comiis_input_set_style($(this));
			});
		}
	}, 25);
}
function comiis_input_set_style(obj){
	if(obj.is(":radio") || obj.is(":checkbox")){
		var comiis_input = $('[for="' + obj.attr('id')+'"]');
		
		if(obj.hasClass('comiis_checkbox_key')){
			if (obj.is(":checked")) {
				comiis_input.children(".comiis_checkbox").removeClass('comiis_checkbox_close');
			}else{
				comiis_input.children(".comiis_checkbox").addClass('comiis_checkbox_close');
			}
		}else{
			if (obj.is(":checked")) {
				if(obj.is(":radio")){
					$('input[name="' + obj.attr('name') + '"]').next().children("i").html('&#xe646;').removeClass('f_0').addClass('f_d');
					comiis_input.children("i").html('&#xe645;').removeClass('f_d').addClass('f_0');
				}else{
					comiis_input.children("i").html('&#xe644;').removeClass('f_d').addClass('f_0');
				}
			}else{
				comiis_input.children("i").html(obj.is(":radio") ? '&#xe646;' : '&#xe643;').removeClass('f_0').addClass('f_d');
			}
		}
	}else{
		$('#' + obj.attr('id') + '_name').text(obj.find('option:selected').text());
	}
}
function comiis_menu_display() {
	$('.comiis_menu_display').each(function(index, comiis_menu) {
		comiis_menu = $(comiis_menu);
		var comiis_menu_box = $('#' + comiis_menu.attr('id') + "_menu");
		comiis_menu_box.addClass('comiis_menu_style');
		if(comiis_menu.length > 0 && comiis_menu_box.length > 0) {
			Comiis_MENU_Data[comiis_menu_box.attr('id')] = comiis_menu_box;
			comiis_menu.on('click', function(e) {
				if(Comiis_MENU_on == 0){
					//if(in_array(e.target.tagName, ['A', 'IMG', 'INPUT'])) return;
					Comiis_MENU_on = 1;
					popup.close();
					$('#comiis_menu_bg').off().on('touchstart', function() {
						comiis_menu_hide();
						comiis_menu.removeClass('comiis_menu_no');
						return false;
					}).css({
						'display':'block',
						'width':'100%',
						'height':'100%',
						'position':'fixed',
						'top':'0',
						'left':'0',
						'background':'transparent',
						'z-index':'101'
					});
					$(this).addClass('comiis_menu_no');
					comiis_menu_box.css({'display':'block', 'z-index':'102'});
					comiis_scrollTop = $(window).scrollTop();
					comiis_menu_box.addClass("comiis_menu_display_show");
				}
			});
		}
	});
}
function comiis_menu_hide() {
	if(Comiis_MENU_on == 1){
		$('#comiis_menu_bg').css('display', 'none');
		if($('.wxlist_bottom_box').length > 0) {
			$('.wxlist_bottom_box').css('width', '0');
		}
		$.each(Comiis_MENU_Data, function(index, comiis_menu_boxs) {
			comiis_menu_boxs.removeClass("comiis_menu_display_show").addClass('comiis_menu_display_hidden').on('webkitTransitionEnd transitionend', function() {
				$(this).off('webkitTransitionEnd transitionend').css('display', 'none').removeClass('comiis_menu_display_hidden');
				Comiis_MENU_on = 0;
			});
		});
		return false;
	}
}
function succeedhandle_(a, b, c){
	comiis_break();
}
function succeedhandle_mods(a, b, c){
	comiis_break();
}
function succeedhandle_comiis(a, b, c){
	comiis_break();
}
function comiis_break(){
	setTimeout(function() {
		location.reload();
	}, '1000');
}
function comiis_leftnv(){
	if($('.comiis_sidenv_box').length > 0){
		if(!$('.comiis_body').hasClass('comiis_showleftnv')){
			$('body').css({'height' : '100%','width' : '100%', 'overflow' : 'hidden'});
			$('.comiis_leftmenubg,.comiis_sidenv_box').css({'display' : 'block'});
			comiis_scrollTop = $(window).scrollTop();
			// $('.sidenv_li').height($(window).height() - 125);
			$('.comiis_body').css({'height' : '100%', 'overflow' : 'hidden'}).scrollTop(comiis_scrollTop).removeClass('comiis_hideleftnv').addClass("comiis_showleftnv");
			$('.comiis_sidenv_box').on('webkitTransitionEnd transitionend', function() {
				$(this).off('webkitTransitionEnd transitionend');
				$('.sidenv_li ul').css({'overflow-y' : 'scroll'});
				$('.comiis_leftmenubg').on("click", comiis_leftnv);
			});
		}else{
			$('.comiis_leftmenubg').off("click", comiis_leftnv);
			$('.sidenv_li ul').css({'overflow-y': ''});
			$('.comiis_body').removeClass("comiis_showleftnv").addClass('comiis_hideleftnv').on('webkitTransitionEnd transitionend', function() {
				$('.comiis_sidenv_box,.comiis_leftmenubg').css({'display' : 'none'});
				$(this).off('webkitTransitionEnd transitionend').removeClass('comiis_hideleftnv').css({'height' : '', 'overflow' : ''});
				$('body').css({'height' : '','width' : '', 'overflow' : ''});
				$(window).scrollTop(comiis_scrollTop);
			});
		}
	}
}
function comiis_fmenu(a){
	id = $(a);
	if(id.css("display") == 'none'){
		Comiis_Touch_on = 0;
		id.css("display" , "block");
		id.css({
			"width" :  $(window).width(),
			"height" :  $(window).height()
		});
		$('.comiis_over_box').css('height', $(window).height() - 44);
		setTimeout(function() {
			id.addClass('comiis_fmenu_show');
		}, 60);
	}else{
		id.removeClass("comiis_fmenu_show").on('webkitTransitionEnd transitionend', function() {
			$(this).off('webkitTransitionEnd transitionend').css({'display' : 'none'});
			Comiis_Touch_on = 1;
		});
	}
}
function comiis_getday(id, Year, Month, day, istime){
    var d = new Date(Year, Month, 0);
	var html = '';
	for(var k = 1; k <= d.getDate(); k++) {
		html += '<option value="' + ( k < 10 ? '0' : '') + k + '"' + (k == day ? 'selected="selected"' : '') + '>' + ( k < 10 ? '0' : '') + k + '日</option>'; 
	}
	$('.dialogbox #' + id + '_date .comiis_date_days').html(html);  
	$('.dialogbox #' + id + '_date .comiis_date_years_name').text($('.dialogbox #' + id + '_date .comiis_date_years').find('option:selected').text());
	$('.dialogbox #' + id + '_date .comiis_date_months_name').text($('.dialogbox #' + id + '_date .comiis_date_months').find('option:selected').text());
	$('.dialogbox #' + id + '_date .comiis_date_days_name').text($('.dialogbox #' + id + '_date .comiis_date_days').find('option:selected').text());
	if(istime){
		$('.dialogbox #' + id + '_date .comiis_date_hs_name').text($('.dialogbox #' + id + '_date .comiis_date_hs').find('option:selected').text());
		$('.dialogbox #' + id + '_date .comiis_date_ms_name').text($('.dialogbox #' + id + '_date .comiis_date_ms').find('option:selected').text());
	}
}
function comiis_parsedate(s) {
	/(\d+)\-(\d+)\-(\d+)\s*(\d*):?(\d*)/.exec(s);
	var m1 = (RegExp.$1 && RegExp.$1 > 1899 && RegExp.$1 < 2101) ? parseFloat(RegExp.$1) : today.getFullYear();
	var m2 = (RegExp.$2 && (RegExp.$2 > 0 && RegExp.$2 < 13)) ? parseFloat(RegExp.$2) : today.getMonth() + 1;
	var m3 = (RegExp.$3 && (RegExp.$3 > 0 && RegExp.$3 < 32)) ? parseFloat(RegExp.$3) : today.getDate();
	var m4 = (RegExp.$4 && (RegExp.$4 > -1 && RegExp.$4 < 24)) ? parseFloat(RegExp.$4) : 0;
	var m5 = (RegExp.$5 && (RegExp.$5 > -1 && RegExp.$5 < 60)) ? parseFloat(RegExp.$5) : 0;
	/(\d+)\-(\d+)\-(\d+)\s*(\d*):?(\d*)/.exec("0000-00-00 00\:00");
	return new Date(m1, m2 - 1, m3, m4, m5);
}
function comiis_closedate(){
	if(comiis_date_style == 1){
		$('#comiis_date_style_popmenu').css('display', 'none');
		$('#comiis_menu_bg').css('display', 'none');
	}else{
		popup.close();
	}
}
function comiis_setdate(id, istime){
	var this_id = $('#' + id);
	var date = $('.dialogbox #' + id + '_date .comiis_date_years').find('option:selected').val() + '-' + $('.dialogbox #' + id + '_date .comiis_date_months').find('option:selected').val() + '-' + $('.dialogbox #' + id + '_date .comiis_date_days').find('option:selected').val() + ' ' + (istime == 'true' ? $('.dialogbox #' + id + '_date .comiis_date_hs').find('option:selected').val() + ':' + $('.dialogbox #' + id + '_date .comiis_date_ms').find('option:selected').val() : '');
	this_id.val(date);
	var title = this_id.parent().find('span').first().text().replace(/\*|\:/ig, '');
	if(comiis_date_style == 1){
		comiis_closedate();
	}else{
		
		popup.open(title ? title + '已更改' : '日期' + (this_id.hasClass("comiis_dateshow") ? '时间' : '') + '已更改', 'alert');
	}
	if(this_id.attr('comiis_change')){
		eval(this_id.attr('comiis_change') + '(\''+date+'\');');
	}
}
function textarea_scrollHeight(obj){
	var scrollHeight = obj[0].scrollHeight;
	if(scrollHeight > 72) {
		obj.css('height', (scrollHeight < 192 ? scrollHeight : 192) + 'px');
	}
}
function comiis_leftnv2(){
	var comiis_gobtn_tbox = $('.comiis_gobtn_tbox');
	var comiis_gobtn_tbox_head_height = 0;
	if(!$('#comiis_head').hasClass('comiis_head_hidden')){
		comiis_gobtn_tbox_head_height = $('#comiis_head').height();
	}
	if(!comiis_gobtn_tbox.hasClass('comiis_gobtn_tbox_on')){
		comiis_gobtn_tbox.css({'transform':'translateY('+comiis_gobtn_tbox_head_height+'px)'}).addClass('comiis_gobtn_tbox_on');
		$('.comiis_leftmenubg').on("click", comiis_leftnv2).css({'display' : 'block','opacity':'.5','z-index':'150'});
	}else{
		comiis_gobtn_tbox.attr('style','').removeClass('comiis_gobtn_tbox_on');
		$('.comiis_leftmenubg').off().css({'display' : 'none','opacity':'0'});
	}
}
var img = {
	init : function() {
		$('img').on('error', function() {
			$(this).attr('src', './template/comiis_app/comiis/img/img_err.gif');
		});
	}
};
$(document).ready(function() {
	setTimeout(function() {
		if (history && history.pushState && history.replaceState && history.length < 2) {
			var t = location.href;
			history.replaceState(null , "comiis_main_Page", SITEURL),
			history.pushState(null , "comiis_Page", t),
			window.onpopstate = function() {
				setTimeout(function() {
					location.replace(location.href)
				}, 100)
			}
		}
	}, 100);
	$(document).on('click', 'a', function(e) {
		var obj = $(this);
		var href = obj.attr("href");
		if(typeof(href) != "undefined" && href.indexOf('javascript:') === -1 && href.indexOf('#') === -1 && !obj.hasClass('dialog')){
			e.preventDefault();
			if(comiis_open_wblink == 1){
				if(href.substr(0,7) == 'http://' || href.substr(0,8) == 'https://' || href.substr(0,2) == '//' || href.indexOf('://') > -1){
					for(x in comiis_all_https){
						if(href.indexOf(comiis_all_https[x]) > -1){
							document.location.href = href;
							return false;
						}
					}
					if(comiis_open_wblink_tip == 1){
						popup.open(comiis_open_wblink_txt, 'confirm', 'misc.php?op=url&mod=faq&url=' + escape(href));
					}else{
						document.location.href = 'misc.php?op=url&mod=faq&url=' + escape(href);
					}
					return false;
				}
			}
			document.location.href = href;
			return false;
		}
	});	
	if($('div.pg').length > 0) {
		page.converthtml();
	}
	if($('img').length > 0) {
		img.init();
	}
	if($('.popup').length > 0) {
		popup.init();
	}
	if($('.display').length > 0) {
		display.init();
	}
	if($('.atap').length > 0) {
		atap.init();
	}
	
	if($('.comiis_input_style').length > 0) {
		comiis_input_style();
	}
	dialog.init();
	formdialog.init();
	redirect.init();
	if(typeof(sessionStorage) != 'undefined'){
		if(sessionStorage.getItem('comiis_showid') != 'true' && comiis_lrshow == 0){
			$('.comiis_lrmenu').removeClass('comiis_lrshow');
		}
		$(window).on('unload', function(){
			sessionStorage.setItem('comiis_showid', $('.comiis_lrmenu').hasClass('comiis_lrshow'));
		});
	}	
	comiis_page_start = 1;
	if($('.comiis_menu_display').length > 0) {
		comiis_menu_display();
	}
	if($('textarea').length > 0) {
		$(document).on('keyup', 'textarea', function(){
			var obj = $(this);
			textarea_scrollHeight(obj)
		});
		$('textarea').each(function(index, comiis_menu) {
			var obj = $(comiis_menu);
			textarea_scrollHeight(obj)
		});
	}
	$(document).on('click', '.comiis_leftnv_top_key', function(e) {
		comiis_leftnv2();
	});
	var comiis_scroll_right_time = setTimeout(function(){
		$('.comiis_footer_scroll').addClass('comiis_footer_scroll_show');
	},1000);
	var comiis_scroll_right_times;
	var comiis_scrollTop_box = new Array();
	var comiis_head_height = 0, comiis_istopnum = 0;
	if($(".comiis_scrollTop_box").length > 0){
		var comiis_scrollTop_box_num = new Array();
		var comiis_scrollTop_box_height = new Array();
		$('.comiis_scrollTop_box').each(function(index, comiis) {
			comiis_scrollTop_box[index] = $(comiis);
			comiis_scrollTop_box_num[index] = comiis_scrollTop_box[index].offset().top;
			comiis_scrollTop_box_height[index] = comiis_scrollTop_box[index].height();
		});
		if(!$('#comiis_head').hasClass('comiis_head_hidden')){
			comiis_head_height = $('#comiis_head').height();
		}
	}
	var comiis_istopnums2 = 0, comiis_out_scrollTop = 0, comiis_scroll_right_out_times;
	$(window).scroll(function() {
		var comiis_scrollTop_num = $(window).scrollTop();
		if(comiis_scrollTop_box.length > 0){
			for (var i = 0; i < comiis_scrollTop_box_num.length; i++) {
				if(comiis_scrollTop_num + comiis_head_height > comiis_scrollTop_box_num[i]){
					var comiis_istopnum = ($('#comiis_head').hasClass('comiis_head_hidden') ? 0 : comiis_head_height)
					if(comiis_scrollTop_box_num[i + 1]){
						if(comiis_scrollTop_num + comiis_head_height + comiis_scrollTop_box_height[i] > comiis_scrollTop_box_num[i + 1]){
							comiis_scrollTop_box[i].removeClass('comiis_scrollTop_boxs');
						}else{
							
							comiis_scrollTop_box[i].addClass('comiis_scrollTop_boxs').css('top', comiis_istopnum +'px');
						}
					}else{
						comiis_scrollTop_box[i].addClass('comiis_scrollTop_boxs').css('top',comiis_istopnum +'px');
					}
				}else{
					comiis_scrollTop_box[i].removeClass('comiis_scrollTop_boxs');
				}
			}
		}
		if($('.comiis_gobtn_tbox_on').length > 0){
			var comiis_istopnums1 = ($('#comiis_head').hasClass('comiis_head_hidden') ? 0 : $('#comiis_head').height());
			if(comiis_istopnums2 != comiis_istopnums1){
				comiis_istopnums2 = comiis_istopnums1;
				$('.comiis_gobtn_tbox').css({'transform':'translateY('+comiis_istopnums2+'px)'})
			}
		}
		clearTimeout(comiis_scroll_right_times);
		clearTimeout(comiis_scroll_right_out_times);
		if($('.comiis_scrolltops').length > 0) {
			if(comiis_scrollTop_num > 150){
				$('.comiis_scrolltops').css('display','block');
			}else{
				$('.comiis_scrolltops').css('display','none');
			}
		}
		if(comiis_rlmenu == 1){
			if(comiis_out_scrollTop < comiis_scrollTop_num){
				$('.comiis_footer_scroll').removeClass('comiis_footer_scroll_show');
				comiis_scroll_right_times = setTimeout(function(){
					$('.comiis_footer_scroll').addClass('comiis_footer_scroll_show');
				}, 5000);
			}else{
				comiis_scroll_right_times = setTimeout(function(){
					$('.comiis_footer_scroll').addClass('comiis_footer_scroll_show');
				}, 100);
			}
			comiis_out_scrollTop = comiis_scrollTop_num;
		}
		if(comiis_nvscroll){
			if(comiis_scrollTop_num > 150 && (comiis_scrollTop_num - Comiis_Touch.TouchscrollTop) > 50){
				$('#comiis_head').addClass("comiis_head_hidden");
			}else if((Comiis_Touch.TouchscrollTop - comiis_scrollTop_num) > 50 || comiis_scrollTop_num < 150){
				$('#comiis_head').removeClass('comiis_head_hidden');
			}
		}
	});
var cat1 = Comiis_Touch.init('html', {
	TouchMove : function(){
		if(!$('.comiis_body').hasClass('comiis_showleftnv')){
			if(Comiis_Touch.TouchDirection == 'left'){
				Comiis_Touch_endtime = new Date().getTime();
				if(Comiis_Touch.TouchMoves > 50){
					Comiis_Touch.Touchon = 3;
					Comiis_Touch_openleftnav = 1;
				}else{
					Comiis_Touch_openleftnav = 0;
				}
			}
		}else if(Comiis_Touch.TouchDirection == 'right' && $('.comiis_body').hasClass('comiis_showleftnv')){
			Comiis_Touch_endtime = new Date().getTime();
			if(Comiis_Touch.TouchMoves > 50){
				Comiis_Touch.Touchon = 4;
				Comiis_Touch_openleftnav = 1;
			}else{
				Comiis_Touch_openleftnav = 0;
			}
		}
	},
	TouchEnd : function(){
		Comiis_Touch.Touchon = 0;
		if(!$('.comiis_body').hasClass('comiis_showleftnv')){
			if(Comiis_Touch.TouchDirection == 'left'){
				Comiis_Touch_endtime = new Date().getTime();
				if(Comiis_Touch_openleftnav == 1 && (Comiis_Touch_endtime - Comiis_Touch.Touchstime) < 500){
					Comiis_Touch_openleftnav = 0;
					comiis_leftnv();
				}
				Comiis_Touch_openleftnav = 0;
			}		
		}else if(Comiis_Touch.TouchDirection == 'right' && $('.comiis_body').hasClass('comiis_showleftnv')){
			Comiis_Touch_endtime = new Date().getTime();
			if(Comiis_Touch_openleftnav == 1 && (Comiis_Touch_endtime - Comiis_Touch.Touchstime) < 500){
				Comiis_Touch_openleftnav = 0;
				comiis_leftnv();
			}
			Comiis_Touch_openleftnav = 0;
		}
	}
});
$(document).on('click', '.comiis_dateshow:text,.comiis_dateshow_nt:text', function() {
	var obj = $(this);
	var istime = $(this).hasClass("comiis_dateshow");
	obj.blur();
	var comiis_date = obj.val() ? comiis_parsedate(obj.val()) : new Date();
	var comiis_y = comiis_date.getFullYear();
	var comiis_m = comiis_date.getMonth() + 1;
	var comiis_d = comiis_date.getDate();
	var comiis_h = comiis_date.getHours();
	var comiis_i = comiis_date.getMinutes();
	var id = obj.attr('id');
	var title = obj.parent().find('span').first().text().replace(/\*|\:/ig, '');
	var datehtml = '<div class="comiis_tip comiis_tip_form bg_f cl" id="' + id + '_date">' + 
	'<div class="tip_tit bg_e f_b b_b">' + (title ? title : '日期'+(istime ? '时间' : '')+'设置') + '</div>' + 
	'<div class="comiis_date_style f_c cl">' + 
	'<div class="comiis_date_ymd cl">' + 
	'<div class="comiis_login_select comiis_date comiis_date_year bg_f b_ok">' + 
	'<span class="inner"><span class="comiis_question f_c comiis_date_years_name"></span></span>' + 
	'<select nemu="comiis_date_years" class="comiis_date_years">';
	for(var k = 2020; k >= 1949; k--) {
		datehtml += '<option value="' + k + '"' + (k == comiis_y ? 'selected="selected"' : '') + '>' + k + '年</option>';
	}
	datehtml += '</select>' + 
	'</div>' + 
	'<div class="comiis_login_select comiis_date comiis_date_month bg_f b_ok">' + 
	'<span class="inner"><span class="comiis_question f_c comiis_date_months_name"></span></span>' + 
	'<select nemu="comiis_date_months" class="comiis_date_months">';
	for(var k = 1; k <= 12; k++) {
		datehtml += '<option value="' + ( k < 10 ? '0' : '') + k + '"' + (k == comiis_m ? 'selected="selected"' : '') + '>' + ( k < 10 ? '0' : '') + k + '月</option>';
	}
	datehtml += '</select>' + 
	'</div>' + 
	'<div class="comiis_login_select comiis_date comiis_date_day bg_f b_ok">' + 
	'<span class="inner">' + 
	'<span class="comiis_question f_c comiis_date_days_name"></span>' + 
	'</span>' + 
	'<select nemu="comiis_date_days" class="comiis_date_days"></select>' + 
	'</div>' + 
	'</div>';
	if(istime){
		datehtml += '<div class="comiis_date_hm cl">' + 
		'<div class="comiis_date comiis_date_txt">时间：</div>' + 
		'<div class="comiis_login_select comiis_date comiis_date_h bg_f b_ok">' + 
		'<span class="inner"><span class="comiis_question f_c comiis_date_hs_name"></span></span>' + 
		'<select nemu="comiis_date_hs" class="comiis_date_hs">';
		for(var k = 0; k <= 23; k++) {
			datehtml += '<option value="' + ( k < 10 ? '0' : '') + k + '"' + (k == comiis_h ? 'selected="selected"' : '') + '>' + ( k < 10 ? '0' : '') + k + '时</option>';
		}
		datehtml += '</select>' + 
		'</div>' + 
		'<div class="comiis_login_select comiis_date comiis_date_m bg_f b_ok">' + 
		'<span class="inner"><span class="comiis_question f_c comiis_date_ms_name"></span></span>' + 
		'<select nemu="comiis_date_ms" class="comiis_date_ms">';
		for(var k = 0; k <= 59; k++) {
			datehtml += '<option value="' + ( k < 10 ? '0' : '') + k + '"' + (k == comiis_i ? 'selected="selected"' : '') + '>' + ( k < 10 ? '0' : '') + k + '分</option>';
		}
		datehtml += '</select>' + 
		'</div>' + 
		'</div>'; 
	}
    if(comiis_post_btnwz == 1){
        datehtml += '</div>' + 
        '<dd class="b_t cl">' + 
        '<a href="javascript:;" onclick="comiis_closedate()" class="tip_btn bg_f f_b">取消</a>' + 
        '<a href="javascript:;" onclick="comiis_setdate(\'' + id + '\', \'' + istime + '\');" class="tip_btn bg_f f_0"><span class="tip_lx">确定</span></a>' + 
        '</dd>' + 
        '</div>';
    }else{
        datehtml += '</div>' + 
        '<dd class="b_t cl">' + 
        '<a href="javascript:;" onclick="comiis_setdate(\'' + id + '\', \'' + istime + '\');" class="tip_btn bg_f f_0">确定</a>' + 
        '<a href="javascript:;" onclick="comiis_closedate()" class="tip_btn bg_f f_b"><span class="tip_lx">取消</span></a>' + 
        '</dd>' + 
        '</div>';
    }
	popup.open(datehtml);
	setTimeout(function(){
		comiis_getday(id, comiis_y, comiis_m, comiis_d, istime);
		$('.dialogbox #' + id + '_date .comiis_date_style select').on('change', function(){
			var obj = $(this);
			$('.' + obj.attr('nemu') + '_name').text(obj.find('option:selected').text());
			if(obj.attr('nemu') == 'comiis_date_years' || obj.attr('nemu') == 'comiis_date_months'){
				comiis_getday(id, $('.dialogbox #' + id + '_date .comiis_date_years').find('option:selected').val(), $('.dialogbox #' + id + '_date .comiis_date_months').find('option:selected').val(), 0, istime);
			}
		});
	}, 16);
});
});
function ajaxget(url, showid, waitid, loading, display, recall) {
	var url = url + '&inajax=1&ajaxtarget=' + showid;
	$.ajax({
		type : 'GET',
		url : url,
		dataType : 'xml',
	}).success(function(s) {
		$('#'+showid).html(s.lastChild.firstChild.nodeValue);
		$("[ajaxtarget]").off('click').on('click', function(e) {
			var id = $(this);
			ajaxget(id.attr('href'), id.attr('ajaxtarget'));
			return false;
		});
	});
	return false;
}
var comiis_displayorder_height = 0;
function comiis_displayorder_sh(a){
	if(a == 1){
		$('.comiis_displayorder_key').addClass("comiis_displayorder_hidden");
		comiis_displayorder_height = $('#comiis_displayorder').css('height');
		$('#comiis_displayorder').css('height','auto');
	}else{
		$('.comiis_displayorder_key').removeClass('comiis_displayorder_hidden');
		$('#comiis_displayorder').height(comiis_displayorder_height);
	}
}
function comiis_flsx_sh(){
	if($(".comiis_flbox").is(":hidden")){
		$('.comiis_flsx_key').removeClass('bg_f').addClass("bg_e");
		$('.comiis_flsxico').html('&#xe621;');
		$(".comiis_flbox").show();
	}else{
		$('.comiis_flsx_key').removeClass('bg_e').addClass("bg_f");
		$('.comiis_flsxico').html('&#xe620;');
		$(".comiis_flbox").hide();
	}
}
function comiis_prevent_post(id, b){
	if(b == 1){
		$(id).attr("disabled", true);
	}else{
		setTimeout(function(){
			$(id).attr("disabled", false);
		}, 500);
	}
}
var JSLOADED = [];
!function(t,e){"function"==typeof define&&define.amd?define("ev-emitter/ev-emitter",e):"object"==typeof module&&module.exports?module.exports=e():t.EvEmitter=e()}(this,function(){function t(){}var e=t.prototype;return e.on=function(t,e){if(t&&e){var i=this._events=this._events||{},n=i[t]=i[t]||[];return-1==n.indexOf(e)&&n.push(e),this}},e.once=function(t,e){if(t&&e){this.on(t,e);var i=this._onceEvents=this._onceEvents||{},n=i[t]=i[t]||[];return n[e]=!0,this}},e.off=function(t,e){var i=this._events&&this._events[t];if(i&&i.length){var n=i.indexOf(e);return-1!=n&&i.splice(n,1),this}},e.emitEvent=function(t,e){var i=this._events&&this._events[t];if(i&&i.length){var n=0,o=i[n];e=e||[];for(var r=this._onceEvents&&this._onceEvents[t];o;){var s=r&&r[o];s&&(this.off(t,o),delete r[o]),o.apply(this,e),n+=s?0:1,o=i[n]}return this}},t}),function(t,e){"use strict";"function"==typeof define&&define.amd?define(["ev-emitter/ev-emitter"],function(i){return e(t,i)}):"object"==typeof module&&module.exports?module.exports=e(t,require("ev-emitter")):t.imagesLoaded=e(t,t.EvEmitter)}(window,function(t,e){function i(t,e){for(var i in e)t[i]=e[i];return t}function n(t){var e=[];if(Array.isArray(t))e=t;else if("number"==typeof t.length)for(var i=0;i<t.length;i++)e.push(t[i]);else e.push(t);return e}function o(t,e,r){return this instanceof o?("string"==typeof t&&(t=document.querySelectorAll(t)),this.elements=n(t),this.options=i({},this.options),"function"==typeof e?r=e:i(this.options,e),r&&this.on("always",r),this.getImages(),h&&(this.jqDeferred=new h.Deferred),void setTimeout(function(){this.check()}.bind(this))):new o(t,e,r)}function r(t){this.img=t}function s(t,e){this.url=t,this.element=e,this.img=new Image}var h=t.jQuery,a=t.console;o.prototype=Object.create(e.prototype),o.prototype.options={},o.prototype.getImages=function(){this.images=[],this.elements.forEach(this.addElementImages,this)},o.prototype.addElementImages=function(t){"IMG"==t.nodeName&&this.addImage(t),this.options.background===!0&&this.addElementBackgroundImages(t);var e=t.nodeType;if(e&&d[e]){for(var i=t.querySelectorAll("img"),n=0;n<i.length;n++){var o=i[n];this.addImage(o)}if("string"==typeof this.options.background){var r=t.querySelectorAll(this.options.background);for(n=0;n<r.length;n++){var s=r[n];this.addElementBackgroundImages(s)}}}};var d={1:!0,9:!0,11:!0};return o.prototype.addElementBackgroundImages=function(t){var e=getComputedStyle(t);if(e)for(var i=/url\((['"])?(.*?)\1\)/gi,n=i.exec(e.backgroundImage);null!==n;){var o=n&&n[2];o&&this.addBackground(o,t),n=i.exec(e.backgroundImage)}},o.prototype.addImage=function(t){var e=new r(t);this.images.push(e)},o.prototype.addBackground=function(t,e){var i=new s(t,e);this.images.push(i)},o.prototype.check=function(){function t(t,i,n){setTimeout(function(){e.progress(t,i,n)})}var e=this;return this.progressedCount=0,this.hasAnyBroken=!1,this.images.length?void this.images.forEach(function(e){e.once("progress",t),e.check()}):void this.complete()},o.prototype.progress=function(t,e,i){this.progressedCount++,this.hasAnyBroken=this.hasAnyBroken||!t.isLoaded,this.emitEvent("progress",[this,t,e]),this.jqDeferred&&this.jqDeferred.notify&&this.jqDeferred.notify(this,t),this.progressedCount==this.images.length&&this.complete(),this.options.debug&&a&&a.log("progress: "+i,t,e)},o.prototype.complete=function(){var t=this.hasAnyBroken?"fail":"done";if(this.isComplete=!0,this.emitEvent(t,[this]),this.emitEvent("always",[this]),this.jqDeferred){var e=this.hasAnyBroken?"reject":"resolve";this.jqDeferred[e](this)}},r.prototype=Object.create(e.prototype),r.prototype.check=function(){var t=this.getIsImageComplete();return t?void this.confirm(0!==this.img.naturalWidth,"naturalWidth"):(this.proxyImage=new Image,this.proxyImage.addEventListener("load",this),this.proxyImage.addEventListener("error",this),this.img.addEventListener("load",this),this.img.addEventListener("error",this),void(this.proxyImage.src=this.img.src))},r.prototype.getIsImageComplete=function(){return this.img.complete&&void 0!==this.img.naturalWidth},r.prototype.confirm=function(t,e){this.isLoaded=t,this.emitEvent("progress",[this,this.img,e])},r.prototype.handleEvent=function(t){var e="on"+t.type;this[e]&&this[e](t)},r.prototype.onload=function(){this.confirm(!0,"onload"),this.unbindEvents()},r.prototype.onerror=function(){this.confirm(!1,"onerror"),this.unbindEvents()},r.prototype.unbindEvents=function(){this.proxyImage.removeEventListener("load",this),this.proxyImage.removeEventListener("error",this),this.img.removeEventListener("load",this),this.img.removeEventListener("error",this)},s.prototype=Object.create(r.prototype),s.prototype.check=function(){this.img.addEventListener("load",this),this.img.addEventListener("error",this),this.img.src=this.url;var t=this.getIsImageComplete();t&&(this.confirm(0!==this.img.naturalWidth,"naturalWidth"),this.unbindEvents())},s.prototype.unbindEvents=function(){this.img.removeEventListener("load",this),this.img.removeEventListener("error",this)},s.prototype.confirm=function(t,e){this.isLoaded=t,this.emitEvent("progress",[this,this.element,e])},o.makeJQueryPlugin=function(e){e=e||t.jQuery,e&&(h=e,h.fn.imagesLoaded=function(t,e){var i=new o(this,t,e);return i.jqDeferred.promise(h(this))})},o.makeJQueryPlugin(),o});
(function(a,b,c){var d=b.event,e;d.special.smartresize={setup:function(){b(this).bind("resize",d.special.smartresize.handler)},teardown:function(){b(this).unbind("resize",d.special.smartresize.handler)},handler:function(a,b){var c=this,d=arguments;a.type="smartresize",e&&clearTimeout(e),e=setTimeout(function(){jQuery.event.handle.apply(c,d)},b==="execAsap"?0:100)}},b.fn.smartresize=function(a){return a?this.bind("smartresize",a):this.trigger("smartresize",["execAsap"])},b.Mason=function(a,c){this.element=b(c),this._create(a),this._init()},b.Mason.settings={isResizable:!0,isAnimated:!1,animationOptions:{queue:!1,duration:500},gutterWidth:0,isRTL:!1,isFitWidth:!1,containerStyle:{position:"relative"}},b.Mason.prototype={_filterFindBricks:function(a){var b=this.options.itemSelector;return b?a.filter(b).add(a.find(b)):a},_getBricks:function(a){var b=this._filterFindBricks(a).css({position:"absolute"}).addClass("masonry-brick");return b},_create:function(c){this.options=b.extend(!0,{},b.Mason.settings,c),this.styleQueue=[];var d=this.element[0].style;this.originalStyle={height:d.height||""};var e=this.options.containerStyle;for(var f in e)this.originalStyle[f]=d[f]||"";this.element.css(e),this.horizontalDirection=this.options.isRTL?"right":"left",this.offset={x:parseInt(this.element.css("padding-"+this.horizontalDirection),10),y:parseInt(this.element.css("padding-top"),10)},this.isFluid=this.options.columnWidth&&typeof this.options.columnWidth=="function";var g=this;setTimeout(function(){g.element.addClass("masonry")},0),this.options.isResizable&&b(a).bind("smartresize.masonry",function(){g.resize()}),this.reloadItems()},_init:function(a){this._getColumns(),this._reLayout(a)},option:function(a,c){b.isPlainObject(a)&&(this.options=b.extend(!0,this.options,a))},layout:function(a,b){for(var c=0,d=a.length;c<d;c++)this._placeBrick(a[c]);var e={};e.height=Math.max.apply(Math,this.colYs);if(this.options.isFitWidth){var f=0,c=this.cols;while(--c){if(this.colYs[c]!==0)break;f++}e.width=(this.cols-f)*this.columnWidth-this.options.gutterWidth}this.styleQueue.push({$el:this.element,style:e});var g=this.isLaidOut?this.options.isAnimated?"animate":"css":"css",h=this.options.animationOptions,i;for(c=0,d=this.styleQueue.length;c<d;c++)i=this.styleQueue[c],i.$el[g](i.style,h);this.styleQueue=[],b&&b.call(a),this.isLaidOut=!0},_getColumns:function(){var a=this.options.isFitWidth?this.element.parent():this.element,b=a.width();this.columnWidth=this.isFluid?this.options.columnWidth(b):this.options.columnWidth||this.$bricks.outerWidth(!0)||b,this.columnWidth+=this.options.gutterWidth,this.cols=Math.floor((b+this.options.gutterWidth)/this.columnWidth),this.cols=Math.max(this.cols,1)},_placeBrick:function(a){var c=b(a),d,e,f,g,h;d=Math.ceil(c.outerWidth(!0)/(this.columnWidth+this.options.gutterWidth)),d=Math.min(d,this.cols);if(d===1)f=this.colYs;else{e=this.cols+1-d,f=[];for(h=0;h<e;h++)g=this.colYs.slice(h,h+d),f[h]=Math.max.apply(Math,g)}var i=Math.min.apply(Math,f),j=0;for(var k=0,l=f.length;k<l;k++)if(f[k]===i){j=k;break}var m={top:i+this.offset.y};m[this.horizontalDirection]=this.columnWidth*j+this.offset.x,this.styleQueue.push({$el:c,style:m});var n=i+c.outerHeight(!0),o=this.cols+1-l;for(k=0;k<o;k++)this.colYs[j+k]=n},resize:function(){var a=this.cols;this._getColumns(),(this.isFluid||this.cols!==a)&&this._reLayout()},_reLayout:function(a){var b=this.cols;this.colYs=[];while(b--)this.colYs.push(0);this.layout(this.$bricks,a)},reloadItems:function(){this.$bricks=this._getBricks(this.element.children())},reload:function(a){this.reloadItems(),this._init(a)},appended:function(a,b,c){if(b){this._filterFindBricks(a).css({top:this.element.height()});var d=this;setTimeout(function(){d._appended(a,c)},1)}else this._appended(a,c)},_appended:function(a,b){var c=this._getBricks(a);this.$bricks=this.$bricks.add(c),this.layout(c,b)},remove:function(a){this.$bricks=this.$bricks.not(a),a.remove()},destroy:function(){this.$bricks.removeClass("masonry-brick").each(function(){this.style.position="",this.style.top="",this.style.left=""});var c=this.element[0].style;for(var d in this.originalStyle)c[d]=this.originalStyle[d];this.element.unbind(".masonry").removeClass("masonry").removeData("masonry"),b(a).unbind(".masonry")}},b.fn.imagesLoaded=function(a){function i(a){a.target.src!==f&&b.inArray(this,g)===-1&&(g.push(this),--e<=0&&(setTimeout(h),d.unbind(".imagesLoaded",i)))}function h(){a.call(c,d)}var c=this,d=c.find("img").add(c.filter("img")),e=d.length,f="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==",g=[];e||h(),d.bind("load.imagesLoaded error.imagesLoaded",i).each(function(){var a=this.src;this.src=f,this.src=a});return c};var f=function(a){this.console&&console.error(a)};b.fn.masonry=function(a){if(typeof a=="string"){var c=Array.prototype.slice.call(arguments,1);this.each(function(){var d=b.data(this,"masonry");if(!d)f("cannot call methods on masonry prior to initialization; attempted to call method '"+a+"'");else{if(!b.isFunction(d[a])||a.charAt(0)==="_"){f("no such method '"+a+"' for masonry instance");return}d[a].apply(d,c)}})}else this.each(function(){var c=b.data(this,"masonry");c?(c.option(a||{}),c._init()):b.data(this,"masonry",new b.Mason(a,this))});return this}})(window,jQuery);
