// Инициализация компонентов

$(document).ready(function () {
    /*
    Точка подключения всех скриптов.
    */
    /*
    Инициализация сайдбара и сворачиваемых меню, ajax-загрузчика, плавающих окон.
     */
    twentysixwordsday.initDropdown();
    twentysixwordsday.initSidebar();
    twentysixwordsday.initTray();
    twentysixwordsday.initFloatingAjax();
    twentysixwordsday.initFloatingWindows();

    /*
    Waves Effects
    */
    Waves.attach('.waves-btn', ['waves-button']);
    Waves.init();
});