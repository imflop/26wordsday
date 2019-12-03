// Базисные функции для подгрузки контента

function ajaxGetRequest(url, container, dataType='JSON', main=null, data={}, icon=null, text='', errorIcon=null,
                        errorText=null, callback=null) {
    // Базовая функция для подгрузки контента GET-запросом по ajax

    const containerObj = $(container); // Контейнер, в который будет осуществляться подгрузка контента

    // Вывод сообщений на экран во время подгрузки контента
    const messenger = new Messages(containerObj);
    const preloader = new messenger.fullScreen();

    // Параметры AJAX
    const ajaxParameters = {
        url: url,
        type: 'GET',
        data: data,
        dataType: dataType,
    };

    // По завершению AJAX - preloader-объект осуществляет выполнение callback-функций
    preloader.preloaderMessage($.ajax(ajaxParameters), function (response, message) {
        // message - объект сообщения, выводимого на экран (preloader object)
        // Можно использовать для манипуляций с сообщениями

        if(dataType === 'JSON'){
            containerObj.empty().append(response.template);
        }
        else if(dataType === 'HTML'){
            containerObj.empty().append(response)
        }

        // Вызов callback - функций
        if(main) {
            main(response);
        }
        if(callback) {
            callback();
        }

    }, icon, text, errorIcon, errorText)
}

function ajaxPostRequest(url, container, data={}, dataType='JSON', main=null, icon=null, text='', errorIcon=null,
                        errorText=null) {
    // Базовая функция для отправки POST-запросов по ajax

    let containerObj = $(container);

    let messenger = new Messages(containerObj);
    let preloader = new messenger.fullScreen();

    // Параметры AJAX
    const ajaxParameters = {
        url: url,
        type: 'POST',
        data: data,
        dataType: dataType,
    };

    preloader.preloaderMessage($.ajax(ajaxParameters), function (response, message) {
        // message - объект сообщения, выводимого на экран (preloader object)
        // Можно использовать для манипуляций с сообщениями

        // Вызов callback - функций
        if (main) {
            main(response);
        }

    }, icon, text, errorIcon, errorText)
}