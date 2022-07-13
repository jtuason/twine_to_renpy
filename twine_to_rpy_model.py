# -*- coding: utf-8 -*-

import os
import json
import webbrowser
from collections import OrderedDict
from bs4 import BeautifulSoup

# Replace dict: {Original term: Replace term}
#  Note for defaults:
#  Tabs get converted to spaces
#  Newline should have a tab in front of it
#  The commented out line is easier to run from python, but otherwise causes errors from pyinstaller dist
DEFAULT_CONFIG_DATA = {
    'html_path': '',
    'script_dir': '',
    'default_replace': [{'\t': '    '}, {'\n': '\n    '}],
    'custom_replace': [{'\u201c': '\"'}, {'\u201d': '\"'}, {'\u2019': '\\\''},
                       {'Double-click this passage to edit it.': 'pass'}],
    # 'custom_replace': [{'“': '\"'}, {'”': '\"'}, {'’': '\\\''}, {'Double-click this passage to edit it.': 'pass'}],
    'twine_mode': 0,
    'start_name': 'start',
    'doc_break': 'doc_break',
    'char_def': True,
    'var_def': True,
    'var_mode': 1,
    'bool_default': False,
    'num_default': 0,
    'str_default': 1,
    'number_mode': 0,
    'number_start_str': 'label_'
}

DIGIT_TO_STR_DICT = {'0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five',
                     '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine', '10': 'ten'}


QUOTE_CHAR_LIST = ['"', '“', '”']


def decode_bytes(o):
    """
    Decode using UTF-8
    """
    return o.decode('utf-8')


def digit_to_string(string):
    """
    Convert a digit to its string equivalent

    Args:
        string: (str) String to convert

    Returns:
        (str): Written out version of the digit
    """
    # Iterate over the list of characters to update
    for og_char, new_char in DIGIT_TO_STR_DICT.iteritems():
        string = string.replace(og_char, new_char)
    return string


def only_whitespace_after_choice(choice_split):
    """
    Check if there's only whitespace after a choice
    This is useful for finding a series of Twine choices

    Args:
        choice_split: (list) The passage string after split with '[[' then currently ']]'

    Returns:
        (bool): Whether there is only whitespace after the choice
    """
    # Check first that the string was split in the first place
    if len(choice_split) > 1:
        # If it was, strip the string of trailing whitespace + newlines
        str_between_choices = choice_split[1].rstrip()
        # If its new length is less than 1, then it only contains whitespace
        if len(str_between_choices) < 1:
            return True
        else:
            return False


def strip_quotes(choice_text):
    """
    Strip quotes from choice text since it will be hardcoded anyway.

    Args:
        choice_text: (str) The choice text that will be on a Ren'Py

    Returns:
        (str): The choice text stripped of any quotes
    """
    for quote_char in QUOTE_CHAR_LIST:
        choice_text = choice_text.replace(quote_char, '')
    return choice_text


