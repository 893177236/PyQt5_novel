
(function ($) {
    new QWebChannel(qt.webChannelTransport,
        function (channel) {
            window.Bridge = channel.objects.Bridge;
            // ����󶨴��ڵı���仯�źţ�����ź�����QWidget�ڲ��ģ�
            /*Bridge.windowTitleChanged.connect(function(title) {
                    alert("���ⱻ�޸�Ϊ��" + title);
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

            // let borderImagePath = Bridge.getBorderImagePath; //����ͼƬ��ַ

            // page_text.one = Bridge.getOnePageText;
            // page_text.selic= Bridge. getSurplusText;
            page_text.info = Bridge.getArrayBookInfo;
            // page_text["one"]  = Bridge.getOnePageText;
            // page_text["selic"] =  Bridge. getSurplusText;
            init__();
        }
    )
}(jQuery));
