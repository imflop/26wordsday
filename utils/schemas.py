from django.urls import reverse
from template_schema.components.basics import MaterialIcon, SingleButton, Badge
from template_schema.handler import TemplateSchema
from template_schema_extensions.components.navigation.components import Sidebar, Navbar, ProfileDropdown, \
    ProfileDropdownRow, ProfileDropdownMenuButton, SidebarButtonTitle, SidebarSingleButton, SidebarLogoImage, \
    SidebarLogoTitle, NavbarLogoImage, NavbarLogoTitle, NavbarSingleButton, SingleButtonType


class BaseApplicationSchema(TemplateSchema):
    """
    Базовая схема приложения
    """

    class GenericNavbar(Navbar):
        """
        Класс для реализации навбара приложения
        """

        unique_name = 'application_navbar'
        grouper_map = {'first_group': ['navbar_button_1'], 'second_group': ['navbar_button_2', 'navbar_button_3']}

        def get_elements(self) -> dict:
            return {
                'toggle_button': NavbarSingleButton(
                    key='toggle_button',
                    css_classes=['navbar-toggler'],
                    icon_before_title=MaterialIcon('view_list'),
                    html_params={'data-toggle': 'collapse', 'data-target': '#navbar-collapsed-content'}
                ),
                'navbar_button_1': NavbarSingleButton(
                    key='navbar_button_1',
                    icon_before_title=MaterialIcon('landscape')
                ),
                'navbar_button_2': NavbarSingleButton(
                    key='navbar_button_2',
                    icon_before_title=MaterialIcon('landscape')
                ),
                'navbar_button_3': NavbarSingleButton(
                    key='navbar_button_3',
                    icon_before_title=MaterialIcon('landscape')
                )
            }

        def get_toggle_button(self) -> SingleButtonType:
            return self.elements.get('toggle_button')

    class LandingNavbar(Navbar):
        """
        Класс для реализации навбара landing-страницы
        """

        unique_name = 'landing_navbar'
        logo_image = NavbarLogoImage(html_params={'src': '/assets/img/logo_img.png'})
        logo_title = NavbarLogoTitle('26 Words Day')

        def extend_context_data(self) -> dict:
            pass

    class GenericSidebar(Sidebar):
        """
        Класс для реализации сайдбара приложения
        """

        unique_name = 'application_sidebar'
        grouper_map = {'Слова': ['random_word_set', 'exams'], 'Другое': ['words_sets_history', 'rating']}
        logo_image = SidebarLogoImage(html_params={'src': '/assets/img/logo_img.png'})
        logo_title = SidebarLogoTitle('26 Words Day')

        def get_elements(self) -> dict:
            return {
                'random_word_set': SidebarSingleButton(
                    key='random_word_set_button',
                    icon_before_title=MaterialIcon('landscape'),
                    title=SidebarButtonTitle('Случайная подборка'),
                    html_params={'href': '#'},
                    active_url='#'
                ),
                'exams': SidebarSingleButton(
                    key='exams_button',
                    icon_before_title=MaterialIcon('school'),
                    title=SidebarButtonTitle('Экзамены'),
                    html_params={'href': '#'},
                    active_url='#',
                    css_classes=['disabled-btn']
                ),
                'words_sets_history': SidebarSingleButton(
                    key='words_sets_history_button',
                    icon_before_title=MaterialIcon('history'),
                    title=SidebarButtonTitle('История'),
                    html_params={'href': '#'},
                    active_url='#',
                    css_classes=['disabled-btn']
                ),
                'rating': SidebarSingleButton(
                    key='rating_button',
                    icon_before_title=MaterialIcon('call_made'),
                    title=SidebarButtonTitle('Рейтинг'),
                    html_params={'href': '#'},
                    active_url='#'
                ),
                'toggle_button': SingleButton(
                    key='toggle_button',
                    title=SidebarButtonTitle('Свернуть'),
                    icon_after_title=MaterialIcon('keyboard_arrow_left', css_classes=['hide-on-sidebar-close']),
                    icon_before_title=MaterialIcon('keyboard_arrow_right', css_classes=['hide-on-sidebar-open']),
                    css_classes=['sidebar-toolbar-btn', 'js-sidebar_toggle_btn']
                )
            }

    class ProfileDropdownWithBadge(ProfileDropdown):
        """
        Класс для реализации выпадающего меню профиля
        """

        unique_name = 'profile_dropdown'
        align = 'right'
        grouper_map = {'user_badge': ['user_settings', 'exit']}

        def set_face_badge(self) -> None:
            self.face_badge = Badge(letter='E', rows=[
                ProfileDropdownRow('EVGENY',
                                    css_classes=['info-badge-row-align', 'hide-on-sidebar-close'],
                                    icon=MaterialIcon('keyboard_arrow_down')),
                ProfileDropdownRow('m3adez@gmail.com', css_classes=['info-badge-row-align', 'hide-on-sidebar-close'])
            ])

        def get_inner_badges(self) -> dict:
            return {
                'user_badge': Badge(letter='E', rows=[
                    ProfileDropdownRow('INFO'),
                    ProfileDropdownRow('INFO'),
                    ProfileDropdownRow('INFO'),
                    ProfileDropdownRow('INFO'),
                    ProfileDropdownRow('INFO'),
                    ProfileDropdownRow('INFO')
                ])
            }

        def get_elements(self) -> dict:
            return {
                'user_settings': ProfileDropdownMenuButton(
                    key='user_settings_button',
                    title='Настройки пользователя'
                ),
                'exit': ProfileDropdownMenuButton(
                    key='exit_button',
                    title='Выход',
                    html_params={'href': reverse('logout')}
                )
            }
