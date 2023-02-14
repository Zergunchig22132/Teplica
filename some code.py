import requests
import time
import random
import multiprocessing

from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.icon_definitions import md_icons
from kivymd.uix.toolbar import MDTopAppBar

class Tab(MDBoxLayout, MDTabsBase):
    pass

class mylabel(MDLabel):
    def update(self, *args):
        self.text = str(random.randint(1, 6000000))

class TestApp(MDApp):
    icons = list(md_icons.keys())[15:30]
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        layout = BoxLayout(orientation='vertical')
        label1 = mylabel()
        Clock.schedule_interval(label1.update, 1)
        return(
            MDBoxLayout(
                MDTopAppBar(title='Example tabs'),
                MDTabs(id="tabs"),
                orientation="vertical",
            )
        )

    def on_start(self):
        self.root.ids.tabs.bind(on_tab_switch=self.on_tab_switch)

        for tab_name in self.icons:
            self.root.ids.tabs.add_widget(
                Tab(
                    MDIconButton(
                        icon=tab_name,
                        icon_size="48sp",
                        pos_hint={"center_x": .5, "center_y": .5},
                    ),
                    label1()
                    icon=tab_name,
                )
            )

    def on_tab_switch(
        self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):
        '''
        Called when switching tabs.

        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        '''

        count_icon = instance_tab.icon  # get the tab icon
        print(f"Welcome to {count_icon}' tab'")


root = TestApp()
root.run()
