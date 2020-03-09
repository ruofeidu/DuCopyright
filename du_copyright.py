# Lint as: python3
# ------------------------------------------------------------------------------
# Licensed under Creative Commons Attribution-NonCommercial-ShareAlike 3.0\
# License with 996 ICU clause.
#
# The above license is only granted to entities that act in concordance with
# local labor laws. In addition, the following requirements must be observed:
# The licensee must not, explicitly or implicitly, request or schedule their
# employees to work more than 45 hours in any single week.
# The licensee must not, explicitly or implicitly, request or schedule their
# employees to be at work consecutively for 10 hours.
#-------------------------------------------------------------------------------
"""Adds or edits the copyright blocks in third_party folder."""
import os
import datetime
import logging


class DuCopyright:
  COPYRIGHT_MODIFY_EQUAL_LINES = 3

  def __init__(self,
               copyright_files,
               extension_white_list=[],
               folder_black_list=[]):
    """Sets white and black lists and reads copyright blocks for each type."""
    self._extension_white_list = extension_white_list
    self._folder_black_list = folder_black_list
    self._copyright = {}
    # Sets copyright blocks for each extension.
    for copyright_file in copyright_files:
      extension = DuCopyright.get_extension(copyright_file)
      with open(copyright_file, 'r', encoding='utf8') as f:
        self._copyright[extension] = f.readlines() + ['\n']
    self._year = datetime.date.today().year
    self._authors = 'Ruofei Du'

  @staticmethod
  def get_extension(filename):
    """Gets the extension of a filename."""
    return os.path.splitext(filename)[1][1:]

  def format(self, code_path, project_name):
    """Adds copyright blocks to all code files under code_path."""
    result_filenames = []
    num_modified = 0
    num_added = 0
    logging.info('Code path: ' + code_path)

    for root, dirs, filenames in os.walk(code_path):
      if root in self._folder_black_list:
        continue
      for filename in filenames:
        extension = DuCopyright.get_extension(filename)
        if extension not in self._extension_white_list:
          continue
        result_filenames.append(os.path.join(root, filename))

    logging.info('Files to parse: %s' % result_filenames)

    for filename in result_filenames:
      extension = DuCopyright.get_extension(filename)
      with open(filename, 'r', encoding='utf8') as f:
        lines = f.readlines()
      copyright_block = self._copyright[extension]
      modify = len(lines) >= len(copyright_block)
      if modify:
        votes = 0
        for i in range(len(copyright_block)):
          if lines[i] == copyright_block[i]:
            votes += 1
        if votes < self.COPYRIGHT_MODIFY_EQUAL_LINES:
          modify = False

      if not modify:
        lines = copyright_block + lines
        num_added += 1
      else:
        first_valid_line = 0
        while lines[first_valid_line].strip(
        ) == '' or lines[first_valid_line][0] == copyright_block[0][0]:
          first_valid_line += 1
        lines = copyright_block + lines[first_valid_line:]
        num_modified += 1

      # Formats the copyright block for each file.
      for i in range(len(copyright_block)):
        if lines[i].find('%s') != -1:
          lines[i] = lines[i] % (self._year, project_name, self._authors)

        with open(filename, 'w', encoding='utf8') as f:
          f.writelines(lines)

    # Prints statistics.
    print('Number of modified files: %d' % num_modified)
    print('Number of added files: %d' % num_added)


if __name__ == '__main__':
  CODE_PATH = os.path.join(os.getcwd(), 'tests')
  COPYRIGHT_FILES = ['996icu.cc', '996icu.py']
  PROJECT_NAME = 'DuCopyright'
  EXTENSION_WHITE_LIST = [
      'cpp', 'h', 'cc', 'py', 'cs', 'shader', 'cginc', 'glsl', 'glslinc'
  ]
  FOLDER_BLACK_LIST = ['private']
  formatter = DuCopyright(COPYRIGHT_FILES, EXTENSION_WHITE_LIST,
                          FOLDER_BLACK_LIST)
  formatter.format(CODE_PATH, PROJECT_NAME)
