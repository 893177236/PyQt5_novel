
(function ($) {
    new QWebChannel(qt.webChannelTransport,
        function (channel) {
            window.Bridge = channel.objects.Bridge;
            // 这里绑定窗口的标题变化信号（这个信号是由QWidget内部的）
            /*Bridge.windowTitleChanged.connect(function(title) {
                    alert("标题被修改为：" + title);
            });
            */
            //let filepath = Bridge.readFilePath;
            //init_main(filepath);
            // let readStatus = Bridge.readStatus;
            // let readText = Bridge.readText;
            // let readPage = parseInt(Bridge.readPage);
            // let readConfig = Bridge.readConfig;
            // let extraCss = `<style type="text/css">${readConfig}</style>`;
            // $("head").append($(extraCss));
            // init_main(readText,readPage,readStatus);

            // let borderImagePath = Bridge.getBorderImagePath; //背景图片地址

            // page_text.one = Bridge.getOnePageText;
            // page_text.selic= Bridge. getSurplusText;
            page_text.info = Bridge.getArrayBookInfo;
            // page_text["one"]  = Bridge.getOnePageText;
            // page_text["selic"] =  Bridge. getSurplusText;
            init__();
        }
    )
}(jQuery));
