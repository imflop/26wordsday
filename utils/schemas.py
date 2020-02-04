from typing import Type

from template_schema.components.basics import MaterialIcon, SingleButton, Badge
from template_schema.handler import TemplateSchema
from template_schema_extensions.components.navigation.components import Sidebar, Navbar, ProfileDropdown


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
                'toggle_button': self.Components.NavbarSingleButton(
                    key='toggle_button',
                    css_classes=['navbar-toggler'],
                    icon_before_title=MaterialIcon('view_list'),
                    html_params={'data-toggle': 'collapse', 'data-target': '#navbar-collapsed-content'}
                ),
                'navbar_button_1': self.Components.NavbarSingleButton(
                    key='navbar_button_1',
                    icon_before_title=MaterialIcon('landscape')
                ),
                'navbar_button_2': self.Components.NavbarSingleButton(
                    key='navbar_button_2',
                    icon_before_title=MaterialIcon('landscape')
                ),
                'navbar_button_3': self.Components.NavbarSingleButton(
                    key='navbar_button_3',
                    icon_before_title=MaterialIcon('landscape')
                )
            }

        def get_toggle_button(self) -> Type[SingleButton]():
            return self.elements.get('toggle_button')

    class GenericSidebar(Sidebar):
        """
        Класс для реализации сайдбара приложения
        """

        unique_name = 'application_sidebar'
        grouper_map = {'Слова': ['random_word_set', 'exams'], 'Другое': ['words_sets_history', 'rating_dropdown']}
        logo_image = Sidebar.Components.LogoImage(html_params={'src': '/assets/img/logo_img.png'})
        logo_title = Sidebar.Components.LogoTitle('26 Words Day')

        def get_elements(self) -> dict:
            return {
                'random_word_set': self.Components.SidebarSingleButton(
                    key='random_word_set_button',
                    icon_before_title=MaterialIcon('landscape'),
                    title=self.Components.SidebarButtonTitle('Случайная подборка'),
                    html_params={'href': '#'},
                    active_url='/words/list/'
                ),
                'exams': self.Components.SidebarSingleButton(
                    key='exams_button',
                    icon_before_title=MaterialIcon('school'),
                    title=self.Components.SidebarButtonTitle('Экзамены'),
                    html_params={'href': '#'},
                    active_url='#',
                    css_classes=['disabled-btn']
                ),
                'words_sets_history': self.Components.SidebarSingleButton(
                    key='words_sets_history_button',
                    icon_before_title=MaterialIcon('history'),
                    title=self.Components.SidebarButtonTitle('История'),
                    html_params={'href': '#'},
                    active_url='#',
                    css_classes=['disabled-btn']
                ),
                'rating_dropdown': self.Components.SidebarDropdownButton(
                    key='rating_dropdown_button',
                    icon_before_title=MaterialIcon('call_made'),
                    title=self.Components.SidebarButtonTitle('Рейтинги'),
                    sub_buttons={
                        'personal_rating': self.Components.SidebarSingleButton(
                            key='personal_rating_button',
                            icon_before_title=MaterialIcon('face'),
                            title=self.Components.SidebarButtonTitle('Персональный рейтинг'),
                            css_classes=['sidebar-sub-btn'],
                            html_params={'href': '#'},
                            active_url='#'
                        ),
                        'world_wide_rating': self.Components.SidebarSingleButton(
                            key='world_wide_rating_button',
                            icon_before_title=MaterialIcon('language'),
                            title=self.Components.SidebarButtonTitle('Мировой рейтинг'),
                            css_classes=['sidebar-sub-btn'],
                            html_params={'href': '#'},
                            active_url='#'
                        )
                    }
                ),
                'toggle_button': SingleButton(
                    key='toggle_button',
                    title=self.Components.SidebarButtonTitle('Свернуть'),
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
                self.Components.Row('EVGENY',
                                    css_classes=['info-badge-row-align', 'hide-on-sidebar-close'],
                                    icon=MaterialIcon('keyboard_arrow_down')),
                self.Components.Row('m3adez@gmail.com', css_classes=['info-badge-row-align', 'hide-on-sidebar-close'])
            ])

        def get_inner_badges(self) -> dict:
            return {
                'user_badge': Badge(letter='E', rows=[
                    self.Components.Row('INFO'),
                    self.Components.Row('INFO'),
                    self.Components.Row('INFO'),
                    self.Components.Row('INFO'),
                    self.Components.Row('INFO'),
                    self.Components.Row('INFO')
                ])
            }

        def get_elements(self) -> dict:
            return {
                'user_settings': self.Components.MenuButton(
                    key='user_settings_button',
                    title='Настройки пользователя'
                ),
                'exit': self.Components.MenuButton(
                    key='exit_button',
                    title='Выход'
                )
            }
