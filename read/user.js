var writeStr = "";

var $alert = $("#alert");
var timer = null;
//模拟请求文本数据
$.get("./js/data2.txt", function (data) {
    initPage(data);
})
function initPage(writeStr) {
    if (!writeStr) {
        return;
    }

    var $wrap = $("#magazine");
    var $page = $("#pages");
    var page_width = $page.width(); //窗口的宽度
    var page_height = $page.height(); //窗口的高度

    var $content = $("#contentText");

    $content.html(writeStr);
    var len = writeStr.length; //总长度
    var total_height = $content.height(); //总高度
    var pageStrNum; //每页大概有多少个字符
    if (total_height > page_height) {
        pageStrNum = (page_height / total_height) * len; //每页大概有多少个字符
        var obj = overflowhiddenTow($content, writeStr, page_height);
        $page.append('<div>' + obj.curr + '</div>');
        while (obj.next && obj.next.length > 0) {
            obj = overflowhiddenTow($content, obj.next, page_height);
            $page.append('<div>' + obj.curr + '</div>');
        }
    } else {
        return;
    }

    //文字切割算法
    function overflowhiddenTow($texts, str, at) {
        var throat = pageStrNum;
        var tempstr = str.substring(0, throat);
        var len = str.length;
        $texts.html(tempstr);
        //取的字节较少,应该增加
        while ($texts.height() < at && throat < len) {
            throat = throat + 2;
            tempstr = str.substring(0, throat);
            $texts.html(tempstr);
        }
        //取的字节较多,应该减少
        while ($texts.height() > at && throat > 0) {
            throat = throat - 2;
            tempstr = str.substring(0, throat);
            $texts.html(tempstr);
        }

        return {
            curr: str.substring(0, throat),
            next: str.substring(throat)
        }

    }

    $page.turn({
        width: page_width,
        height: page_height,
        elevation: 50,
        display: 'single',
        gradients: true,
        autoCenter: true,
        when: {
            start: function () {},
            turning: function (e, page, view) {},
            turned: function (e, page, view) {}
        }
    });

    $wrap.click(function (e) {
        var e = e || window.event;
        //获得当前点击位置距离浏览器顶部的距离
        var top = e.pageY;
        //获得当前点击位置距离浏览器左侧的距离
        var left = e.pageX;
        let windowWidth = $("#magazine").width();
        let windowHeight = $("#magazine").height();
        console.log("浏览器宽，高：%s %s", windowWidth, windowHeight)
        console.log("点击区域,距离左,上：%s %s", left, top)
        let threePointsWidth_left = windowWidth / 3;
        //let threePointsHeight_left = windowHeight / 3;
        let threePointsWidth_right = windowWidth / 3 * 2;
        //let threePointsHeight_right = windowHeight / 3*2;
        var pageCount = $page.turn("pages"); //总页数
        var currentPage = $page.turn("page"); //当前页
        if (left <= threePointsWidth_left && left >= 0) {
            console.log("左边区域");
            previousPage(currentPage);

        } else if (left >= threePointsWidth_right && left <= windowWidth) {
            console.log("右边区域");
            nextPage(currentPage, pageCount);
        } else {
            console.log("中间区域");
        }

    })

    function previousPage(currentPage) { //上一页
        if (currentPage > 1) {
            $page.turn('page', currentPage - 1);
        } else {
            console.log("已经是第一页")
            showAlert('已经是第一页');
        }
    }
    function nextPage(currentPage, pageCount) { //下一页
        if (currentPage < pageCount) {
            $page.turn('page', currentPage + 1);
        } else {
            console.log("最后一页");
            showAlert('已经是最后一页');
        }
    }

    function showAlert(msg) {
        clearTimeout(timer);
        $alert.text(msg);
        $alert.fadeIn();
        timer = setTimeout(function () {
            $alert.fadeOut();
        }, 1000)
    }

}