class TwineToRenpy:
    def __init__(self):
        # Get the config path by getting current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(current_dir, 'config.json')

        # Check if the config json exists
        if os.path.exists(self.config_path):
            # If it does, load the json data from the config path
            json_data = open(self.config_path).read()
            self.data = json.loads(json_data, object_pairs_hook=OrderedDict)
        else:
            # If not, load the default data and create a new config json file
            self.reset_config()

        # Create replace lists
        self.default_char_replace_list = []
        self.custom_char_replace_list = []
        self.char_replace_list = []
        self.load_replace_lists()

    def load_replace_lists(self):
        """
        Load the lists of replace terms
        """
        self.default_char_replace_list = self.data['default_replace']
        self.custom_char_replace_list = self.data['custom_replace']

    def load_config(self):
        """
        Load data from the config file

        Returns:
            (bool): Whether the config could be loaded
        """
        # Check if the config json exists
        if os.path.exists(self.config_path):
            # If it does, load the json data from the config path
            json_data = open(self.config_path).read()
            self.data = json.loads(json_data, object_pairs_hook=OrderedDict)
            self.load_replace_lists()
            return True
        else:
            return False

    def write_config(self):
        """
        Write current data to the config file
        """
        self.data['custom_replace'] = self.custom_char_replace_list
        with open(self.config_path, 'w') as outfile:
            json.dump(self.data, outfile, indent=4)

    def reset_config(self):
        """
        Reset the config.json + data to the default config data
        """
        self.data = OrderedDict(DEFAULT_CONFIG_DATA)
        with open(self.config_path, 'w') as outfile:
            json.dump(self.data, outfile, default=decode_bytes, indent=4)

    def open_config(self):
        """
        Open the config file using webbrowser
        """
        webbrowser.open(self.config_path)

    def get_config_value(self, config_key):
        """
        Get the config value if it exists
        If it doesn't, default to returning the default config data

        Args:
            config_key: (str) Config key to find

        Returns:
            (data): Config value if found, default value if not
        """
        return self.data.get(config_key, DEFAULT_CONFIG_DATA.get(config_key, ''))

    def to_rpy_name(self, name):
        """
        Convert passage titles/jump statements to label friendly names

        Args:
            name: (str) Original Twine passage name

        Returns:
            (str): New Ren'Py label name
        """
        name = name.lower().replace(' ', '_')
        new_name = ''
        for char_index, char in enumerate(name):
            # Check if the first character is a number
            if char_index is 1:
                # If so, either change the digit to a string
                #  or add a string in front of the label
                if char.isdigit():
                    if self.data['number_mode'] == 0:
                        new_name = digit_to_string(char)
                    else:
                        new_name = self.data['number_start_str'] + char
                else:
                    new_name += char
            else:
                # Check if the current character is alphanumeric or _ which is acceptable
                if char.isalnum() or char == '_':
                    new_name += char
        return new_name

    def data_validated(self):
        """
        Validate the data needed to execute the script

        Returns:
            (Bool): Whether the script has the appropriate paths to run
        """
        # Check the html path has data stored
        html_path = self.data.get('html_path', False)
        if html_path:
            # If it does, check if the path exists and that the extension is .html
            if not os.path.exists(html_path) or os.path.splitext(str(html_path).lower())[1] != '.html':
                return False
        else:
            return False
        # Check that the script dir has a directory stored and also that it's a directory
        script_dir = self.data.get('script_dir', False)
        if script_dir:
            if not os.path.isdir(script_dir):
                return False
        else:
            return False
        # If this looks good, return True
        return True

    def run(self):
        """
        Convert a Twine HTML file to Ren'Py files and output them to a script directory
        """
        # First validate the data: If it's not enough to run, return False
        if not self.data_validated():
            return False

        # Save the settings
        self.write_config()

        # Open the HTML file as a soup
        with open(self.data['html_path'], 'r') as html_file:
            soup = BeautifulSoup(html_file, 'html.parser')

        # Get the list of passages
        raw_passage_list = soup.find_all('tw-passagedata')

        document_passage = ''
        rpy_file_name = self.get_config_value('start_name') + '.rpy'
        create_file_name = False
        passage_list = []
        raw_name_list = []

        # Get list of all variables to declare at the beginning
        raw_variables_dict = {}

        # Check for <<set $[variable] to [value] ("[STRING]"/BOOLEAN/INT)>>
        # Swap to $ [variable] = [value]
        set_phrase = '<<set $'
        boolean_replace_dict = {'true': 'True', 'false': 'False'}

        # Do a prepass on ALL passages to get all of the characters and variables that need to be defined
        for passage in raw_passage_list:
            # Create the passage name to use for the label (is the same as jump statement)
            passage_tags = passage['tags']
            # Only add passages that don't have this tag
            if passage_tags != 'Twine.image':
                passage_list.append(passage)

                # Convert passage from ascii to unicode
                unicode_passage = passage.string.encode('utf-8')

                # Get list of characters if asked to generate
                if self.get_config_value('char_def'):
                    # Split by every line
                    newline_split = unicode_passage.split('\n')
                    for newline in newline_split:
                        newline = newline.strip()
                        if len(newline) > 0:
                            # Check if the line starts with a letter, which is likely a speaking character
                            # If formatted properly for Ren'Py scripting
                            if newline[0].isalpha():
                                char_name_split = newline.split(' "', 1)
                                if len(char_name_split) > 1:
                                    raw_name_list.append(char_name_split[0])
                # Define variables if asked to generate
                if self.get_config_value('var_def'):
                    # Check if we're setting variables
                    if set_phrase in unicode_passage:
                        set_passage_split_list = unicode_passage.split(set_phrase)
                        # Start after the first instance of the set phrase
                        for set_passage_split in set_passage_split_list[1:]:
                            # Get the set statement by splitting at next immediate instance of >>
                            set_passage_split_list = set_passage_split.split('>>', 1)
                            # This is our set statement
                            set_passage_statement = set_passage_split_list[0]
                            # Split out the variable name and the value
                            variable_name, variable_value = set_passage_statement.split(' to ')
                            # Replace Twine boolean phrase with the Ren'Py/Python accepted one
                            for boolean_phrase, boolean_replace in boolean_replace_dict.iteritems():
                                if boolean_phrase in set_passage_statement:
                                    variable_value = set_passage_statement.replace(boolean_phrase,
                                                                                   boolean_replace)
                            # If setting vars to a default value, try to discern the variable type
                            # Then set to the specified defaults
                            if self.get_config_value('var_mode'):
                                if variable_value.strip() == 'True' or variable_value.strip() == 'False':
                                    variable_value = self.get_config_value('bool_default')
                                if variable_value.isdigit():
                                    variable_value = self.get_config_value('num_default')
                                else:
                                    # Set this to string or None based on default str setting
                                    variable_value = '\'\'' if self.get_config_value('str_default') else None
                            # If not using a default value, it will just be set to whatever it was in the passage
                            raw_variables_dict[variable_name] = variable_value

        # Strip down to a list of unique names
        final_name_list = list(set(raw_name_list))
        # Then generate a string of char definitions that will be attached to the top of the script
        char_def_str = ''
        for char_name in final_name_list:
            char_def_str += 'define {} = Character("{}")\n'.format(char_name, char_name.replace('_', ' '))

        # Add character defs to the document passage if desired
        if self.get_config_value('char_def'):
            document_passage += '{}\n'.format(char_def_str)

        # Generate a string of variable definitions to attach after characters but before the script
        var_def_str = ''
        for variable_name, variable_value in raw_variables_dict.iteritems():
            var_def_str += 'default {} = {}\n'.format(variable_name, variable_value)

        # Add variable defs to the document passage if desired
        if self.get_config_value('var_def'):
            document_passage += '{}\n'.format(var_def_str)

        # Generate an rpy file for each passage
        for passage_index, passage in enumerate(passage_list):
            # Create the passage name to use for the label (is the same as jump statement)
            passage_name = self.to_rpy_name(passage['name'])
            passage_tags = passage['tags']

            # Create file name for the first passage/iteration
            #  then set to False until the rpy file is written and it is reset
            if create_file_name:
                rpy_file_name = passage_name + '.rpy'
                create_file_name = False

            if passage is None or passage.string is None:
                passage.string = ''

            # Convert passage from ascii to unicode
            unicode_passage = passage.string.encode('utf-8')

            # A "Twine mode" that adds " to every newline as if all lines are spoken by a Ren'Py narrator
            quotes_passage = ''
            if self.get_config_value('twine_mode'):
                # Avoid adding quotes to lines that start with a link or if statement
                avoid_quotes_list = ['[[', '<<']
                quotes_passage_split = unicode_passage.split('\n')
                for passage_split in quotes_passage_split:
                    if passage_split == "Double-click this passage to edit it.":
                        # This phrase usually gets replaced with pass, but with this mode pass could be encased in "
                        # And therefore printed to Ren'Py script
                        # We will leave it as is so it can be replace later properly
                        # Or allow the user to apply their own custom replace
                        quotes_passage += passage_split
                    else:
                        # Add \ to " in the middle of passages
                        if "\"" in passage_split:
                            passage_split = passage_split.replace("\"", "\\\"")

                        # Check if the split has at least 2 characters
                        if len(passage_split) > 1:
                            # By default we'll apply quotes
                            apply_quotes = True
                            # Unless it contains a phrase that denote it's actually a code line
                            # Then we will avoid applying quotes
                            for avoid_phrase in avoid_quotes_list:
                                if passage_split[0] + passage_split[1] == avoid_phrase:
                                    # If it does, set to apply quotes flag to false
                                    apply_quotes = False
                                    break
                            if apply_quotes:
                                quotes_passage += '"{}"\n'.format(passage_split)
                            else:
                                quotes_passage += '{}\n'.format(passage_split)
                        else:
                            quotes_passage += '{}\n'.format(passage_split)
            else:
                quotes_passage = unicode_passage

            # Convert the twine [[next passage]] to rpy jump statements
            # Start by splitting the file using [[
            split_passage = quotes_passage.split('[[')

            # Check the passage first for a Twine like menu with list of choices
            passage_index_with_whitespace = []
            twine_menu_indeces = []
            # If the passage has at least two [[ (by having more than three indeces in the list)
            #  then iterate through the passage sections to see if they're Twine-like menus.
            #  Otherwise, this is just a normal jump at the end of a passage.
            twine_menu_indeces_groupings_dict = OrderedDict()
            final_menu_groupings_dict = OrderedDict()
            twine_menu_indeces_dict = OrderedDict()
            current_group_index = 0
            if len(split_passage) > 2:
                in_choice_group = False
                for i, passage_section in enumerate(split_passage):
                    choice_split = passage_section.split(']]')
                    if len(choice_split) > 1:
                        if only_whitespace_after_choice(choice_split):
                            # Check if we're currently in a choice group
                            if not in_choice_group:
                                # If not, we are now
                                # Create a new list of indeces...
                                in_choice_group = True
                                twine_menu_indeces_groupings_dict[current_group_index] = []
                            # If this is the last index, only add the current one
                            if i + 1 == len(split_passage):
                                twine_menu_indeces_groupings_dict[current_group_index].append(i)
                                passage_index_with_whitespace.append(i)
                            # Otherwise add the current plus the one after
                            else:
                                twine_menu_indeces_groupings_dict[current_group_index].extend([i, i+1])
                                passage_index_with_whitespace.extend([i, i+1])
                        else:
                            # Check if we were currently in a choice group
                            if in_choice_group:
                                # If we were, we aren't now
                                in_choice_group = False
                                # Iterate our index
                                current_group_index += 1
                            else:
                                # If not in a group, this is probably a standalone choice
                                twine_menu_indeces_groupings_dict[current_group_index] = []
                                twine_menu_indeces_groupings_dict[current_group_index].append(i)
                                passage_index_with_whitespace.append(i)
                                current_group_index += 1
                twine_menu_indeces = list(set(passage_index_with_whitespace))
                for choice_index, choice_list in twine_menu_indeces_groupings_dict.iteritems():
                    final_menu_groupings_dict[choice_index] = list(set(choice_list))
                for choice_index, choice_list in final_menu_groupings_dict.iteritems():
                    # Based on the choice index groups, we will assign whether the choices are
                    #  first, middle, or end of a group. Or whether they are standalone choices.
                    for i, choice_split_index in enumerate(choice_list):
                        if i == 0 and i+1 == len(choice_list):
                            twine_menu_indeces_dict[choice_split_index] = 'standalone'
                        elif i == 0:
                            twine_menu_indeces_dict[choice_split_index] = 'start'
                        elif i+1 == len(choice_list):
                            twine_menu_indeces_dict[choice_split_index] = 'end'
                        else:
                            twine_menu_indeces_dict[choice_split_index] = 'middle'

            # Create a string for the rpy jump statement version of the passage
            jump_passage = ''
            # If the passage has at least one [[ (by having more than one index in the list)
            #  then iterate through the passage sections
            if len(split_passage) > 1:
                # Check if using Twine-like choices for conversion to Ren'Py menus
                #  by seeing if there are any stored indeces from above.
                if len(twine_menu_indeces) > 1:
                    for passage_split_index, passage_section in enumerate(split_passage):
                        # If the current index was one of the twine menu indeces, then process it accordingly
                        if passage_split_index in twine_menu_indeces_dict:
                            passage_section_split = passage_section.split(']]')
                            jump_statement = passage_section_split[0]
                            # Check if there are link ends at all
                            passage_rest = ''
                            if len(passage_section_split) > 1:
                                passage_rest = passage_section_split[1]
                            choice_text = jump_statement
                            if len(jump_statement.split('|')) > 1:
                                choice_text, jump_statement = jump_statement.split('|')
                            # Strip the quotes if it has any since we'll be adding these anyway
                            choice_text = strip_quotes(choice_text)

                            # If this is the first Twine menu index, generate the menu start
                            if twine_menu_indeces_dict[passage_split_index] == 'start':
                                jump_passage += 'menu:\n    "{}":\n        jump {}\n    '.\
                                    format(choice_text, self.to_rpy_name(jump_statement))
                            # If it's the last one, we don't need the trailing newline
                            elif twine_menu_indeces_dict[passage_split_index] == 'end':
                                jump_passage += '"{}":\n        jump {}{}'.\
                                    format(choice_text, self.to_rpy_name(jump_statement), passage_rest)
                            # If it's standalone, menu and jump
                            elif twine_menu_indeces_dict[passage_split_index] == 'standalone':
                                jump_passage += 'menu:\n    "{}":\n        jump {}{}'. \
                                    format(choice_text, self.to_rpy_name(jump_statement), passage_rest)
                            # All others will use the newline
                            else:
                                jump_passage += '"{}":\n        jump {}\n    '. \
                                    format(choice_text, self.to_rpy_name(jump_statement))
                        # We don't immediately write the first passage to the string just in case it's actually a menu
                        #  If it isn't a menu though, then we can go ahead and write it
                        elif passage_split_index == 0:
                            # If this is the first passage section, populate the string
                            jump_passage = passage_section
                # Otherwise use Ren'Py-like menus
                else:
                    # Start by populating the first string
                    jump_passage = split_passage[0]
                    for passage_section in split_passage[1:]:
                        # Split the passage into jump statement + the rest of passage
                        passage_section_split = passage_section.split(']]')
                        jump_statement = passage_section_split[0]
                        if len(passage_section_split) > 1:
                            passage_rest = passage_section_split[1]
                        else:
                            passage_rest = ''
                        choice_text = jump_statement
                        if len(jump_statement.split('|')) > 1:
                            choice_text, jump_statement = jump_statement.split('|')
                        # Strip the quotes if it has any since we'll be adding these anyway
                        choice_text = strip_quotes(choice_text)

                        # If we have a pipe, use a menu
                        if '|' in quotes_passage:
                            jump_passage += 'menu:\n    "{}":\n        jump {}\n    {}'. \
                                format(choice_text, self.to_rpy_name(jump_statement), passage_rest)
                        else:
                            # Convert the jump statement to rpy name (which is used as the label)
                            jump_passage += 'jump ' + self.to_rpy_name(jump_statement) + passage_rest
            else:
                # If the passage doesn't have any [[ then just assign it to the string
                jump_passage = split_passage[0]

            # Check for <<set $[variable] to [value] ("[STRING]"/BOOLEAN/INT)>>
            # Swap to $ [variable] = [value]
            set_passage = ''
            # Check if we're setting variables
            if set_phrase in jump_passage:
                set_passage_split_list = jump_passage.split(set_phrase)
                # Start after the first instance of the set phrase
                for set_passage_split in set_passage_split_list[1:]:
                    # Get the set statement by splitting at next immediate instance of >>
                    set_passage_split_list = set_passage_split.split('>>', 1)
                    # This is our statement
                    set_passage_statement = set_passage_split_list[0]
                    # We only set what's after if it exists
                    set_passage_end = ''
                    if len(set_passage_split_list) > 1:
                        set_passage_end = set_passage_split_list[1]
                    # Replace the "to" inside the statement only
                    set_passage_statement = '$ ' + set_passage_statement.replace(' to ', ' = ')
                    # Replace Twine boolean phrase with the Ren'Py/Python accepted one
                    for boolean_phrase, boolean_replace in boolean_replace_dict.iteritems():
                        if boolean_phrase in set_passage_statement:
                            set_passage_statement = set_passage_statement.replace(boolean_phrase, boolean_replace)
                    set_passage += set_passage_statement + set_passage_end
            else:
                # If we aren't, just pass the jump passage as is
                set_passage = jump_passage

            # Check for if/else statements
            initial_if_phrase = '<<if $'
            if_passage = ''
            comparison_phrase_dict = {'is': '==', 'isnot': '!=',
                                      'gt': '>', 'gte': '>=',
                                      'lt': '<', 'lte': '<='}
            if_phrase_dict = {'<<if $': 'if ', '<<elseif $': 'elif ', '<<else': 'else', '>>': ':'}
            # Check if we have any conditionals in the passage
            if initial_if_phrase in set_passage:
                # If so, let's find the phrases
                if_passage_split = set_passage.split('<<')
                # The first part of the split won't have conditionals, so add as is
                if_passage += if_passage_split[0]
                for passage_split in if_passage_split[1:]:
                    # Only split if string isn't empty
                    if passage_split != '':
                        # Split again to get the conditional statement itself
                        if_phrase_split = passage_split.split('>>')
                        if_phrase = if_phrase_split[0]
                        if_result = ''
                        if len(if_phrase_split) > 1:
                            if_result = if_phrase_split[1]
                        for comparison_phrase, comparison_replace in comparison_phrase_dict.iteritems():
                            if comparison_phrase in if_phrase:
                                # No break because we could have multiple types of comparison
                                if_phrase = if_phrase.replace(comparison_phrase, comparison_replace)

                        # Indent everything in the conditional result except for the last line
                        # Hack: Don't indent after the if statement closes...
                        if '/if>>' not in passage_split:
                            if_newline_count = if_result.count('\n') - 1
                            if_result = if_result.replace('\n', '\n    ', if_newline_count)

                        # Retain original formatting to make it easier to find these
                        if_passage += '<<{}>>{}'.format(if_phrase, if_result)
                if_passage = if_passage.replace('<</if>>', '')
                for if_phrase, if_replace in if_phrase_dict.iteritems():
                    if_passage = if_passage.replace(if_phrase, if_replace)
            else:
                # If we don't, just pass the previous passage along
                if_passage = set_passage

            # Check for printed variables inside of messages
            # These would be occurring outside of the setting + conditionals
            # They will always use the form $[alpha character]
            variable_passage = ''
            if '$' in if_passage:
                variable_passage_split_list = if_passage.split('$')
                for i, variable_passage_split in enumerate(variable_passage_split_list):
                    # Anything before the first $ is not going to have a variable
                    # We now check if there's a letter immediately after the $, which gives us a variable
                    # First check the current passage split contains anything
                    # If $ is at the beginning of a passage, it could be 0 characters long
                    if len(variable_passage_split) > 0:
                        # If first, always add passage as is
                        if i == 0:
                            variable_passage += variable_passage_split
                        elif variable_passage_split[0].isalpha():
                            # We split immediately at the next non-alphanumeric or invalid variable character
                            stop_char = ' '
                            for var_char in variable_passage_split:
                                if not var_char.isalnum() and var_char != '_':
                                    stop_char = var_char
                                    break
                            variable_phrase_split_list = variable_passage_split.split(stop_char, 1)

                            # Check if we got anything
                            if len(variable_phrase_split_list) > 1:
                                variable_name, rest_of_var_passage = variable_phrase_split_list
                                # Put variable in Ren'Py inside-brackets format
                                variable_passage += '[{}]{}{}'.format(variable_name, stop_char, rest_of_var_passage)
                            else:
                                variable_passage += variable_passage_split
                        else:
                            # If not first passage, but not alpha, add back the $
                            variable_passage += '${}'.format(variable_passage_split)
            else:
                # If $ doesn't exist in the passage, just pass it through
                variable_passage = if_passage

            # TODO Reach goal: Adding if statements after menu options in Ren'Py
            #  Would have to figure out the Twine equivalent (in a way that would be straightforward to catch)
            # https://www.renpy.org/doc/html/menus.html
            # https://www.reddit.com/r/RenPy/comments/7zxe5f/conditional_menuentries/

            # Remove whitespace
            clean_passage = variable_passage.strip()

            # Combine the default and custom lists to make one list to iterate over
            self.char_replace_list = self.default_char_replace_list + self.custom_char_replace_list

            # Iterate over the list of terms to update
            # Generally we're replacing all the non-recognized characters with safe for Ren'Py ones
            for dict_pair in self.char_replace_list:
                for og_char, new_char in dict_pair.iteritems():
                    clean_passage = clean_passage.replace(og_char.encode('utf-8'), new_char.encode('utf-8'))

            # The passage label is the passage name since this is used in the jump text
            passage_text = 'label {}:\n    {}\n\n'.format(passage_name, clean_passage)

            # Add the current passage text to the rpy file passage
            document_passage += passage_text

            # Check if this is a document break or if it's the end of the twine document
            if passage_tags == self.get_config_value('doc_break') or passage_index == len(passage_list) - 1:
                # If it is, write the rpy passage file
                passage_file = open(os.path.join(self.data['script_dir'], rpy_file_name), 'w')
                n = passage_file.write(document_passage)
                passage_file.close()

                # Reset passage variables
                document_passage = ''
                create_file_name = True

        return True
