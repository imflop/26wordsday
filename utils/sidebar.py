import abc
from collections import Collection, OrderedDict
from typing import Type

from django.http import HttpRequest
from django.urls import resolve, reverse_lazy


class MenuElement:
    """
    Абстрактный класс кнопки
    """
    @staticmethod
    def prepare_html_params(html_params: Collection) -> str:
        """
        Метод для подготовки html-атрибутов кнопки
        :param html_params: Collection, атрибуты кнопки
        :return: str
        """
        return ' '.join(html_params)

    @staticmethod
    def prepare_css_classes(css_classes: Collection) -> str:
        """
        Метод для подготовки html-атрибутов кнопки
        :param css_classes: Collection, классы кнопки
        :return: str
        """
        return ' '.join(css_classes)


class SidebarMenuButtonTypes:
    """
    Класс-коллекция типов кнопок
    """
    SINGLE = 'single'
    DROPDOWN = 'dropdown'


class SidebarTypes:
    """
    Класс-коллекция типов сайдбара
    """
    APP_MAIN = 'app_main_sidebar'


class TemplateVarMapper:
    """
    Класс с методами маппа значений переменных на значения, пригодные для использования в шаблонах
    """
    @staticmethod
    def boolean_to_str_js_compatible(value: bool) -> str:
        """
        Мап питновского bool на строки для js
        :return: str
        """
        return 'true' if value else 'false'


class AbstractMenuButton(MenuElement):
    """
    Общий класс для всех кнопок элементов меню
    """
    button_type = None

    def __init__(self,
                 key: str,
                 title: str,
                 html_params: Collection,
                 css_classes: Collection,
                 icon: str = None):

        self.key = key
        self.title = title
        self.icon = icon
        self.html_params = self.prepare_html_params(html_params)
        self.css_classes = self.prepare_css_classes(css_classes)

    def is_single(self) -> bool:
        """
        Метод для проверки типа кнопки - 'Одиночная'
        :return: bool
        """
        return self.button_type == SidebarMenuButtonTypes.SINGLE

    def is_dropdown(self) -> bool:
        """
        Метод для проверки типа кнопки - 'Выпадающая'
        :return: bool
        """
        return self.button_type == SidebarMenuButtonTypes.DROPDOWN

    def disable_button(self) -> None:
        """
        Метод для блокировки кнопки
        :return: None
        """
        self.css_classes += ''

    def set_as_active(self) -> None:
        """
        Метод для активации кнопки
        :return: None
        """
        self.css_classes += 'active'

    def activate_by_url(self, url: str) -> bool:
        """
        Метод для активации кнопки
        :param url: str, url для проверки
        :return: bool
        """
        url_check_result = self.is_single() and getattr(self, 'active_url', None) == url
        if url_check_result:
            self.set_as_active()
        return url_check_result

    def get_url(self) -> str:
        """
        Метод для получения 'url' для кнопки
        :return: str
        """
        return getattr(self, 'active_url', '#')

    @abc.abstractproperty
    def css_extra_classes(self) -> str:
        """
        Метод для установки css-экстра-классов для кнопки
        :return: str
        """
        pass


class SidebarMenuSingleButton(AbstractMenuButton):
    """
    Класс для одиночной кнопки
    """
    button_type = SidebarMenuButtonTypes.SINGLE

    def __init__(self, active_url: str, parent: str = None, *args, **kwargs):
        self.active_url = active_url
        self.parent = parent
        super().__init__(*args, **kwargs)

    def css_extra_classes(self) -> str:
        """
        Метод для установки css-экстра-классов для кнопки
        :return: str
        """
        extra_css = 'sidebar-btn'
        if self.parent is not None:
            extra_css = 'sidebar-sub-btn'
        return extra_css


class SidebarMenuDropdownButton(AbstractMenuButton):
    """
    Класс для кнопки сворачивающегося меню
    """
    button_type = SidebarMenuButtonTypes.DROPDOWN

    def __init__(self,
                 sub_buttons: OrderedDict,
                 toggle_on_icon: str,
                 toggle_off_icon: str,
                 is_open: bool,
                 *args, **kwargs):

        self.sub_buttons = sub_buttons
        self.toggle_on_icon = toggle_on_icon
        self.toggle_off_icon = toggle_off_icon
        self.is_open = is_open
        super().__init__(*args, **kwargs)

    @property
    def is_open_mapped(self) -> str:
        """
        Метод для получения значения атрибута 'is_open', пригодного для использования в шаблонах
        :return: str
        """
        return TemplateVarMapper.boolean_to_str_js_compatible(self.is_open)

    def css_extra_classes(self) -> str:
        """
        Метод для установки css-экстра-классов для кнопки
        :return: str
        """
        return 'sidebar-btn js-sidebar_dropdown_toggle_btn'


class AbstractSidebarMenu:
    """
    Абстрактный класс для меню сайдбара
    """
    def __init__(self, key: str, request: HttpRequest):
        self._key = key
        self._request = request
        self.buttons = self.set_buttons()
        self.is_open = True

        self._current_url = request.get_full_path() if request else None
        self._current_app = resolve(request.path).app_name if request else None

        self.initialize()

    @property
    def is_open_mapped(self) -> str:
        """
        Метод для получения значения атрибута 'is_open', пригодного для использования в шаблонах
        :return: str
        """
        return TemplateVarMapper.boolean_to_str_js_compatible(self.is_open)

    @abc.abstractmethod
    def set_buttons(self) -> OrderedDict:
        """
        Метод для установки кнопок для меню
        :return: sidebar_menu_buttons
        """
        return OrderedDict({})

    def initialize(self) -> None:
        """
        Метод для запуска инициализации меню. Установка кнопкам активного статуса при совпадении url, открытие
        выпадающего меню при наличии активной кнопки в нем
        :return: None
        """
        for button_key, button in self.buttons.items():
            button.activate_by_url(self._current_url)
            for sub_button in button.sub_buttons.values():
                sub_button.parent = button_key
                url_check_result = sub_button.activate_by_url(self._current_url)
                if url_check_result:
                    parent_button = self.buttons[sub_button.parent]
                    parent_button.set_as_active()
                    parent_button.is_open = True

    def build_menu(self) -> Type['AbstractSidebarMenu']:
        """
        Метод для сборки сайдбара
        :return: Type['AbstractSidebarMenu']
        """
        pass

    def __str__(self):
        return self._key


class TwentySixWordsDaySidebarMenu(AbstractSidebarMenu):
    """
    Класс меню для исходного приложения
    """
    def set_buttons(self) -> OrderedDict:
        return OrderedDict({
            'main': SidebarMenuDropdownButton(
                key='home',
                icon='home',
                title='Главная',
                html_params=[],
                css_classes=[],
                is_open=False,
                toggle_on_icon='keyboard_arrow_down',
                toggle_off_icon='keyboard_arrow_up',
                sub_buttons=OrderedDict({
                    'main__words': SidebarMenuSingleButton(
                        key='words',
                        icon='list',
                        title='Слова',
                        html_params=[],
                        css_classes=[],
                        active_url=reverse_lazy('words:words-list'),
                    ),
                    'main__history': SidebarMenuSingleButton(
                        key='history',
                        icon='schedule',
                        title='История',
                        html_params=[],
                        css_classes=[],
                        active_url='',
                    )
                })
            )
        })
