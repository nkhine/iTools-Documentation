How to build itools from Linux to Windows
#########################################

.. highlight:: sh

#. Install Wine
#. Install MinGW. Download from
   http://sf.net/project/showfiles.php?group_id=2435
   ::

      $ wine MinGW-5.1.4.exe

#. Install GLib. Download from http://www.gtk.org/download-windows.html
   ::

      $ cd .wine/drive_c/MinGW/
      $ unzip ~/download/glib-dev_2.18.4-1_win32.zip

#. Install Python (in Wine), http://www.python.org/download/
   ::

      $ msiexec /i python-2.5.4.msi
      $ msiexec /i python-2.6.1.msi

#. Edit the file :file:`~/.wine/drive_c/Python25/Lib/distutils/distutils.cfg`:

   .. code-block:: none

      [build]
      compiler = mingw32

#. Add MinGW to the system's path:

      1. Launch regedit

      2. Go to:

         .. code-block:: none

              HKEY_LOCAL_MACHINE
                System
                  CurrentControlSet
                    Control
                      Session Manager
                        Environment

      3. Append "c:\MinGW\bin" to the "PATH" variable

#. Install pywin32. Download from https://sourceforge.net/projects/pywin32/
   ::

      $ wine pywin32-212.win32-py2.5.exe

#. Enjoy::

      $ wine c:/Python25/python.exe setup.py bdist_wininst


