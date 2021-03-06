# -*- coding: utf-8 -*-

'''This module contains classes to represent the main page.'''

import PyQt4.QtGui      as QtGui
import PyQt4.QtCore     as QtCore

from gui.qt4ui.Utils import tr

import extension
import gui

class MainPage (QtGui.QWidget, gui.MainWindowBase):
    '''The main page (the one with the contact list)'''
    # pylint: disable=W0612
    NAME = 'MainPage'
    DESCRIPTION = 'The widget used to to dislay the main screen'
    AUTHOR = 'Gabriele "Whisky" Visconti'
    WEBSITE = ''
    # pylint: enable=W0612

    def __init__(self,  session, on_new_conversation, set_menu_bar_cb, parent=None):
        '''Constructor'''
        QtGui.QWidget.__init__(self, parent)
        gui.MainWindowBase.__init__(self, session, on_new_conversation)
        # callbacks:
        self._set_menu_bar_cb = set_menu_bar_cb

        # menu objects:
        self._main_menu = None
        self._contact_menu = None
        self._group_menu = None

        # a widget dic to avoid proliferation of instance variables:
        self._widget_dict = {}
        self._setup_ui()

        # emesene's
        self.contact_list = self._widget_dict['contact_list']

        # Session's Signals: [Remember to unsubscribe! O_O]
        session.signals.profile_get_succeed.subscribe(
                                self._on_ss_profile_get_succeed)
        session.signals.status_change_succeed.subscribe(
                                self._widget_dict['status_combo'].set_status)

    def _setup_ui(self):
        '''Instantiates the widgets, and sets the layout'''
        widget_dict = self._widget_dict

        nick_edit_cls = extension.get_default('nick edit')
        status_combo_cls = extension.get_default('status combo')
        avatar_cls = extension.get_default('avatar')
        contact_list_cls = extension.get_default('contact list')

        nick_box = QtGui.QHBoxLayout()
        widget_dict['nick_edit'] = nick_edit_cls()
        widget_dict['mail_btn']  = QtGui.QToolButton()
        widget_dict['mail_btn'].setAutoRaise(True)
        widget_dict['mail_btn'].setIcon(
                                    QtGui.QIcon.fromTheme('mail-unread'))
        widget_dict['mail_btn'].setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        widget_dict['mail_btn'].setText("(0)")
        nick_box.addWidget(widget_dict['nick_edit'])
        nick_box.addWidget(widget_dict['mail_btn'])

        widget_dict['psm_edit'] = nick_edit_cls(allow_empty=True,
            empty_message=QtCore.QString(
                tr('<u>Click here to set a personal message...</u>')))
        widget_dict['current_media'] = QtGui.QLabel()
        widget_dict['status_combo'] = status_combo_cls()
        widget_dict['display_pic'] = avatar_cls(self.session)
        widget_dict['contact_list'] = contact_list_cls(self.session)
        my_info_lay_left = QtGui.QVBoxLayout()
        my_info_lay_left.addLayout(nick_box)
        my_info_lay_left.addWidget(widget_dict['psm_edit'])
        my_info_lay_left.addWidget(widget_dict['current_media'])
        my_info_lay_left.addWidget(widget_dict['status_combo'])

        my_info_lay = QtGui.QHBoxLayout()
        my_info_lay.addWidget(widget_dict['display_pic'])
        my_info_lay.addLayout(my_info_lay_left)

        lay = QtGui.QVBoxLayout()
        lay.addLayout(my_info_lay)
        lay.addWidget(widget_dict['contact_list'])
        self.setLayout(lay)

        # First fill of personal Infos:
        self._on_ss_profile_get_succeed('','')

        widget_dict['nick_edit'].nick_changed.connect(
                                        self._on_set_new_nick)
        widget_dict['psm_edit'].nick_changed.connect(
                                        self._on_set_new_psm)
        widget_dict['status_combo'].status_changed.connect(
                                        self._on_set_new_status)
        widget_dict['display_pic'].clicked.connect(
                                        self._on_display_pic_clicked)
        widget_dict['contact_list'].new_conversation_requested.connect(
                                        self.on_new_conversation_requested)
        widget_dict['mail_btn'].clicked.connect(
                                    self._on_mail_click)

    def _on_ss_profile_get_succeed(self, nick, psm):
        '''This method sets the displayed account's info,
        retrieving data from "_session" object'''
        if nick == '':
            nick = self.session.contacts.me.display_name
        if psm == '':
            psm = self.session.contacts.me.message
        status = self.session.contacts.me.status

        widget_dict = self._widget_dict
        widget_dict['nick_edit'].set_text(nick)
        widget_dict['psm_edit'].set_text(psm)
        widget_dict['status_combo'].set_status(status)
        #print "display pic path: %s" % display_pic_path
        # investigate display pic...
        widget_dict['display_pic'].set_display_pic_of_account()

    def _on_new_conversation_requested(self, account):
        '''Slot called when the user doubleclicks
        an entry in the contact list'''
        self.on_new_conversation_requested(account)

    def _on_set_new_nick(self, nick):
        '''Slot called when user tries to se a new nick'''
        self.session.set_nick(nick)
        # to be completed handling the subsequent signal from e3

    def _on_set_new_psm(self, psm):
        '''Slot called when the user tries to set a new psm'''
        self.session.set_message(psm)
        # to be completed handling the subsequent signal from e3

    def _on_set_new_status(self, status):
        '''Slot called when the user tries to set a new status'''
        self.session.set_status(status)
        # to be completed handling the subsequent signal from e3

    def _on_display_pic_clicked(self):
        '''Slot called when the user clicks the display pic. It shows
        the AvatarChooser'''
        chooser_cls = extension.get_default('avatar chooser')
        chooser = chooser_cls(self.session)
        chooser.exec_()

    def _on_mail_count_changed(self, count):
        widget_dict = self._widget_dict
        widget_dict['mail_btn'].setText("(%d)" % count)

    def _on_mail_click(self):
        self.on_mail_click()

    def replace_extensions(self):
        #FIXME: add extension support
        #below_userlist, below_menu, below_panel
        #we can only import qt extensions
        pass

