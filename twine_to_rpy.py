# Generate rpy files from a Twine HTML
# -*- coding: utf-8 -*-

import os
import sys
from PyQt4.QtGui import *
from twine_to_rpy_model import TwineToRenpy


class TwineToRenpyView(QWidget):
    def __init__(self):
        super(TwineToRenpyView, self).__init__()

        self.model = TwineToRenpy()

        self.resize(700, 500)
        self.center()

        # MAIN TAB

        # PATHS
        self.html_path_label = QLabel('Twine HTML file', self)
        self.script_dir_label = QLabel('Ren\'Py script directory', self)
        self.gen_dir_btn = QPushButton('Autofill', self)
        self.html_path_le = QLineEdit(self.model.data['html_path'], self)
        self.script_dir_le = QLineEdit(self.model.data['script_dir'], self)
        self.html_path_btn = QPushButton('...', self)
        self.script_dir_btn = QPushButton('...', self)
        width = self.html_path_btn.fontMetrics().boundingRect('  ...  ').width()
        large_width = self.html_path_btn.fontMetrics().boundingRect('  Autofill  ').width()
        self.html_path_btn.setMaximumWidth(width)
        self.script_dir_btn.setMaximumWidth(width)
        self.gen_dir_btn.setMaximumWidth(large_width)

        # Path layouts
        html_path_layout = QHBoxLayout()
        script_dir_layout = QHBoxLayout()
        html_path_layout.addWidget(self.html_path_label)
        html_path_layout.addWidget(self.html_path_le)
        html_path_layout.addWidget(self.html_path_btn)
        script_dir_layout.addWidget(self.script_dir_label)
        script_dir_layout.addWidget(self.script_dir_le)
        script_dir_layout.addWidget(self.gen_dir_btn)
        script_dir_layout.addWidget(self.script_dir_btn)
        paths_layout = QVBoxLayout()
        paths_layout.addLayout(html_path_layout)
        paths_layout.addLayout(script_dir_layout)
        # paths_layout.addWidget(self.gen_dir_btn)

        # Path groupbox
        paths_groupbox = QGroupBox('Filepaths', self)
        paths_groupbox.setLayout(paths_layout)

        # SETTINGS
        settings_layout = QFormLayout()

        vars_layout = QFormLayout()

        # Twine or Ren'Py mode
        self.twine_mode_label = QLabel('Game originally written for', self)
        self.twine_mode_combobox = QComboBox(self)
        twine_mode_items = ['Ren\'Py (Don\'t add narrator quotes)', 'Twine (Add narrator quotes)']
        self.twine_mode_combobox.addItems(twine_mode_items)
        self.twine_mode_combobox.setCurrentIndex(self.model.get_config_value('twine_mode'))
        settings_layout.addRow(self.twine_mode_label, self.twine_mode_combobox)

        # Document break tag
        self.start_name_label = QLabel('Start file name', self)
        self.start_name_le = QLineEdit(self.model.get_config_value('start_name'), self)
        settings_layout.addRow(self.start_name_label, self.start_name_le)

        # Document break tag
        self.doc_break_label = QLabel('End of document tag', self)
        self.doc_break_le = QLineEdit(self.model.get_config_value('doc_break'), self)
        settings_layout.addRow(self.doc_break_label, self.doc_break_le)

        # Label starting with number
        self.number_first_label = QLabel('When labels start with a number:', self)
        self.number_first_combobox = QComboBox(self)
        number_first_items = ['Convert first digit to string', 'Add string to beginning of label']
        self.number_first_combobox.addItems(number_first_items)
        settings_layout.addRow(self.number_first_label, self.number_first_combobox)

        # In front of labels starting with number
        self.number_str_label = QLabel('String to add', self)
        self.number_str_label.setEnabled(False)
        self.number_str_le = QLineEdit(self.model.get_config_value('number_start_str'), self)
        self.number_str_le.setEnabled(False)
        settings_layout.addRow(self.number_str_label, self.number_str_le)

        # Settings groupbox
        settings_groupbox = QGroupBox('Conversion settings', self)
        settings_groupbox.setLayout(settings_layout)

        # Character definitions
        self.char_def_label = QLabel('Define characters', self)
        self.char_def_checkbox = QCheckBox(self)
        self.char_def_checkbox.setChecked(self.model.get_config_value('char_def'))
        vars_layout.addRow(self.char_def_label, self.char_def_checkbox)

        # Variable definitions
        self.var_def_label = QLabel('Define variables', self)
        self.var_def_checkbox = QCheckBox(self)
        self.var_def_checkbox.setChecked(self.model.get_config_value('var_def'))
        vars_layout.addRow(self.var_def_label, self.var_def_checkbox)

        # Variable default values
        self.var_default_label = QLabel('Set variables by default to:', self)
        self.var_default_combobox = QComboBox(self)
        var_default_items = ['Passage value', 'A default value']
        self.var_default_combobox.addItems(var_default_items)
        self.var_default_combobox.setCurrentIndex(self.model.get_config_value('var_mode'))
        vars_layout.addRow(self.var_default_label, self.var_default_combobox)

        # Boolean default value
        self.bool_default_label = QLabel('Boolean default value', self)
        self.bool_default_combobox = QComboBox(self)
        var_default_items = ['False', 'True']
        self.bool_default_combobox.addItems(var_default_items)
        self.bool_default_combobox.setCurrentIndex(self.model.get_config_value('bool_default'))
        vars_layout.addRow(self.bool_default_label, self.bool_default_combobox)

        # Number default value
        self.num_default_label = QLabel('Number default value', self)
        self.num_default_spinbox = QSpinBox()
        self.num_default_spinbox.setValue(self.model.get_config_value('num_default'))
        vars_layout.addRow(self.num_default_label, self.num_default_spinbox)

        # String default value
        self.str_default_label = QLabel('String default value', self)
        self.str_default_combobox = QComboBox(self)
        str_default_items = ['None', 'Blank string']
        self.str_default_combobox.addItems(str_default_items)
        self.str_default_combobox.setCurrentIndex(self.model.get_config_value('str_default'))
        vars_layout.addRow(self.str_default_label, self.str_default_combobox)

        # Chars and variables groupbox
        vars_groupbox = QGroupBox('Characters and variables', self)
        vars_groupbox.setLayout(vars_layout)

        # CONFIG
        self.config_load_btn = QPushButton('Load', self)
        self.config_save_btn = QPushButton('Save', self)
        self.config_reset_btn = QPushButton('Reset to default', self)
        self.config_open_btn = QPushButton('Open', self)

        # Config layout
        config_layout = QHBoxLayout()
        config_layout.addWidget(self.config_load_btn)
        config_layout.addWidget(self.config_save_btn)
        config_layout.addWidget(self.config_reset_btn)
        config_layout.addWidget(self.config_open_btn)

        # Config groupbox
        config_groupbox = QGroupBox('Config', self)
        config_groupbox.setLayout(config_layout)

        # RUN BUTTON
        main_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.execute_btn = QPushButton('Run', self)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(paths_groupbox)
        main_layout.addWidget(settings_groupbox)
        main_layout.addWidget(vars_groupbox)
        main_layout.addWidget(config_groupbox)
        main_layout.addItem(main_spacer)
        main_layout.addWidget(self.execute_btn)

        # REPLACE CHARS TAB

        # Header
        self.og_char_label = QLabel('Twine term', self)
        self.new_char_label = QLabel('Ren\'Py term', self)
        char_title_layout = QHBoxLayout()
        char_title_layout.addWidget(self.og_char_label)
        char_title_layout.addWidget(self.new_char_label)
        replace_chars_layout = QVBoxLayout()
        replace_chars_layout.addLayout(char_title_layout)

        # Scroll area
        self.replace_scroll = QScrollArea()
        self.replace_scroll.setFixedHeight(400)
        self.replace_scroll.setWidgetResizable(True)

        # Scroll widget
        self.scroll_widget = QWidget()
        self.replace_lineedits_layout = QVBoxLayout(self.scroll_widget)

        # Char replace lists
        self.char_replace_layout_list = []
        self.og_char_le_list = []
        self.new_char_le_list = []
        self.del_button_list = []

        # Create the term replace UI
        for i, char_dict in enumerate(self.model.custom_char_replace_list):
            for og_char, new_char in char_dict.iteritems():
                # Create widgets
                og_char_le = QLineEdit(og_char, self)
                new_char_le = QLineEdit(new_char, self)
                char_del_button = QPushButton('x', self)
                width = char_del_button.fontMetrics().boundingRect('  x  ').width() + 7
                char_del_button.setMaximumWidth(width)

                # Add widgets to a horizontal layout
                char_layout = QHBoxLayout()
                char_layout.addWidget(og_char_le)
                char_layout.addWidget(new_char_le)
                char_layout.addWidget(char_del_button)

                # Add to the char layout
                self.replace_lineedits_layout.addLayout(char_layout)

                # Make connections
                og_char_le.textEdited.connect(lambda: self.update_og_term(og_char_le))
                new_char_le.textEdited.connect(lambda: self.update_new_term(new_char_le))

                # Add to the lists
                self.char_replace_layout_list.append(char_layout)
                self.og_char_le_list.append(og_char_le)
                self.new_char_le_list.append(new_char_le)
                self.del_button_list.append(char_del_button)

        # Add spacer at the end so they line up from the top nicely
        #  instead of weirdly evenly spaced
        self.replace_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.replace_lineedits_layout.addItem(self.replace_spacer)

        # Set a widget to scroll widget in order for it to work
        self.replace_scroll.setWidget(self.scroll_widget)

        self.add_char_btn = QPushButton('Add term', self)
        replace_chars_layout.addWidget(self.replace_scroll)
        replace_chars_layout.addWidget(self.add_char_btn)

        # TABS
        tabs = QTabWidget()

        # Create tabs
        tab1 = QWidget()
        tab2 = QWidget()

        # Resize width and height
        tabs.resize(690, 490)

        # Set tab layouts
        tab1.setLayout(main_layout)
        tab2.setLayout(replace_chars_layout)

        # Add tabs
        tabs.addTab(tab1, 'Main')
        tabs.addTab(tab2, 'Replace')

        tabs_layout = QVBoxLayout()
        tabs_layout.addWidget(tabs)

        # Status
        self.status_label = QLabel('Ready!')

        # Add tabs and status label
        all_layout = QVBoxLayout()
        all_layout.addLayout(tabs_layout)
        all_layout.addWidget(self.status_label)

        self.setLayout(all_layout)

        self.setWindowTitle('Twine to Ren\'Py')
        self.show()

        self.make_connections()

    def center(self):
        """
        Center the window on the screen
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def get_path(self, lineedit):
        """
        Display a dialog to get the path of the Twine html file and update the lineedit with it

        Args:
            lineedit: (lineedit) The lineedit displaying the filepath
        """
        filepath = QFileDialog().getOpenFileName(self, 'Select file', '/', 'HTML files (*.html)')
        if filepath:
            lineedit.setText(filepath)

    def get_dir(self, lineedit):
        """
        Display a dialog to get the directory and update the lineedit with it

        Args:
            lineedit: (lineedit) The lineedit displaying the directory
        """
        file_dir = QFileDialog().getExistingDirectory(self, 'Select directory')
        if file_dir:
            lineedit.setText(file_dir)

    def gen_dir(self):
        """
        Generate the directory
        """
        dir_path = str(self.html_path_le.text())
        self.script_dir_le.setText(os.path.dirname(dir_path))
        self.set_status('Set directory path "{}"'.format(dir_path))

    def update_terms(self, og_char, new_char, index):
        """
        Update the terms  in the dictionary by completely clearing it then setting the new one
        The dictionary should only ever be one pair

        Args:
            og_char: (str) The Twine term to be replaced
            new_char: (str) The Ren'Py term
            index: (int) The index of the term to be updated
        """
        self.model.custom_char_replace_list[index].clear()
        self.model.custom_char_replace_list[index] = {og_char: new_char}

    # TODO Not sure if this is broken...
    def update_og_term(self, og_char_le):
        """
        Update the old term in the model data

        Args:
            og_char_le: (lineedit) The lineedit of the old term
        """
        # Get the index
        index = self.og_char_le_list.index(og_char_le)
        # Get both terms
        og_char = str(og_char_le.text())
        new_char = str(self.new_char_le_list[index].text())
        self.update_terms(og_char, new_char, index)

    def update_new_term(self, new_char_le):
        """
        Update the new term in the model data

        Args:
            new_char_le: (lineedit) The lineedit of the new term
        """
        # Get the index
        index = self.new_char_le_list.index(new_char_le)
        # Get both terms
        og_char = str(self.new_char_le_list[index].text())
        new_char = str(new_char_le.text())
        self.update_terms(og_char, new_char, index)

    def add_term(self):
        """
        Add a new Twine to Ren'Py replacement term by creating the UI and adding a line to the list
        """
        # Create term widgets
        og_char_le = QLineEdit(self)
        new_char_le = QLineEdit(self)
        char_del_button = QPushButton('x', self)
        width = char_del_button.fontMetrics().boundingRect('  x  ').width() + 7
        char_del_button.setMaximumWidth(width)

        # Add widgets to a horizontal layout
        char_layout = QHBoxLayout()
        char_layout.addWidget(og_char_le)
        char_layout.addWidget(new_char_le)
        char_layout.addWidget(char_del_button)

        # Add to the char layout
        self.replace_lineedits_layout.removeItem(self.replace_spacer)
        self.replace_lineedits_layout.addLayout(char_layout)
        self.replace_lineedits_layout.addItem(self.replace_spacer)

        # Make connections
        og_char_le.textEdited.connect(lambda: self.update_og_term(og_char_le))
        new_char_le.textEdited.connect(lambda: self.update_new_term(new_char_le))

        # Add to lists
        self.char_replace_layout_list.append(char_layout)
        self.og_char_le_list.append(og_char_le)
        self.new_char_le_list.append(new_char_le)
        self.del_button_list.append(char_del_button)
        char_del_button.clicked.connect(lambda state, x=char_del_button: self.del_term(x))

        # Add the blank term to the data
        self.model.custom_char_replace_list.append({})

        # Update status
        self.set_status('Added term')

    def del_term(self, del_btn):
        """
        Delete a replacement term

        Args:
            del_btn: (pushbutton) The delete button associated with the term line to delete
        """
        # Get the index of the button to delete
        del_index = self.del_button_list.index(del_btn)
        # Delete the layout
        self.del_layout(self.char_replace_layout_list.pop(del_index))
        # Remove the widgets from the lists
        del self.og_char_le_list[del_index]
        del self.new_char_le_list[del_index]
        del self.del_button_list[del_index]
        # Delete the data line
        del self.model.custom_char_replace_list[del_index]

        # Status
        self.set_status('Deleted term')

    def del_layout(self, layout):
        """
        Remove a layout and all its associated widgets

        Args:
            layout: (layout) PyQt layout to remove
        """
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.del_layout(item.layout())

    def update_le_model_data(self, key_name, lineedit):
        """
        Update model data from lineedit text

        Args:
            key_name: (str) Key of the data to update
            lineedit: (lineedit) Lineedit to pull the text from
        """
        self.model.data[key_name] = str(lineedit.text())

    def update_cb_model_data(self, key_name, combobox):
        """
        Update model data with combobox index

        Args:
            key_name: (str) Key of the data to set
            combobox: (combobox) Combobox to get data from
        """
        self.model.data[key_name] = combobox.currentIndex()

    def update_cb_bool_model_data(self):
        """
        Update model data with combobox index
        """
        bool_value = False
        if self.bool_default_combobox.currentIndex():
            bool_value = True
        self.model.data['bool_default'] = bool_value

    def update_checkbox_model_data(self, key_name, checkbox):
        """
        Update the value of the key_name in model data with combobox index

        Args:
            key_name: (str) Key of the data to set
            checkbox: (checkbox) Checkbox to get data from
        """
        self.model.data[key_name] = checkbox.isChecked()

    def update_sb_value(self):
        """
        Update default number in model data with spinbox number
        """
        self.model.data['num_default'] = self.num_default_spinbox.value()

    def set_number_mode_state(self):
        """
        Update model data with proper mode for handling number first labels
        """
        number_mode = self.number_first_combobox.currentIndex()
        self.number_str_label.setEnabled(number_mode)
        self.number_str_le.setEnabled(number_mode)
        self.model.data['number_mode'] = number_mode

    def set_var_define_state(self):
        """
        Update model data with proper mode for variable definitions
        """
        var_def = self.var_def_checkbox.isChecked()
        self.model.data['var_def'] = var_def
        self.var_default_label.setEnabled(var_def)
        self.var_default_combobox.setEnabled(var_def)
        # Next decide wheter default values are enabled
        var_default_enabled = var_def
        # If we're turning on variables, set it to whatever the current var default mode is
        # If not, it will just retain the False state from the var_def
        if var_def:
            var_default_enabled = self.var_default_combobox.currentIndex()
        self.bool_default_label.setEnabled(var_default_enabled)
        self.bool_default_combobox.setEnabled(var_default_enabled)
        self.num_default_label.setEnabled(var_default_enabled)
        self.num_default_spinbox.setEnabled(var_default_enabled)
        self.str_default_label.setEnabled(var_default_enabled)
        self.str_default_combobox.setEnabled(var_default_enabled)

    def set_var_default_state(self):
        """
        Update model data with proper mode for variable defaults
        """
        var_mode = self.var_default_combobox.currentIndex()
        self.bool_default_label.setEnabled(var_mode)
        self.bool_default_combobox.setEnabled(var_mode)
        self.num_default_label.setEnabled(var_mode)
        self.num_default_spinbox.setEnabled(var_mode)
        self.str_default_label.setEnabled(var_mode)
        self.str_default_combobox.setEnabled(var_mode)
        self.model.data['var_mode'] = var_mode

    def populate_le(self, lineedit, key):
        """
        Populate a lineedit with the data value from a key

        Args:
            lineedit: (lineedit) Lineedit to populate
            key: (str) Key of the data to look up
        """
        lineedit.setText(str(self.model.data.get(key, '')))

    def repopulate_ui(self):
        """
        Populate the UI with data from the model
        """
        self.populate_le(self.html_path_le, 'html_path')
        self.populate_le(self.script_dir_le, 'script_dir')
        self.populate_le(self.number_str_le, 'number_start_str')
        self.populate_le(self.doc_break_le, 'doc_break')
        self.number_first_combobox.setCurrentIndex(self.model.data.get('number_mode', 0))

        # Clear the replace lists and delete the layout
        self.del_layout(self.replace_lineedits_layout)
        self.char_replace_layout_list = []
        self.og_char_le_list = []
        self.new_char_le_list = []
        self.del_button_list = []

        # Remake the replace terms UI
        for i, char_dict in enumerate(self.model.custom_char_replace_list):
            for og_char, new_char in char_dict.iteritems():
                # Create widgets
                og_char_le = QLineEdit(og_char, self)
                new_char_le = QLineEdit(new_char, self)
                char_del_button = QPushButton('x', self)
                width = char_del_button.fontMetrics().boundingRect('  x  ').width() + 7
                char_del_button.setMaximumWidth(width)
                # Add widgets to a horizontal layout
                char_layout = QHBoxLayout()
                char_layout.addWidget(og_char_le)
                char_layout.addWidget(new_char_le)
                char_layout.addWidget(char_del_button)
                # Add to the char layout
                self.replace_lineedits_layout.addLayout(char_layout)
                # Add to the lists
                self.char_replace_layout_list.append(char_layout)
                self.og_char_le_list.append(og_char_le)
                self.new_char_le_list.append(new_char_le)
                self.del_button_list.append(char_del_button)
        self.replace_lineedits_layout.addItem(self.replace_spacer)
        # Make the term replace connections again
        self.make_char_connections()

    def load_config(self):
        """
        Load the config data again and repopulate the UI
        """
        if self.model.load_config():
            self.repopulate_ui()
            self.set_status('Reloaded data from config.json')
        else:
            self.set_status('Could not reload data from config.json')

    def save_config(self):
        """
        Write the config data to config.json
        """
        self.model.write_config()
        self.set_status('Saved data to config.json')

    def reset_config(self):
        """
        Reset config to default data and repopulate the UI
        """
        self.model.reset_config()
        self.repopulate_ui()
        self.set_status('Reset config.json to default')

    def open_config(self):
        """
        Open config in notepad
        """
        self.set_status('Opening config in Notepad')
        self.model.open_config()

    def run(self):
        """
        Run the script. Update status with whether it succeeds or fails
        """
        if self.model.run():
            self.set_status('Run successful! Output Ren\'Py scripts to "{}"'.format(self.model.data['script_dir']))
        else:
            self.set_status('Failed! Check the file exists and for empty passages.')

    def set_status(self, text):
        """
        Update the status label at the bottom of the UI
        """
        self.status_label.setText(text)

    def make_char_connections(self):
        """
        Make the char UI connections. This is broken out because when the UI gets repopulated,
        the replace term connections will need to be remade again
        """
        # Use lambda state to make sure the current widget is passed in
        for del_button in self.del_button_list:
            del_button.clicked.connect(lambda state, x=del_button: self.del_term(x))
        for og_char_le in self.og_char_le_list:
            og_char_le.textEdited.connect(lambda state, x=og_char_le: self.update_term(x))
        for new_char_le in self.og_char_le_list:
            new_char_le.textEdited.connect(lambda state, x=new_char_le: self.update_term(x))

    def make_connections(self):
        """
        Make UI connections
        """
        # Filepaths
        self.html_path_btn.clicked.connect(lambda: self.get_path(self.html_path_le))
        self.script_dir_btn.clicked.connect(lambda: self.get_dir(self.script_dir_le))
        # Text *changed* instead of edited for the below since the file dialogs will update the lineedit
        #  But in addition this will also account for edits
        self.html_path_le.textChanged.connect(lambda: self.update_le_model_data('html_path', self.html_path_le))
        self.script_dir_le.textChanged.connect(lambda: self.update_le_model_data('script_dir', self.script_dir_le))
        self.gen_dir_btn.clicked.connect(self.gen_dir)

        # Conversion settings
        self.twine_mode_combobox.currentIndexChanged.connect(
            lambda: self.update_cb_model_data('twine_mode', self.twine_mode_combobox))
        self.start_name_le.textChanged.connect(lambda: self.update_le_model_data('start_name', self.start_name_le))
        self.doc_break_le.textChanged.connect(lambda: self.update_le_model_data('doc_break', self.doc_break_le))
        self.number_first_combobox.currentIndexChanged.connect(self.set_number_mode_state)
        self.number_str_le.textChanged.connect(lambda: self.update_le_model_data('number_start_str', self.doc_break_le))

        # Characters and variables
        self.char_def_checkbox.stateChanged.connect(
            lambda: self.update_checkbox_model_data('char_def', self.char_def_checkbox))
        self.var_def_checkbox.stateChanged.connect(self.set_var_define_state)
        self.var_default_combobox.currentIndexChanged.connect(self.set_var_default_state)
        self.bool_default_combobox.currentIndexChanged.connect(self.update_cb_bool_model_data)
        self.num_default_spinbox.valueChanged.connect(self.update_sb_value)
        self.str_default_combobox.currentIndexChanged.connect(
            lambda: self.update_cb_model_data('str_default', self.str_default_combobox))

        # Config buttons
        self.config_reset_btn.clicked.connect(self.reset_config)
        self.config_load_btn.clicked.connect(self.load_config)
        self.config_save_btn.clicked.connect(self.save_config)
        self.config_open_btn.clicked.connect(self.open_config)

        # Run button
        self.execute_btn.clicked.connect(self.run)

        # Replace terms
        self.add_char_btn.clicked.connect(self.add_term)

        # Replace character connections are a separate function since they need to be rerun when UI is regenerated
        self.make_char_connections()


def main():
    app = QApplication(sys.argv)
    TwineToRenpyView()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
