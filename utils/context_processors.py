from utils.sidebar import TwentySixWordsDaySidebarMenu, SidebarTypes


def twentysixwordsday_context_processor(request) -> dict:
    """
    Основной контекстный процессор приложения
    :param request: HttpRequest, данные запроса
    :return: dic
    """
    sidebar = TwentySixWordsDaySidebarMenu(key=SidebarTypes.APP_MAIN, request=request)
    return {SidebarTypes.APP_MAIN: sidebar}
