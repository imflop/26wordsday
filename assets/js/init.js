// Инициализация компонентов

$(document).ready(function () {
    /*
    Точка подключения всех скриптов
    */
    /*
    Инициализация сайдбара и сворачиваемых меню
     */
    twentysixwordsday.initSidebar();

    /*
    Waves Effects
    */
    Waves.attach('.waves-btn', ['waves-button']);
    Waves.init();
});